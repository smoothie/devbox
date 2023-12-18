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

- **Custom System Dependencies:** Automatic setup of essential development tools
    - HTTP
        - [x] apache2
        - [ ] nginx
        - [ ] with SSL support
    - Code
        - [x] PHP (5.6 - 8.3)
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
          - [x] Helm
            - [x] MetalLB (Load Balancer) 
            - [x] NGINX Ingress
    - Others
        - [ ] Apache Solr
        - [ ] Blackfire
        - [x] Git
        - [ ] Grafana
        - [ ] Meilisearch
        - [ ] Minio
        - [ ] Prometheus
        - [x] Image Optimizers
        - [x] PDF Generation
        - [x] Conftest

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

## Installation

TBD

## Usage

TBD

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
