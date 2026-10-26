# Devbox maintenance review

Verified on 2026-10-26 against clone `3993799b02fbe19a2f5eabc90548f60ecf074818`.
This review distinguishes implemented fixes from migrations that need a disposable
VM and an explicit compatibility decision. No existing VM services were upgraded
or restarted during the review.

## Implemented

| Area | Finding | Change |
| --- | --- | --- |
| Pi | No coding-agent provisioning role | Optional `pi` role with current tools, isolated Node 24 LTS, updates and project instruction rollout |
| PHP download | Repository HTML was downloaded as a key; subsequent live-key checksums failed on varying armor headers | Ship the reviewed public key and use a dedicated `signed-by` keyring |
| PHP source | `jammy` was hard-coded irrespective of the host | Select Jammy or Noble from host facts; fail clearly on other releases |
| nvm | Installer was pinned to v0.39.4, world-writable in shared `/tmp`, and successful runs were reported unchanged | v0.40.8, installed-version detection, user-owned private installer and real change reporting |
| VM example | `ubuntu_version: 2004` did not match `ubuntu/<box>` naming or the Jammy default | Use `jammy64` consistently |
| Quality gates | Ansible lint configuration implicitly enabled file rewriting | Checks are read-only; shell QA runner simplified |
| Line endings | Existing repository contents and host `core.autocrlf=true` produce CRLF shell/YAML failures on Linux | `.gitattributes` enforces LF for future checkouts, matching `.editorconfig` |

Pi's verified package set is Pi 1.4.0, Node 24.22.1, agent-browser 0.39.4,
Context7 MCP 4.4.4, DBHub 1.5.0, pi-tasks 0.9.1, and pi-subagents 0.22.0.
Chrome for Testing 156.0.8078.47 was downloaded and exercised. The browser's
upstream native MCP implementation makes third-party browser MCP wrappers
unnecessary.

## PHP evidence

The [Launchpad API](https://api.launchpad.net/1.0/~ondrej/+archive/ubuntu/php)
identifies signing fingerprint
`B8DC7E53946656EFBCE4C1DD71DAEAAB4AD4CAB6`. Live keyserver responses for this
same fingerprint produced different SHA-256 values because armor headers varied;
the initial checksum-pinned download failed during real provisioning. The role
now ships the reviewed key without variable armor headers. Its SHA-256 is
`17cee003e52c7d4f197804c59460839950634fc6b8141967ef343655668428ca` and is
regression-tested. Jammy and Noble APT installations accepted this scoped key.
Key rotation requires a deliberate review and update of the bundled public key.

The Jammy and Noble PPA package indices were compared against the role's PHP
8.3, 8.4 and 8.5 package names, including virtual `Provides`: no missing names
were found. That initial availability check was not an execution test. Follow-up
acceptance now installs the complete PHP 8.5 package set on fresh Jammy and Noble,
executes PHP 8.5.12 CLI/CGI/debugger/development binaries, validates Apache/FPM
configuration and serves a real HTTP endpoint through the FPM socket. CLI and
FPM both load the expected extension set and configured Xdebug port. The
`php8.5-interbase` package supplies `pdo_firebird`, not `interbase`. Both unchanged
reruns report `changed=0`, and both targets recover a deliberately stopped FPM.

The PPA now states that Ubuntu Resolute should use the canonical
[packages.sury.org](https://packages.sury.org/php/) repository. Jammy and Noble
remain available in the PPA. A 26.04 migration must therefore review the base box,
repository setup and extension compatibility together; changing only the Ubuntu
codename is unsafe.

The Apache `conf-available` template directory stops at PHP 8.3, but those files
are not used by `roles/apache2/tasks/main.yaml`. Active vhosts interpolate their
PHP socket directly, and PHP FPM/Xdebug templates already exist for 8.4 and 8.5.
Automated template-path checks cover every declared supported PHP version;
executable acceptance is specifically for PHP 8.5, not every legacy version.

## Remaining priorities

1. **Docker API exposure:** `site.yaml` configures `tcp://0.0.0.0:2375`, and the VM
   example forwards it to the host. This is unauthenticated root-equivalent
   access, not a harmless development port. Prefer the Unix socket or an SSH
   Docker context. Changing it can break existing host integrations, so it was
   not changed on the running machine.
2. **Lifecycle review:** the example pins Go 1.21.0 and OpenJDK 18, while local
   roles pin kubectl 1.28.4 and k9s 0.29.1. These are old selections, not verified
   current releases. Choose supported Go/Java lines and match kubectl's supported
   skew to the actual cluster before updating; do not blindly choose `latest`.
   PHP 5.6–8.1 defaults remain legacy compatibility options and should not be
   interpreted as upstream security-supported releases.
3. **Dependency updates:** QA Python packages and Ansible collections are now
   pinned; the LDAP role's floating `master` has been replaced with a commit.
   Other runtime downloads still need a broader checksum audit. Pi packages
   default to automatic updates by request; controlled environments should pin
   versions and disable scheduling.
4. **Existing configuration defects:** Docker's
   `docker_config.install_compose | true` expression still needs runtime validation.
   Apache's group replacement was fixed and exercised with a username different
   from the group name. FPM socket permissions remain a separate hardening task.
5. **Fresh-machine acceptance:** validate browser APT dependencies, cron, PHP
   repository migration and all enabled services together in a disposable VM.
   Existing-library smoke tests do not prove a clean machine's dependency graph.

## Validation and boundaries

- Pi and nvm roles were provisioned in isolated `/tmp` homes and rerun to test
  idempotence. Existing project `AGENTS.md` content was preserved.
- Real MCP calls navigated example.com and read its title; SQLite returned
  `SELECT 42` and rejected `CREATE TABLE`; Context7 completed tool discovery.
  A separate anonymous Context7 library lookup returned the Ansible documentation.
- Real local Pi tools created/updated a task and ran an isolated subagent that
  returned `SUBAGENT_OK`. The package pair loads on Pi 1.4.0.
- `pi-devbox-update` was executed successfully against the isolated installation;
  wrapper scripts passed `bash -n`.
- GitHub's newer MySQL collection exposed deprecated `community.mysql`
  redirects missed by the original host's older dependencies. Both database
  roles now use `ansible.mysql`, with a pinned collection installed explicitly.
  `make check-ci` rebuilds the pinned Docker controller and invokes the same gates
  locally and in Actions; no host Python or existing collections are used.
- Pi writes `enableInstallTelemetry: false` and `enableAnalytics: false` on
  Ansible runs, preserving unrelated settings. Managed processes also receive
  `PI_TELEMETRY=false`. Regression tests cover prior opt-ins and deliberate opt-in
  through the dedicated role variables.

PostgreSQL, MySQL and MariaDB executables/configurations are installed, but no
application credentials were assumed and no live network database was queried.
Only the isolated SQLite database is enabled by default. Browser dependency APT
installation and cron were deliberately disabled in the isolated smoke playbook.
PHP package installation and Apache/FPM execution are now covered in disposable
containers. No full Vagrant/systemd boot was performed. The PHP role still uses
`apt_repository`, deprecated for removal in ansible-core 2.25; the pinned 2.21
controller reports this separately from lint violations.
