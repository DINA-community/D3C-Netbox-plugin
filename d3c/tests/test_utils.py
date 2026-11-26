from django.test import TestCase

from d3c.utils import parse_nmap

class ParseNmapTestCase(TestCase):
    """tests parse_nmap"""

    def test_parse_nmap_no_record(self):
        """tests parse_nmap returns ({}, []) in no records found case"""
        xml = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE nmaprun>
<?xml-stylesheet href="file:///usr/local/share/nmap/nmap.xsl" type="text/xsl"?>
<!-- Nmap 7.94 scan initiated Wed Apr  2 14:47:50 2025 as: nmap -oX scan.xml -sV -O 192.168.1.0/24 -->
<nmaprun scanner="nmap" args="nmap -oX scan.xml -sV -O 192.168.1.0/24" start="1743598070" startstr="Wed Apr  2 14:47:50 2025" version="7.94" xmloutputversion="1.05">
<verbose level="0"/>
<debugging level="0"/>
<hosthint><status state="up" reason="arp-response" reason_ttl="0"/>
<address addr="192.168.1.10" addrtype="ipv4"/>
<address addr="AA:BB:CC:DD:EE:FF" addrtype="mac" vendor="Super Micro Computer"/>
<hostnames>
</hostnames>
</hosthint>
</nmaprun>
"""
        self.assertEqual(parse_nmap(xml.strip()), ({}, []))

class ParseCsvTestCase(TestCase):
    """TODO: parse_csv"""

    def test_placeholder(self):
        pass


class FillTemplateTestCase(TestCase):
    """TODO: fillTemplate, getFromContext"""

    def test_placeholder(self):
        pass


class IpMacHelpersTestCase(TestCase):
    """TODO: get_ip, parse_ip, get_mac"""

    def test_placeholder(self):
        pass


class ValidateCpeTestCase(TestCase):
    """TODO: validate_cpe"""

    def test_placeholder(self):
        pass


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
