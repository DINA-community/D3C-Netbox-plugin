from django.test import TestCase

from d3c.string_helper import (
    disassemble_role,
    get_specific_role,
    check_choice,
    router_choices
)

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
    """tests check_choice"""

    def test_check_choice(self):
        """tests the different cases."""
        choices = [("testa", 0), ("testb", 1)]
        self.assertEqual(check_choice(choices, "testA"), "testa")
        self.assertEqual(check_choice(choices, "testB"), "testb")
        self.assertIsNone(check_choice(choices, "testC"))


class RouterChoicesTestCase(TestCase):
    """tests router_choices"""

    def test_router_choices(self):
        """tests the different cases."""
        oracle = (
            ("yes", "true", [(0, "Yes")]),
            ("no", "false", [(0, "No")]),
            ("yes", "maybe", [(0, "Yes"), (1, "No")]),
            ("no", "m", [(0, "No"), (1, "Yes")]),
            ("test", "maybe", [(0, "Test"), (1, "Yes"), (2, "No")]),
            ("test", "test", None)
        )
        for item in oracle:
            self.assertEqual(router_choices(item[0], item[1]), item[2])


class GetSugTestCase(TestCase):
    """TODO: get_sug"""

    def test_placeholder(self):
        pass
