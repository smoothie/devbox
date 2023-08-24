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

As a web developer, I know the importance of a smooth local development environment. That's why 
I created smoothie's Devbox—an Ansible playbook that does the heavy lifting for me... and maybe 
for you too.

## Features

- **Custom System Dependencies:** Automatic setup of essential development tools
  - HTTP
    - [x] apache2
    - [ ] nginx
    - [ ] with SSL support
  - Code
    - [x] PHP (5.6 - 8.3)
      - [x] XDebug support
      - [ ] Composer
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
    - [ ] Memcached
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
  - Others
    - [ ] Apache Solr
    - [ ] Blackfire
    - [x] Git
    - [ ] Grafana
    - [ ] Meilisearch
    - [ ] Minio
    - [ ] Prometheus
- [x] **Streamlined Project Organization:** Dedicated vendor folder for each client, ensuring a 
  well-organized and clean structure.
- [x] **Simple Environment Setup:** No fuss, no stress – just smooth sailing!

### TODO

- [x] Fix Xdebug config for Xdebug 2 (php: 5.6, 7.0, 7.1).
    - Fixed: Add missing php5.6-xdebug packages on defaults :facepalm:
- [x] Extract common:git into separate role
    - [x] Set defaults (git user, mail, global gitignore, default branch name)
    - git config --global init.defaultBranch
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
request. You can also simply open an issue with the tag "enhancement". Don't forget to give the 
project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
