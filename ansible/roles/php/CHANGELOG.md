# Changelog

All notable changes are documented in this file, following Keep a Changelog 1.1.0.

## [Unreleased]

### Added

- Real PHP 8.5 installation and Apache/FPM acceptance coverage on Ubuntu 22.04 and 24.04.

### Fixed

- Repository signing uses a reviewed bundled public key instead of unstable keyserver response bytes.
- Selected FPM services start even when already enabled but stopped; unselected services stop independently of enablement.
- PHP packages rely on their module activation scripts instead of invalid package-name arguments to `phpenmod`.
- PHP 8.5 Xdebug configuration applies the configured client port.
