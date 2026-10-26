import hashlib
from pathlib import Path
import unittest

from jinja2 import Environment, FileSystemLoader, StrictUndefined
import yaml


ROOT = Path(__file__).resolve().parents[1]
ROLE = ROOT / "ansible/roles/php"
DEFAULTS = yaml.safe_load((ROLE / "defaults/main.yaml").read_text())


class PhpTemplatesTest(unittest.TestCase):
    def test_reviewed_repository_key_is_unchanged(self):
        key = (ROLE / "files/ondrej-php.asc").read_bytes()
        self.assertEqual(hashlib.sha256(key).hexdigest(),
                         "17cee003e52c7d4f197804c59460839950634fc6b8141967ef343655668428ca")

    def test_every_supported_version_has_active_files(self):
        for version in DEFAULTS["php_supported_versions"]:
            with self.subTest(version=version):
                self.assertIn(version, DEFAULTS["php_packages"])
                self.assertIn(version, DEFAULTS["php_ini_changes"])
                self.assertIn(f"php{version}-fpm", DEFAULTS["php_packages"][version])
                for relative in ["mods-available/xdebug.ini.j2", "fpm/pool.d/www.conf.j2"]:
                    self.assertTrue((ROLE / "templates" / version / relative).is_file(), relative)

    def test_php85_fpm_template(self):
        environment = Environment(loader=FileSystemLoader(ROLE / "templates"), undefined=StrictUndefined)
        rendered = environment.get_template("8.5/fpm/pool.d/www.conf.j2").render(DEFAULTS)
        self.assertIn("listen = /run/php/php8.5-fpm.sock", rendered)
        self.assertIn("user = www-data", rendered)
        self.assertIn("group = www-data", rendered)
        self.assertIn("pm.max_children = 16", rendered)

    def test_php85_xdebug_settings(self):
        environment = Environment(loader=FileSystemLoader(ROLE / "templates"), undefined=StrictUndefined)
        settings = dict(DEFAULTS, php_xdebug=dict(DEFAULTS["php_xdebug"], client_port=19003))
        rendered = environment.get_template("8.5/mods-available/xdebug.ini.j2").render(settings)
        self.assertIn("xdebug.client_port = 19003", rendered)
        self.assertIn("xdebug.mode = debug", rendered)

    def test_apache_routes_php85_to_fpm(self):
        templates = ROOT / "ansible/roles/apache2/templates/sites-available"
        environment = Environment(loader=FileSystemLoader(templates), undefined=StrictUndefined)
        rendered = environment.get_template("000-default.conf.j2").render(
            item={"key": "php85.test", "value": {
                "apache2_server_admin": "root@localhost",
                "apache2_document_root": "/var/www/php85",
                "php_version": "8.5",
            }},
            apache2_logs_directory="${APACHE_LOG_DIR}",
        )
        self.assertIn("php8.5-fpm.sock|fcgi://localhost", rendered)
        self.assertIn("ServerName php85.test", rendered)


if __name__ == "__main__":
    unittest.main(verbosity=2)
