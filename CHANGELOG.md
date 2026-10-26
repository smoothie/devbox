# Changelog

All notable changes are documented in this file, following Keep a Changelog 1.1.0.

## [Unreleased]

### Added

- Optional Pi coding environment with documentation, database and browser MCP
  integrations, task tracking, subagents, scheduled updates and project instruction
  distribution.
- Maintenance review with verified fixes and prioritized upgrade risks.

### Changed

- nvm provisioning targets v0.40.8 with version detection and user-owned installers.
- The example VM selects the existing Jammy box convention rather than `ubuntu/2004`.
- Ansible lint runs no longer implicitly rewrite source files.

### Fixed

- PHP installation downloads a checksum-verified PPA signing key rather than an
  HTML directory page, and selects the target Ubuntu distribution explicitly.
- Linux checkouts enforce LF line endings for executable scripts and YAML checks.
