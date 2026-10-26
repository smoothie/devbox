SHELL := /bin/bash
.DEFAULT_GOAL := check-ci
QA_IMAGE ?= devbox-qa:local
DOCKER_SOCKET ?= /var/run/docker.sock

.PHONY: qa-image qa-image-fresh qa test test-php check-ci

qa-image:
	docker build --pull --file tests/qa.Dockerfile --tag $(QA_IMAGE) .

qa-image-fresh:
	docker build --pull --no-cache --file tests/qa.Dockerfile --tag $(QA_IMAGE) .

qa: qa-image
	docker run --rm $(QA_IMAGE) bash ansible/qa.sh

test: qa-image
	docker run --rm $(QA_IMAGE) ansible-playbook ansible/roles/pi/tests/settings_smoke.yaml -i localhost,
	docker run --rm $(QA_IMAGE) python tests/php_templates.py

test-php: qa-image
	docker run --rm --volume $(DOCKER_SOCKET):/var/run/docker.sock $(QA_IMAGE) python tests/php_integration.py

check-ci: qa-image-fresh
	docker run --rm $(QA_IMAGE) bash ansible/qa.sh
	docker run --rm $(QA_IMAGE) ansible-playbook ansible/roles/pi/tests/settings_smoke.yaml -i localhost,
	docker run --rm $(QA_IMAGE) python tests/php_templates.py
	docker run --rm --volume $(DOCKER_SOCKET):/var/run/docker.sock $(QA_IMAGE) python tests/php_integration.py
