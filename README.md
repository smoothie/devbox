# smoothie's Devbox

Yet another Ansible playbook for local development environment automation.

## Development Status

> :warning: **This project is currently in development and is not yet production-ready.** It is a
> work in progress, and there may be incomplete features or known issues. Use it at your own risk.

## Table of Contents

- [Project Description](#project-description)
- [Development Status](#development-status)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Description

As a developer, I enjoy a smooth local development environment. That's why I'm currently exploring
this devbox.

## Features

- **AI coding environment:** Optional [Pi role](ansible/roles/pi/README.md) with Context7,
  PostgreSQL/SQLite/MySQL/MariaDB MCP tools, integrated tasks and subagents, Vercel
  agent-browser, scheduled updates, and safe default `AGENTS.md` rollout.
- **Custom System Dependencies:** Automatic setup of essential development tools
    - HTTP
        - [x] apache2
        - [ ] nginx
        - [ ] with SSL support
    - Code
        - [x] PHP (5.6 - 8.5; legacy releases require explicit compatibility review)
            - PHP 8.5 is execution-tested on Ubuntu 22.04 and 24.04; see the [PHP role guide](ansible/roles/php/README.md).
            - [x] XDebug support
            - [x] Composer
        - [x] JavaScript
            - [x] Node.js (via nvm)
            - [ ] Deno (via dvm)
            - [x] npm (via nvm)
            - [ ] yarn
        - [x] Go
        - [x] Java
            - [ ] Gradle
            - [ ] Ivy
            - [ ] Maven
        - [ ] Python
    - Database
        - [x] MySQL
        - [x] MariaDB
        - [ ] PostgreSQL
        - [ ] SQLite
        - [ ] CouchDB
        - [ ] MongoDB
        - [x] Redis
        - [x] Memcached
        - [ ] InfluxDB
    - Messaging
        - [ ] Kafka
        - [ ] RabbitMQ
        - [ ] Gearman
    - ELK-Stack
        - [ ] Elasticsearch
        - [ ] Logstash
        - [ ] Kibana
        - [ ] Beats
    - Virtualization
        - [x] containerd
        - [x] Docker
        - [x] Kubernetes
          - [x] via k0s
            - [x] optional k0sctl
            - [x] Persistent storage via OpenEBS
          - [ ] via k3s
          - [ ] via kind
          - [ ] via kubeadm
          - [ ] via minikube
          - [ ] Podman
          - [x] kubectl
            - [x] kubectx
          - [x] Helm
            - [x] MetalLB (Load Balancer) 
            - [x] NGINX Ingress
          - [x] k9s
    - Others
        - [ ] Apache Solr
        - [ ] Blackfire
        - [x] Git
          - [x] pre-commit
        - [ ] Grafana
        - [ ] Meilisearch
        - [ ] Minio
        - [ ] Prometheus
        - [x] Image Optimizers
        - [x] PDF Generation
        - [x] Conftest
        - [x] gcloud SDK
        - [x] Mailpit
        - [x] LDAP

### TODO

- [ ] Consider (ADR) splitting groups into devmachine, devcontroller:
  - The machine would be the current webserver stuff (virtual machine managed via vagrant).
  - The controller would be the host. So stuff like PHPStorm, browsers and so could be installed.
- [ ] k0s: 
  - Update kubectl auth when installing k0s.
  - Consider (ADR) extracting deployments into separate roles, maybe per use case e.g. one for ingress-nginx, another one for metallb, another one for k0sctl.
- [ ] bash completions: Add a role which lets us add bash completions and computes enabled CLI's into that one. 
- [ ] Support self-signed apache2 vhosts
- [ ] Fix apache2, php, user permissions
    - Context: Currently we rewrite apache, php user to vagrant:vagrant.  
      This is considered a bad practice, that's why we should do something else (TBD).
- [ ] Maintenance Tasks
  - Check stuff  
    - Check for apt updates
    - Check for pip updates
    - Check for composer upgrades
    - Check for current used npm/node updates
  - Do stuff
    - [ ] Upgrade apt packages
    - [ ] Upgrade pip packages
    - [ ] Upgrade composer
    - [ ] Upgrade for current used npm/node
- [ ] QA
  - Test the vagrant setup
    - [ ] Check that configuration is applied as expected (mounts, virtual provider)

## Installation

TBD

## Usage

Enable `webservers_stack.pi: true` in the existing inventory to provision the AI
coding environment, then run:

```bash
cd ansible
ansible-playbook site.yaml -i development.ini --tags pi
```

See the [Pi role guide](ansible/roles/pi/README.md) for prerequisites, authentication,
database targets, updates, and default project instruction distribution.
See the [maintenance review](docs/maintenance-review.md) for verified download fixes
and remaining infrastructure upgrade risks.

## Quality gates

Docker Engine and GNU Make are the only host prerequisites for checks. The QA
image pins Python, Ansible, lint tools, collections, and Galaxy roles; host Python
and previously installed Ansible collections do not participate.

```bash
make check-ci
```

This is also the GitHub Actions entry point and must pass before every commit
and push. It rebuilds the QA image without cache, runs strict YAML/Ansible checks,
tests Pi privacy/configuration reconciliation, checks every supported PHP
version's active template paths, and provisions the complete PHP 8.5 package set
in fresh Ubuntu 22.04 and 24.04 containers. Each target must serve PHP through
Apache/FPM, rerun unchanged, and recover a stopped FPM service.

For shorter iterations, `make qa` runs static checks, `make test` runs isolated
configuration/template tests, and `make test-php` runs real PHP acceptance tests.
These targets allow Docker build caching but always include current source.
The full gate normally takes about 8–12 minutes with available package mirrors.

The PHP tests mount `DOCKER_SOCKET` (default `/var/run/docker.sock`) into the QA
controller so it can create and clean up disposable sibling containers. Docker
socket access is root-equivalent; only run trusted checkout contents. Tests do
not bind host ports or change host services, and do not require privileged
containers. Ubuntu images are digest-pinned; APT still resolves current packages.
A full Vagrant boot and systemd boot behavior are separate acceptance tests.

## Contributing

Contributions are one thing that make the open source community such an amazing place to learn,
inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull
request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
