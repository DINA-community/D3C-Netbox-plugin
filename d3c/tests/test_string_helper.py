from django.test import TestCase
from d3c.string_helper import get_sug
from d3c.string_normalizer import StringNormalizer

class DisassebmleRoleTestCase(TestCase):
    """TODO: disassebmle_role"""

    def test_placeholder(self):
        pass


class GetSpecificRoleTestCase(TestCase):
    """TODO: get_specific_role"""

    def test_placeholder(self):
        pass


class CheckChoiceTestCase(TestCase):
    """TODO: check_choice"""

    def test_placeholder(self):
        pass


class RouterChoicesTestCase(TestCase):
    """TODO: router_choices"""

    def test_placeholder(self):
        pass


class GetSugTestCase(TestCase):
    """tests get_sug(rsp, string_normalizer, string_checker, device_attr, device_value, finding_value)"""

    def test_get_sug_findings_empty(self):
        self.assertIsNone(get_sug(False, None, None, 'device_family', 'test', ''))

    def test_get_sug_equal_values(self):
        self.assertEqual(
            get_sug(False, None, None, 'device_family', 'test', 'test'),
            [(0, 'test'), (1,'test')]
        )

    def test_get_sug_diff_values(self):
        self.assertEqual(
            get_sug(False, None, None, 'device_family', 'device_val', 'finding_val'),
            [(0, 'device_val'), (1, 'finding_val')]
        )

    def test_simple_case_normalizer(self):
        normalizer = StringNormalizer()
        self.assertEqual(
            get_sug(True, normalizer, None, '', 'test', 'Siemens Ag'),
            [(0, 'test'), (1, 'Siemens')]
        )

    def test_normalized_value_eq_device_value(self):
        normalizer = StringNormalizer()
        self.assertEqual(
            get_sug(True, normalizer, None, '', 'Siemens', 'Siemens Ag'),
            [(0, 'Siemens'), (1, 'Siemens')]
        )

