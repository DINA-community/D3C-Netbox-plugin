from django.test import TestCase

from d3c.string_helper import disassemble_role, get_specific_role

class DisassembleRoleTestCase(TestCase):
    """tests disassemble_role"""

    def test_disassemble_role(self):
        """tests the different cases of disassemble_role."""
        fct = disassemble_role
        oracle = [
            ("", None),
            ("io", ["Sensor", "Actuator"]),
            ("HMI", ["HMI Field", "Scada Client"]),
            ("gateway", ["Switch L2", "Switch L3", 'Firewall', 'Router', 'Gateway Koppler']),
            ("server", ["Active Directory", "Server"]),
            ("test", None)
        ]
        for item in oracle:
            self.assertEqual(fct(item[0]), item[1])


class GetSpecificRoleTestCase(TestCase):
    """tests get_specific_role"""

    def test_get_specific_role(self):
        """tests the different cases."""
        fct = get_specific_role
        oracle = [
            ("", "test", []),
            ("test", "test", [(0, "test")]),
            ("Server", "server", [(0, "Server"), (1, "Active Directory")])
        ]
        for item in oracle:
            self.assertEqual(fct(item[0], item[1]), item[2])



class CheckChoiceTestCase(TestCase):
    """TODO: check_choice"""

    def test_placeholder(self):
        pass


class RouterChoicesTestCase(TestCase):
    """TODO: router_choices"""

    def test_placeholder(self):
        pass


class GetSugTestCase(TestCase):
    """TODO: get_sug"""

    def test_placeholder(self):
        pass
