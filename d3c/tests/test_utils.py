from django.test import TestCase

from d3c.utils import get_ip, parse_ip, get_mac, validate_cpe, ValidationError


class ParseNmapTestCase(TestCase):
    """TODO: parse_nmap"""

    def test_placeholder(self):
        pass


class ParseCsvTestCase(TestCase):
    """TODO: parse_csv"""

    def test_placeholder(self):
        pass


class FillTemplateTestCase(TestCase):
    """TODO: fillTemplate, getFromContext"""

    def test_placeholder(self):
        pass


class IpMacHelpersTestCase(TestCase):
    """tests get_ip, parse_ip, get_mac"""

    def test_get_ip(self):
        """tests get_ip the cases: empty, invalid, valid v4, valid v6"""
        self.assertIsNone(get_ip(""))
        self.assertIsNone(get_ip("X.0.0.1"))
        self.assertEqual(get_ip("127.0.0.12"), "127.0.0.12/32")
        self.assertIsNone(get_ip("2001:0db8:85a3:08d3::0370:7344"))

    def test_parse_ip(self):
        """tests parse_ip the three cases: exception, valid v4, valid v6"""
        self.assertIsNone(parse_ip("127.0.0.X"))
        self.assertEqual(str(parse_ip("127.0.0.1")), "127.0.0.1/32")
        self.assertIsNone(parse_ip("2001:0db8:85a3:08d3::0370:7344"))

    def test_get_mac(self):
        """tests get_mac. Three cases: empty str, valid, invalid"""
        self.assertIsNone(get_mac(''))
        self.assertEqual(get_mac('00:1A:2B:3C:4D:5E'), '00:1A:2B:3C:4D:5E')
        self.assertIsNone(get_mac('00:1A:2B:3C:4D:YY'))


class ValidateCpeTestCase(TestCase):
    """TODO: validate_cpe"""

    def test_validate_cpe(self):
        validate_cpe("cpe:2.3:a:openssl:openssl:3.3.1:*:*:*:*:*:*:*")
        with self.assertRaises(ValidationError):
            validate_cpe("bla0123045")
        validate_cpe("0123")


class ValidatePurlTestCase(TestCase):
    """TODO: validate_purl"""

    def test_placeholder(self):
        pass


class ValidateFhTestCase(TestCase):
    """TODO: validate_fh"""

    def test_placeholder(self):
        pass


class ValidateUriTestCase(TestCase):
    """TODO: validate_uri"""

    def test_placeholder(self):
        pass
