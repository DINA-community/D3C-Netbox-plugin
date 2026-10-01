from django.urls import reverse

from core.models import ObjectType
from dcim.models import DeviceType, Manufacturer, Platform
from users.models import ObjectPermission
from utilities.testing import ModelViewTestCase, create_tags

from d3c import models


class DeviceFindingMapTestCase(ModelViewTestCase):
    """TODO: DeviceFindingMap"""
    model = models.DeviceFinding

    def test_placeholder(self):
        pass


class DeviceFindingRejectTestCase(ModelViewTestCase):
    """TODO: DeviceFindingReject"""
    model = models.DeviceFinding

    def test_placeholder(self):
        pass


class DeviceFindingSplitTestCase(ModelViewTestCase):
    """TODO: DeviceFindingSplit"""
    model = models.DeviceFinding

    def test_placeholder(self):
        pass


class DeviceFindingApplyTestCase(ModelViewTestCase):
    """TODO: DeviceFindingApply"""
    model = models.DeviceFinding

    def test_placeholder(self):
        pass


class DeviceFindingLookupViewTestCase(ModelViewTestCase):
    """TODO: DeviceFindingLookupView"""
    model = models.DeviceFinding

    def test_placeholder(self):
        pass


class CommunicationFindingMapTestCase(ModelViewTestCase):
    """TODO: CommunicationFindingMap"""
    model = models.CommunicationFinding

    def test_placeholder(self):
        pass


class CommunicationFindingRejectTestCase(ModelViewTestCase):
    """TODO: CommunicationFindingReject"""
    model = models.CommunicationFinding

    def test_placeholder(self):
        pass


class DeviceTypeEditViewTestCase(ModelViewTestCase):
    """
    d3c replaces NetBox's DeviceTypeEditView and
    NetBox's own unittests can't be used as they don't know of the Custom Fields.
    """
    model = DeviceType

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name='Manufacturer 1', slug='manufacturer-1')
        cls.platform = Platform.objects.create(name='Platform 1', slug='platform-1')
        cls.tags = create_tags('Alpha', 'Bravo')

    def _post_data(self, **overrides):
        data = {
            'manufacturer': self.manufacturer.pk,
            'cf_device_family': 'DeviceFamily',
            'cf_model_number': 'ModelNumber 1',
            'cf_hardware_name': 'HardwareNumber 1',
        }
        data.update(overrides)
        return data

    def test_create_requires_manufacturer(self):
        self.add_permissions('dcim.add_devicetype')
        data = self._post_data()
        del data['manufacturer']

        response = self.client.post(reverse('dcim:devicetype_add'), data)
        # FIXME check error message

        self.assertHttpStatus(response, 200)
        self.assertFalse(DeviceType.objects.exists())

    def test_create_requires_device_family(self):
        self.add_permissions('dcim.add_devicetype')

        response = self.client.post(reverse('dcim:devicetype_add'), self._post_data(cf_device_family=''))

        self.assertHttpStatus(response, 200)
        self.assertFalse(DeviceType.objects.exists())

    def test_create_only_required(self):
        """ Create a Device Type with only the required fields. """
        self.add_permissions('dcim.add_devicetype')

        response = self.client.post(reverse('dcim:devicetype_add'), self._post_data())

        self.assertHttpStatus(response, 302)
        device_type = DeviceType.objects.get()
        self.assertEqual(device_type.manufacturer, self.manufacturer)
        self.assertEqual(device_type.custom_field_data['device_family'], 'DeviceFamily')

    def test_model_custom_slug(self):
        self.add_permissions('dcim.add_devicetype')

        self.client.post(reverse('dcim:devicetype_add'),
                         self._post_data(cf_hardware_version='1.2', part_number='PN-9'))

        device_type = DeviceType.objects.get()
        self.assertEqual(device_type.model,
                         'DeviceFamily ModelNumber 1 HardwareNumber 1 1.2 PN-9')
