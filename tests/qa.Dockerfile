FROM python:3.13-slim-bookworm@sha256:e32be0e55814a08977501ca863271d9bd02443710db8f2afaf8372e2c4508530
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ANSIBLE_ROLES_PATH=/workspace/ansible/roles:/opt/ansible/roles \
    ANSIBLE_COLLECTIONS_PATH=/opt/ansible/collections \
    ANSIBLE_LOCAL_TEMP=/tmp/ansible-local \
    ANSIBLE_GALAXY_SERVER_TIMEOUT=180
RUN apt-get update && apt-get install --yes --no-install-recommends ca-certificates git \
    && rm -rf /var/lib/apt/lists/*
COPY requirements-qa.txt /tmp/requirements-qa.txt
RUN pip install --no-cache-dir --requirement /tmp/requirements-qa.txt && pip check
COPY ansible/requirements.yaml /tmp/roles.yaml
COPY ansible/collections/requirements.yaml /tmp/collections.yaml
RUN for attempt in 1 2 3; do \
      echo "Galaxy role installation attempt ${attempt}/3"; \
      ansible-galaxy role install --role-file /tmp/roles.yaml --roles-path /opt/ansible/roles && exit 0; \
    done; exit 1
RUN for attempt in 1 2 3; do \
      echo "Galaxy collection installation attempt ${attempt}/3"; \
      ansible-galaxy collection install --requirements-file /tmp/collections.yaml && exit 0; \
    done; exit 1
COPY . /workspace
WORKDIR /workspace
CMD ["bash", "ansible/qa.sh"]
