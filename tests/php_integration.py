import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

import docker


ROOT = Path(__file__).resolve().parents[1]
IMAGES = {
    "jammy": "ubuntu:22.04@sha256:0a9887931b0e38af2e3487ed39e29436b0535c4f3f52e57745baaf79d1898956",
    "noble": "ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac",
}


def execute(container, command):
    result = container.exec_run(["bash", "-ec", command], environment={"DEBIAN_FRONTEND": "noninteractive"})
    print(result.output.decode(errors="replace"), flush=True)
    if result.exit_code:
        raise RuntimeError(f"Container command failed with exit {result.exit_code}: {command}")


def provision(inventory, variables=None):
    command = ["ansible-playbook", str(ROOT / "tests/php85.yaml"), "-i", str(inventory)]
    if variables:
        command.extend(["--extra-vars", json.dumps(variables)])
    result = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=dict(os.environ, ANSIBLE_NOCOLOR="1"),
        timeout=1200,
    )
    print(result.stdout, flush=True)
    if result.returncode:
        raise RuntimeError(f"PHP 8.5 acceptance playbook failed with exit {result.returncode}")
    return result.stdout


def verify_distribution(client, distribution, image):
    print(f"Testing PHP 8.5 on fresh Ubuntu {distribution}", flush=True)
    client.images.pull(image)
    container = client.containers.run(image, ["sleep", "infinity"], detach=True)
    try:
        execute(container, "apt-get update && apt-get install --yes python3 python3-apt ca-certificates")
        with tempfile.TemporaryDirectory(prefix="devbox-php85-") as directory:
            inventory = Path(directory) / "inventory.json"
            inventory.write_text(json.dumps({"all": {"hosts": {container.id: {
                "ansible_connection": "community.docker.docker_api",
                "ansible_python_interpreter": "/usr/bin/python3",
                "ansible_user": "root",
            }}}}))
            provision(inventory)
            repeated = provision(inventory)
            if not re.search(r"\bchanged=0\s", repeated):
                raise AssertionError(f"PHP 8.5 provisioning is not idempotent on {distribution}")
            execute(container, "service php8.5-fpm stop")
            provision(inventory)
            provision(inventory, {"apache2_user": "www-data", "apache2_group": "www-data"})
        print(f"PASS {distribution}: full packages, CLI, FPM, Apache HTTP, idempotence, service recovery and identity change", flush=True)
    finally:
        container.remove(force=True)


if __name__ == "__main__":
    client = docker.from_env(timeout=120)
    try:
        for distribution, image in IMAGES.items():
            verify_distribution(client, distribution, image)
    finally:
        client.close()
