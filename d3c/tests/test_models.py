from django.db.utils import IntegrityError
from dcim.models import Manufacturer
from utilities.testing import TestCase
from d3c.models import (
    Communication,
    CommunicationFinding,
    DeviceFinding,
    FileHash,
    Hash,
    Mapping,
    ProductRelationship,
    Software,
    SoftwareType,
    XGenericUri,
)


class SoftwareTestCase(TestCase):
    """Includes some Software model tests."""

    def test_create(self):
        """Creates a single software."""
        manufacturer = Manufacturer.objects.create(
            name='Manufacturer', slug='manufacturer'
        )
        software_type = SoftwareType.objects.create(
            name="Software Type", manufacturer=manufacturer
        )
        software = Software.objects.create(
            name="TSoft2", software_type=software_type
        )
        self.assertEqual(software.name, "TSoft2")
        self.assertEqual(Software.objects.count(), 1)

    def test_software_type_must_not_be_null(self):
        """Checks the non-null contraint on software_type."""
        with self.assertRaises(IntegrityError) as exc:
            Software.objects.create(name="TSoft1")
        self.assertIn(
            'null value in column "software_type_id" of relation '
            '"d3c_software" violates not-null constraint',
            str(exc.exception))


class SoftwareTypeTestCase(TestCase):
    """TODO: SoftwareType"""

    def test_placeholder(self):
        pass


class XGenericUriTestCase(TestCase):
    """TODO: XGenericUri"""

    def test_placeholder(self):
        pass


class HashTestCase(TestCase):
    """TODO: Hash"""

    def test_placeholder(self):
        pass


class FileHashTestCase(TestCase):
    """TODO: FileHash"""

    def test_placeholder(self):
        pass


class ProductRelationshipTestCase(TestCase):
    """TODO: ProductRelationship"""

    def test_placeholder(self):
        pass


class CommunicationTestCase(TestCase):
    """TODO: Communication"""

    def test_placeholder(self):
        pass


class DeviceFindingTestCase(TestCase):
    """TODO: get_matched_device, get_device_by_ip, get_device_by_mac, is_empty"""

    def test_get_matched_device(self):
        pass

    def test_get_device_by_ip(self):
        pass

    def test_get_device_by_mac(self):
        pass

    def test_is_empty(self):
        pass


class CommunicationFindingTestCase(TestCase):
    """TODO: get_matched_device"""

    def test_get_matched_device(self):
        pass


class MappingTestCase(TestCase):
    """TODO: Mapping"""

    def test_placeholder(self):
        pass
