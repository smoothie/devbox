# Pi coding environment

Installs Pi, Context7 MCP, DBHub for PostgreSQL/SQLite/MySQL/MariaDB, interoperable
`@tintinweb/pi-tasks` and `@tintinweb/pi-subagents`, and Vercel agent-browser with
its native MCP server. Pi's built-in MCP client is used; no MCP adapter or browser
wrapper package is required.

## Enable

Configure the existing inventory's group or host variables:

```yaml
webservers_stack:
  pi: true

pi_user: vagrant
pi_group: vagrant
pi_home: /home/vagrant
pi_projects:
  - path: /home/vagrant/projects/example
```

Preserve the other `webservers_stack` entries when enabling Pi. Project directories
must already exist; remove the example project entry when no rollout is needed.

```bash
cd ansible
ansible-galaxy collection install --requirements-file collections/requirements.yaml
ansible-galaxy install --role-file requirements.yaml
ansible-playbook site.yaml -i development.ini --tags pi
export PATH="$HOME/.local/bin:$PATH"
pi mcp list
pi
```

Authenticate the model through `/login` inside Pi. The role never writes
`auth.json`, `models.json`, tokens, or provider credentials. Use `/reload` in an
existing Pi session after provisioning; a fresh shell picks up a newly installed
`~/.local/bin` through Ubuntu's standard profile.

## Privacy defaults

Every Ansible run writes `enableInstallTelemetry: false` and
`enableAnalytics: false` to the user's `settings.json`, including when an existing
configuration has either flag enabled. Unrelated settings remain intact. These
flags take precedence over `pi_settings` so replacing that dictionary does not
silently re-enable reporting.

The Pi launcher, provisioning environment, and maintenance script also set
`PI_TELEMETRY=false`, overriding an inherited opt-in. These are Pi's documented
settings, not an unsupported `telemetry.enabled` object. This does not disable
update checks, provider API requests, or independently configured third-party
MCP services.

Explicit opt-in is available only through the role variables:

```yaml
pi_enable_install_telemetry: true
pi_enable_analytics: true
```

## Runtime and updates

The role owns a separate Node 24 LTS runtime under
`~/.local/share/devbox-pi`, verified against Node's published SHA-256 sums.
Wrappers in `~/.local/bin` select it explicitly, so project nvm versions do not
break Pi, MCP servers, or cron. Existing system and nvm Node installations are
not changed. Packages run as `pi_user`, not root; only APT requires elevation.

Reprovisioning selects the latest Node 24 LTS patch and updates all six npm
packages. Weekly updates run as the user on Monday at 06:15 by default and update
Pi, the two extensions, Context7, DBHub, and Chrome. Overlapping maintenance runs
are excluded with `flock`. Updates are not transactional: an upstream failure
returns a nonzero exit and leaves a log, so rerun after correcting the failure.

```bash
~/.local/bin/pi-devbox-update
```

The log is `~/.local/share/devbox-pi/update.log`. Node patch updates require
reprovisioning; the weekly command intentionally does not replace the runtime
under active processes. Reprovisioning should also not overlap a running update.
Restart active Pi sessions after updates. Other Pi packages remain configured and
can be updated separately with `pi update --extensions`.

Automatic updates execute newly published third-party code. Disable scheduling
for controlled environments:

```yaml
pi_update_schedule_enabled: false
pi_node_version: 24.22.1
pi_package_version: 1.4.0
pi_browser_version: 0.39.4
pi_context7_version: 4.4.4
pi_dbhub_version: 1.5.0
pi_tasks_version: 0.9.1
pi_subagents_version: 0.22.0
```

These are the locally verified versions, not minimum requirements. The default
for every version except the Node major is `latest`. Lifecycle scripts are
disabled during npm installation. The browser package supplies its native binary;
Chrome is downloaded separately as the unprivileged user.

## MCP and databases

Servers use deferred tool exposure. Context7 works without a key subject to the
upstream anonymous quota. For authenticated usage, inherit `CONTEXT7_API_KEY`
from the launching environment or supply an environment reference:

```yaml
pi_context7_env:
  CONTEXT7_API_KEY: ${CONTEXT7_API_KEY}
```

Only the isolated SQLite scratch file is enabled by default. Network database
entries are installed but disabled until a target is deliberately configured.
Enable a target through `/mcp` or configure connections in inventory:

```yaml
pi_database_connections:
  - name: sqlite
    dsn: sqlite:///home/vagrant/projects/example/var/dev.sqlite
    enabled: true
  - name: postgresql
    dsn: ${PI_POSTGRES_DSN}
    enabled: true
  - name: mysql
    dsn: ${PI_MYSQL_DSN}
    enabled: false
  - name: mariadb
    dsn: ${PI_MARIADB_DSN}
    enabled: false
```

Export the corresponding DSNs before starting Pi, using `postgres://`,
`mysql://`, or `mariadb://`. URL-encode credentials in DSNs. Environment references
are expanded by DBHub, not Ansible. Cron does not inherit interactive shell
exports; use `/mcp` from a correctly configured shell to diagnose database access.
Avoid literal secrets in inventory; use environment variables or Ansible Vault.

Each connection exposes `execute_sql` and `search_objects`. Defaults are
`readonly: true`, `max_rows: 1000`, `connection_timeout: 10` seconds, and
`query_timeout: 30` seconds. SQLite does not implement network query timeouts.
Use database-enforced read-only accounts too: tool policy is not an OS or database
privilege boundary. The SQLite scratch file is empty and outside projects.
A configured project SQLite file is never created by the role.

`pi_mcp_servers` overrides role-owned entries and can add other servers. Existing
unrelated MCP entries and settings are retained. The role owns its named servers;
reprovisioning reasserts inventory values. To retire a previously configured
connection, disable its server explicitly with `pi_mcp_servers.<name>.enabled:
false` or remove it through `pi mcp remove <name>`; omission alone preserves
existing user configuration.

## Tasks, subagents, and browser

Tasks use `session-global` storage outside repositories; auto-cascade is off.
`/tasks` and `/agents` expose their management interfaces. The matching
`tintinweb` extensions communicate directly, including `TaskExecute`; installing
a differently named subagent package does not provide that integration.

The browser skill loads current instructions from `agent-browser skills get core`
rather than a copied, stale command reference. Browser MCP uses the upstream
`agent-browser mcp` command with content boundaries and a 50,000-character output
limit. Use distinct browser sessions for independent agents and close them when
finished. The limits and boundaries are not a prompt-injection sandbox.

## Default AGENTS.md rollout

`pi_projects` is an explicit allowlist. By default, `AGENTS.md` is created only
when missing; existing project rules are preserved. No project is automatically
trusted and no Git configuration is changed.

```yaml
pi_agents_template: /path/on/ansible/controller/default-AGENTS.md.j2
pi_agents_force: false
pi_projects:
  - path: /home/vagrant/projects/example
  - path: /home/vagrant/projects/managed-example
    template: /path/on/ansible/controller/managed-AGENTS.md.j2
    force: true
```

`force: true` opts into replacing and subsequently updating that project's file;
Ansible keeps a backup. An individual project can also override `owner` and
`group`. The target user needs write access. Role changes do not overwrite
existing instructions unless replacement was explicitly enabled.

## Validation

On an already browser-capable Ubuntu host, isolated provisioning needs no model
credentials and touches only `/tmp/devbox-pi-smoke`:

```bash
cd ansible
ansible-playbook roles/pi/tests/settings_smoke.yaml -i localhost,
ANSIBLE_ROLES_PATH="$PWD/roles" ansible-playbook roles/pi/tests/smoke.yaml -i localhost,
ANSIBLE_ROLES_PATH="$PWD/roles" ansible-playbook roles/pi/tests/smoke.yaml -i localhost,
```

The second run should report `changed=0`. The test covers real installation,
project instruction preservation, enabled MCP connections, SQLite SQL execution
and write rejection, browser MCP navigation, and Context7 tool discovery. It
requires outbound npm, Node, Chrome download, Context7, and example.com access.
System dependency installation and cron are disabled in this isolated test;
validate them in a disposable Ubuntu VM before deploying to a new base image.
