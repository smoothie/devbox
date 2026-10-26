import grp
import json
from pathlib import Path
import pwd
import sys


expected = [pwd.getpwnam(sys.argv[1]).pw_uid, grp.getgrnam(sys.argv[2]).gr_gid]
workers = []
for process in Path("/proc").iterdir():
    if not process.name.isdigit():
        continue
    try:
        if (process / "comm").read_text().strip() != "apache2":
            continue
        status = dict(line.split(":", 1) for line in (process / "status").read_text().splitlines())
        identity = [int(status["Uid"].split()[1]), int(status["Gid"].split()[1])]
    except (FileNotFoundError, ProcessLookupError):
        continue
    if identity[0] != 0:
        workers.append(identity)
assert workers, "No non-root Apache workers found"
assert all(worker == expected for worker in workers), {"expected": expected, "workers": workers}
print(json.dumps({"expected": expected, "workers": workers}))
