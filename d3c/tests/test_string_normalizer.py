from django.test import TestCase
from d3c.string_normalizer import StringNormalizer


class StringNormalizerTestCase(TestCase):

    def test_simple(self):
        normalizer = StringNormalizer()
        self.assertEqual(normalizer.normalize('Siemens Ag', ''), 'Siemens')
