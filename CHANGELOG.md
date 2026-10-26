# Changelog

All notable changes are documented in this file, following Keep a Changelog 1.1.0.

## [Unreleased]

### Added

- Optional Pi coding environment with documentation, database and browser MCP
  integrations, task tracking, subagents, scheduled updates and project instruction
  distribution.
- Maintenance review with verified fixes and prioritized upgrade risks.
- Docker-backed Make targets with the same pinned QA environment locally and in
  GitHub Actions, including executable PHP 8.5 acceptance on Jammy and Noble.

### Changed

- nvm provisioning targets v0.40.8 with version detection and user-owned installers.
- The example VM selects the existing Jammy box convention rather than `ubuntu/2004`.
- Ansible lint runs no longer implicitly rewrite source files.
- MySQL and MariaDB provisioning use canonical `ansible.mysql` modules with a
  pinned collection; controller dependencies and Galaxy roles are pinned.
- Pi provisioning disables install telemetry and analytics by default, including
  existing opt-ins and inherited telemetry environment variables.

### Fixed

- PHP installation uses a reviewed bundled PPA signing key rather than HTML or
  unstable keyserver response bytes, and selects the Ubuntu distribution explicitly.
- PHP 8.5 provisioning respects the Xdebug port and converges stopped FPM
  services; module activation no longer passes package names to `phpenmod`.
- Apache applies the requested process group without overwriting its process user,
  and restarts workers when their configured identity or group membership changes.
- Linux checkouts enforce LF line endings for executable scripts and YAML checks.
