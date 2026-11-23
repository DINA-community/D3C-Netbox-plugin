import contextlib
import io

from django.test import TestCase

from d3c.populate import get_value, Handler, REPO


class GetValueTestCase(TestCase):
    """tests get_value"""

    def test_get_value(self):
        """tests the cases of get_value: found None, found str, not-found default"""
        dict_ = {
            "testA": None,
            "testB": "test"
        }
        self.assertEqual(get_value("testA", dict_), None)
        self.assertEqual(get_value("testB", dict_), "test")
        self.assertEqual(get_value("testC", dict_), '')


class HandlerTestCase(TestCase):
    """tests Handler."""

    def test_create_and_call(self):
        """creates a Handler and calls its log function."""
        handler = Handler("d3c.test_populate.HandlerTestCase")
        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            handler.verbose_log("Test")
        self.assertEqual(f.getvalue(), "Test\n")
        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            handler.logger.warning("Test2")
        self.assertEqual(f.getvalue(), "Test2\n")


class REPOTestCase(TestCase):
    """tests REPO."""

    @classmethod
    def setUpTestData(cls):
        """class method to setup data"""
        cls.repo = REPO("testtesttest")

    def test_slug_format(self):
        """tests the slug_format helper function."""
        self.assertEqual(self.repo.slug_format("test\n"), "test-")
        self.assertEqual(self.repo.slug_format("test"), "test")

    def test_get_relative_path(self):
        """tests helper."""
        self.assertEqual(self.repo.get_relative_path(), "testtesttest")

    def test_get_absolute_path(self):
        """tests helper."""
        self.assertIn("testtesttest", self.repo.get_absolute_path())
        self.assertIn(self.repo.cwd, self.repo.get_absolute_path())
