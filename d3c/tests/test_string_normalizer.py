from django.test import TestCase
from d3c.string_normalizer import StringNormalizer

class StringNormalizerTestCase(TestCase):
    """tests normalize and helper method"""

    def test_get_master_word_from_dictionary(self):
        """tests helper method _get_master_word_from_dictionary of the
        StringNormalizer."""
        normalizer = StringNormalizer()
        method = normalizer._get_master_word_from_dictionary

        master_dict = {
            "testA": ["testa", "TESTA", "Test XY A"]
        }
        self.assertEqual(method("testA", master_dict, True), "testA")
        self.assertEqual(method("testa", master_dict, True), "testA")
        self.assertEqual(method("TestA", master_dict, True), "")
        self.assertEqual(method("tEsTa", master_dict, False), "testA")
        self.assertEqual(method("test xy A", master_dict, False), "testA")
        self.assertEqual(method("Test Xyz B", master_dict, False), "")

    def test_normalize(self):
        """tests the normalize method of StringNormalizer."""
        normalizer = StringNormalizer()
        method = normalizer.normalize

        specific_dict_str = "Manufacturer"
        self.assertEqual(method("", specific_dict_str, False), "")
        self.assertEqual(method("Siemens", specific_dict_str, False), "Siemens")
        self.assertEqual(method("Siemens AG", "Test", False), "Siemens")
