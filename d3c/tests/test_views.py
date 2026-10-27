from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site, Platform
from django.contrib.messages import ERROR, get_messages
from ipam.models import Service
from utilities.testing import ModelViewTestCase, TestCase, create_tags

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

class FindingImportViewTestCase(TestCase):
    """
    Checks the FindingImportView with validate and submit calls.
    """

    def _post_data(self, **update):
        data_file = SimpleUploadedFile(
            "test.txt",
            """mac_address,ip_address,device_role,manufacturer,device_family,confidence,source
00:01:e6:44:19:ff,,IODevice2,Packard,SPS-5001,0.067,IPadded
,127.0.0.1,IODevice2,Packard,SPS-5001,0.067,IPadded""".encode("utf-8"),
            content_type="text/plain"
        )
        data = {
            "data_file": data_file,
            "file_name": "test.txt",
            "format": "csv",
            "csv_delimiter": "auto",
            "step_field": "1",
            "submit_button": "data_validate",
            "data_string":"""mac_address,ip_address,device_role,manufacturer,device_family,confidence,source
00:01:e6:44:19:ff,,IODevice2,Packard,SPS-5001,0.067,IPadded
,127.0.0.1,IODevice2,Packard,SPS-5001,0.067,IPadded"""  ,
        }
        data.update(update)
        return data

    def test_validate_and_submit_with_rawdata(self):
        """
        Calls validate and submit with correct rawdata and check if findings
        are created in the end.
        """
        response = self.client.get(reverse("plugins:d3c:devicefinding_import"))
        self.assertHttpStatus(response, 200)
        self.assertContains(response, "Importing DeviceFindings")
        response = self.client.post(
            reverse("plugins:d3c:devicefinding_import"),
            self._post_data()
        )
        self.assertHttpStatus(response, 200)
        self.assertContains(response, "{confidence}")
        response = self.client.post(
            reverse("plugins:d3c:devicefinding_import"),
            self._post_data(submit_button="data_submit", data_string="""mac_address,ip_address,device_role,manufacturer,device_family,confidence,source
00:01:e6:44:19:ff,,IODevice2,Packard,SPS-5001,0.067,IPadded
,127.0.0.1,IODevice2,Packard,SPS-5001,0.067,IPadded""",
                source="{source}",
                ip_address="{ip_address}",
                mac_address="{mac_address}",
                confidence="{confidence}"
            )
        )
        self.assertHttpStatus(response, 302)
        self.assertTrue(models.DeviceFinding.objects.all().exists())

    def test_validate_and_submit_with_errors(self):
        """
        Calls validate and submit with data without IP/MAC address and check if
        errors are displayed.
        """
        data_string = """mac_address,ip_address,device_role,manufacturer,device_family,confidence,source
,127.0.0.1,IODevice3,Packard,SPS-5001,0.090,IPadded
,,IODevice3,Packard,SPS-5001,0.067,IPadded
"""

        data_file = SimpleUploadedFile(
            "test.txt",
            data_string.encode("utf-8"),
            content_type="text/plain"
        )
        response = self.client.get(reverse("plugins:d3c:devicefinding_import"))
        self.assertHttpStatus(response, 200)
        self.assertContains(response, "Importing DeviceFindings")
        response = self.client.post(
            reverse("plugins:d3c:devicefinding_import"),
            self._post_data(data_file=data_file, data_string=data_string)
        )
        self.assertHttpStatus(response, 200)
        self.assertContains(response, "test.txt")
        data_file = SimpleUploadedFile(
            "test.txt",
            data_string.encode("utf-8"),
            content_type="text/plain"
        )
        data = self._post_data(
            submit_button="data_submit",
            data_file=data_file,
            data_string=data_string,
            source="{source}",
            mac_address="{mac_address}",
            ip_address="{ip_address}",
            confidence="{confidence}",
            device_family="{device_family}"
        )
        response = self.client.post(
            reverse("plugins:d3c:devicefinding_import"),
            data
        )
        self.assertHttpStatus(response, 200)
        self.assertFalse(models.DeviceFinding.objects.all().exists())
        self.assertContains(response, "Error in create Device Finding in line 2")
