from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from django.contrib.messages import ERROR, get_messages
from django.urls import reverse
from ipam.models import Service
from utilities.testing import ModelViewTestCase, TestCase

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


class FindingListForDeviceViewTestCase(TestCase):
    """Applying the service of a finding via the Findings tab of a device."""

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')
        cls.device = Device.objects.create(
            name='Device',
            device_type=DeviceType.objects.create(manufacturer=manufacturer, model='Device Type', slug='device-type'),
            role=DeviceRole.objects.create(name='Role', slug='role'),
            site=Site.objects.create(name='Site', slug='site'),
        )
        cls.finding = models.DeviceFinding.objects.create(source='manual', device=cls.device)

    def apply_service(self, port):
        finding_id = self.finding.pk
        return self.client.post(reverse('dcim:device_findinglistfordeviceview', kwargs={'pk': self.device.pk}), {
            f'id-{finding_id}': 'on',
            f'service-{finding_id}': 'on',
            f'ip_address-{finding_id}': '192.168.1.1',
            f'network_protocol-{finding_id}': 'ipv4',
            f'transport_protocol-{finding_id}': 'udp',
            f'application_protocol-{finding_id}': 'syslog',
            f'port-{finding_id}': port,
        })

    def test_port_as_decimal_number(self):
        response = self.apply_service('514.0')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Service.objects.get(parent_object_id=self.device.pk).port_mappings, ['udp/514'])

    def test_invalid_port_shows_error(self):
        response = self.apply_service('http')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Service.objects.filter(parent_object_id=self.device.pk).exists())
        errors = [str(m) for m in get_messages(response.wsgi_request) if m.level == ERROR]
        self.assertTrue(any('Port must be an integer' in e for e in errors), errors)
