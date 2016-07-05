from unittest import TestCase

from .settings_utils import parse_secure_proxy_ssl_header


class ParseSecureProxySslHeaderTests(TestCase):
    def test_basic_functionality(self):
        self.assertEqual(
            parse_secure_proxy_ssl_header('X-Forwarded-Proto: https'),
            ('HTTP_X_FORWARDED_PROTO', 'https')
        )
