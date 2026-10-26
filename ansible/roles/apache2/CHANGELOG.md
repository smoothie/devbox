# Changelog

All notable changes are documented in this file, following Keep a Changelog 1.1.0.

## [Unreleased]

### Fixed

- Configured process groups no longer overwrite the Apache process user.
- User/group and group-membership changes restart the parent and workers instead
  of leaving the previous identity active after a graceful reload.
