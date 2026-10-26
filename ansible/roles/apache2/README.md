# Apache HTTP server

Installs Apache, configures its process identity, enables proxy/FastCGI and rewrite
modules, and renders the virtual hosts in `apache2_sites`. Each site supplies a
server admin and document root; sites with `php_version` route PHP requests to
that version's FPM socket. The PHP role must provision the requested FPM runtime.
The active template is `templates/sites-available/000-default.conf.j2`; older
static `conf-available` templates are not copied by this role.

`apache2_user` and `apache2_group` select separate process identity fields in
`/etc/apache2/envvars`. Identity or supplementary-group changes notify a restart,
not a graceful reload: an existing parent process otherwise retains its old
environment. Ordinary virtual-host configuration changes notify a reload.

`make test-php` from the repository root installs this role with PHP 8.5 on fresh
Ubuntu 22.04 and 24.04 containers. It checks configuration syntax, real FastCGI
HTTP execution, repeat-run idempotence, and actual worker identities after
changing the configured user/group on an already-enabled virtual host.
`make check-ci` rebuilds the controller and runs this acceptance suite together
with the static quality gates before commits and in GitHub Actions. This is not
a Vagrant boot or systemd lifecycle test.
