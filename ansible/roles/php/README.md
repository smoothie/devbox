# PHP runtime

Installs the configured PHP versions and extensions from the distribution-matched
Ondřej Surý PPA, writes CLI/FPM settings, installs Xdebug and FPM pool templates,
and converges selected FPM services to enabled and running. Unselected installed
FPM services are stopped and disabled. Ubuntu 22.04/Jammy and 24.04/Noble are the
supported PPA targets; other distributions fail before repository changes.

## Select PHP 8.5

The site playbook derives required versions from `apache2_sites`:

```yaml
apache2_sites:
  example.test:
    apache2_server_admin: root@localhost
    apache2_document_root: /var/www/example/public
    php_version: "8.5"
```

A standalone invocation can set `php_versions: ["8.5"]` and
`apache2_sites: {}`. The FPM user/group must already exist; the site playbook uses
its configured host account. Standalone role defaults use `www-data`.

Active PHP 8.5 files are:

- `defaults/main.yaml`: package names, supported versions, INI values and Xdebug/FPM settings.
- `templates/8.5/mods-available/xdebug.ini.j2`: loaded Xdebug configuration including `client_port`.
- `templates/8.5/fpm/pool.d/www.conf.j2`: pool and `/run/php/php8.5-fpm.sock` configuration.
- `../apache2/templates/sites-available/000-default.conf.j2`: dynamically selects the PHP 8.5 FPM socket.

The Apache role's older static `conf-available` templates are not used by the
active provisioning path. No separate static Apache 8.5 template is required.
APT's package maintainer scripts enable installed modules; package names are not
passed as module names to `phpenmod`. For example, `php8.5-interbase` supplies
`pdo_firebird`, not a loaded module named `interbase`.

## Repository trust

`files/ondrej-php.asc` contains the reviewed public signing key with fingerprint
`B8DC7E53946656EFBCE4C1DD71DAEAAB4AD4CAB6`. It is copied to a dedicated
`/etc/apt/keyrings/devbox-php.asc` and scoped with `signed-by`. Keyserver armor
headers vary between responses even for the same key, so provisioning does not
pin a live keyserver response's bytes. The checked-in key has a regression-tested
SHA-256 digest; key rotation requires an explicit source review.

## Executable acceptance

From the repository root:

```bash
make test-php
```

On 2026-10-26, the complete PHP 8.5 package list installed successfully and PHP
8.5.12 passed on fresh Ubuntu 22.04 and 24.04 containers. Tests execute the CLI,
CGI, debugger and development binaries, validate FPM and Apache configurations,
and assert that Apache serves JSON from PHP-FPM rather than returning PHP source.
All expected extension modules, the custom Xdebug port, memory limit and timezone
are checked in both CLI and FPM. The second provisioning run must report
`changed=0`; another run must recover a deliberately stopped FPM service. A final
run changes Apache's user/group on the already-enabled site and asserts the
actual worker process identities, requiring a restart rather than only a reload.

`make test` additionally checks that every declared supported version has its
package list, INI configuration and active FPM/Xdebug templates. Existence checks
for older PHP versions are not execution or upstream security-support claims.
The full `make check-ci` rebuilds the controller image and runs all static and
runtime checks locally and in GitHub Actions. Container service tests use SysV
init scripts; Vagrant/systemd boot and legacy-release combinations are not tested
by this suite. Existing FPM socket permissions remain unchanged.
