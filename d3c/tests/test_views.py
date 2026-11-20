from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from django.urls import reverse
from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site, Platform
from django.contrib.messages import ERROR, get_messages
from ipam.models import Service
from utilities.testing import ModelViewTestCase, TestCase, create_tags

from d3c import models
from d3c import views


class DeviceFindingRejectTestCase(ModelViewTestCase):
    """tests DeviceFindingReject"""
    model = models.DeviceFinding

    @classmethod
    def setUpTestData(cls):
        """class method to setup data"""
        manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')
        cls.device = Device.objects.create(
            name='Device',
            device_type=DeviceType.objects.create(
                manufacturer=manufacturer, model='Device Type', slug='device-type'
            ),
            role=DeviceRole.objects.create(name='Role', slug='role'),
            site=Site.objects.create(name='Site', slug='site'),
        )

    def test_get_required_permission(self):
        """test get_required_permission of the view"""
        self.assertEqual(views.DeviceFindingReject().get_required_permission(), 'd3c.edit_DeviceFinding')

    def test_post_with_different_findings(self):
        """creates some DeviceFindings and rejects them."""
        finding1 = models.DeviceFinding.objects.create(source="Manual1")
        finding2 = models.DeviceFinding.objects.create(source="Manual2", device=self.device)

        view = views.DeviceFindingReject()
        request = RequestFactory().post("/", {"pk": [finding1.pk, finding2.pk]})
        request.session = self.client.session
        request._messages = FallbackStorage(request)
        response = view.post(request)
        messages = list(get_messages(request))
        self.assertEqual(str(messages[0]), "2 device findings rejected")
        self.assertHttpStatus(response, 302)


class DeviceFindingSplitTestCase(ModelViewTestCase):
    """tests DeviceFindingSplit"""
    model = models.DeviceFinding

    def test_get_required_permission(self):
        """test get_required_permission of the view"""
        self.assertEqual(views.DeviceFindingMap().get_required_permission(), 'd3c.edit_DeviceFinding')

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

    def test_get(self):
        """calls get method and checks messages."""
        view = views.DeviceFindingLookupView()
        request = RequestFactory().get("/")
        request.session = self.client.session
        request._messages = FallbackStorage(request)
        result = view.get(request)
        messages = list(get_messages(request))
        self.assertEqual(str(messages[0]), "Device Lookup finished")


class DeviceFindingImportViewTestCase(ModelViewTestCase):
    """ Automatic tests for DeviceFinding import"""
    model = models.DeviceFinding

    def test_validate_with_data(self):
        self.add_permissions('d3c.import_devicefinding')
        data = {
            'data_string': (
                'mac_address,ip_address,device_role,manufacturer,device_family,confidence,source\n'
                '00:01:e6:44:19:ff,,IODevice2,Packard,SPS-5001,0.067,IPadded\n'
                ',192.168.10.46,IODevice2,Packard,SPS-5001,0.067,IPadded\n'),
            'format': 'csv',
            'csv_delimiter': 'auto',
            'step_field': 1,
            'submit_button': 'data_validate'
        }
        response = self.client.post(reverse('plugins:d3c:devicefinding_import'), data)
        self.assertContains(response, 'Source:')
        self.assertContains(response, '{source}')
        self.assertContains(response, 'IPadded')
        self.assertContains(response, '{confidence}')

    def test_validate_without_data(self):
        self.add_permissions('d3c.import_devicefinding')
        data = {
            'data_string': 'mac_address,ip_address,device_role,manufacturer,device_family,confidence,source',
            'format': 'csv',
            'csv_delimiter': 'auto',
            'step_field': 1,
            'submit_button': 'data_validate'
        }
        response = self.client.get(reverse('plugins:d3c:devicefinding_import'))
        self.assertHttpStatus(response, 200)
        response = self.client.post(reverse('plugins:d3c:devicefinding_import'), data)
        self.assertContains(response, 'Source:')
        self.assertContains(response, '{source}')
        self.assertNotContains(response, 'IPadded')
        self.assertContains(response, '{confidence}')


class DeviceFindingMapTestCase(TestCase):
    """tests DeviceFindingMap"""

    @classmethod
    def setUpTestData(cls):
        """class method to setup data"""
        manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')
        cls.device = Device.objects.create(
            name='Device',
            device_type=DeviceType.objects.create(
                manufacturer=manufacturer, model='Device Type', slug='device-type'
            ),
            role=DeviceRole.objects.create(name='Role', slug='role'),
            site=Site.objects.create(name='Site', slug='site'),
        )

    def test_get_required_permission(self):
        """test get_required_permission of the view"""
        self.assertEqual(views.DeviceFindingMap().get_required_permission(), 'd3c.edit_DeviceFinding')

    def test_post_with_different_findings(self):
        """creates some DeviceFindings and matches them."""
        finding1 = models.DeviceFinding.objects.create(source="Manual1")
        finding2 = models.DeviceFinding.objects.create(source="Manual2", device=self.device)

        view = views.DeviceFindingMap()
        request = RequestFactory().post("/", {"pk": [finding1.pk, finding2.pk]})
        request.session = self.client.session
        request._messages = FallbackStorage(request)
        result = view.post(request)
        messages = list(get_messages(request))
        self.assertIn("Mapping of record with ID", str(messages[0]))
        self.assertEqual(str(messages[-1]), "Mapped 1 device findings")


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

    def test_hide_empty_columns(self):
        "tests the hideEmptyColumns method."
        view = views.FindingListForDeviceView()
        request = RequestFactory().get("/")
        request.user = get_user_model().objects.get(username="testuser")
        table = view.get_table(models.DeviceFinding.objects.filter(device=self.device), request, False)
        table.setStringNormalizerEnabled(True)
        table.setDevice(self.device)
        view.hideEmptyColumns(table.data, table)
        self.assertFalse(table.columns.columns['service'].visible)
        self.assertFalse(table.columns.columns['software'].visible)

    def test_get(self):
        """tests the get method without htmx. The table part needs the user
        in the request, use existing 'testuser' for it. 'Device' is the name
        for self.device. """
        view = views.FindingListForDeviceView()
        view.kwargs = {"pk": self.device.pk}
        request = RequestFactory().get("/")
        request.user = get_user_model().objects.get(username="testuser")
        request.htmx = None
        response = view.get(request, name="Device")
        self.assertContains(response, f"/dcim/devices/{self.device.pk}")


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

    def _post_data(self, version="rawdata", **update):
        headers = b"mac_address,ip_address,device_role,manufacturer,device_family,confidence,source\n"
        if version == "rawdata":
            data_bytes = headers + b"""00:01:e6:44:19:ff,,IODevice2,Packard,SPS-5001,0.067,IPadded
,127.0.0.1,IODevice2,Packard,SPS-5001,0.067,IPadded"""
        elif version == "reorder_missing_mac":
            data_bytes = headers + b""",127.0.0.1,IODevice3,Packard,SPS-5001,0.090,IPadded
,,IODevice3,Packard,SPS-5001,0.067,IPadded"""
        else:
            raise ValueError("version must be 'rawdata' or 'reorder_missing_mac'")
        data_file = SimpleUploadedFile(
            "test.txt",
            data_bytes,
            content_type="text/plain"
        )
        data = {
            "data_file": data_file,
            "file_name": "test.txt",
            "format": "csv",
            "csv_delimiter": "auto",
            "step_field": "1",
            "submit_button": "data_validate",
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
            self._post_data(submit_button="data_submit",
                source="{source}",
                ip_address="{ip_address}",
                mac_address="{mac_address}",
                confidence="{confidence}"
            )
        )
        self.assertHttpStatus(response, 302)
        self.assertEqual(models.DeviceFinding.objects.count(), 2)

    def test_validate_and_submit_with_errors(self):
        """
        Calls validate and submit with data without IP/MAC address and check if
        errors are displayed.
        """
        response = self.client.get(reverse("plugins:d3c:devicefinding_import"))
        self.assertHttpStatus(response, 200)
        self.assertContains(response, "Importing DeviceFindings")
        response = self.client.post(
            reverse("plugins:d3c:devicefinding_import"),
            self._post_data(version="reorder_missing_mac")
        )
        self.assertHttpStatus(response, 200)
        self.assertContains(response, "test.txt")
        data = self._post_data(
            version="reorder_missing_mac",
            submit_button="data_submit",
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


class XGenericUriEditViewTestCase(ModelViewTestCase):
    """tests XGenericUriEditView"""
    model = models.XGenericUri

    @classmethod
    def setUpTestData(cls):
        """class method to setup data"""
        manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')
        cls.xgenericuri = models.XGenericUri.objects.create(
            namespace="TEST",
            content_object=models.Software.objects.create(name="Origin content type software"),
            uri="file:///tmp/example.json"
        )
        cls.device_type = DeviceType.objects.create(
            manufacturer=manufacturer, model='Device Type', slug='device-type'
        )
        cls.software = models.Software.objects.create(name="TSoftware")

    def test_alter_object_with_devicetype(self):
        """tests alter_object of this class with devicetype"""
        parent = self.device_type
        child =  self.xgenericuri

        request = RequestFactory().get("/", {'devicetype': parent.pk})
        view = views.XGenericUriEditView()

        result = view.alter_object(child, request, tuple(), {})
        self.assertEqual(result.parent, parent)

    def test_alter_object_devicetype_exception_case(self):
        """tests alter_object with missing device type"""
        child =  self.xgenericuri

        request = RequestFactory().get("/", {'devicetype': -1})
        view = views.XGenericUriEditView()

        result = view.alter_object(child, request, tuple(), {})
        self.assertFalse(hasattr(result, "parent"))

    def test_alter_object_with_software(self):
        """tests alter_object of this class with software"""
        parent = self.software
        child =  self.xgenericuri

        request = RequestFactory().get("/", {'software': parent.pk})
        view = views.XGenericUriEditView()

        result = view.alter_object(child, request, tuple(), {})
        self.assertEqual(result.parent, parent)

    def test_alter_object_software_exception_case(self):
        """tests alter_object with missing software"""
        child =  self.xgenericuri

        request = RequestFactory().get("/", {'software': -1})
        view = views.XGenericUriEditView()

        result = view.alter_object(child, request, tuple(), {})
        self.assertFalse(hasattr(result, "parent"))


class ProductRelationshipEditViewTestCase(ModelViewTestCase):
    """tests ProductRelationshipEditView"""
    model = models.ProductRelationship

    @classmethod
    def setUpTestData(cls):
        """class method to setup data"""
        manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')
        cls.device = Device.objects.create(
            name='Device',
            device_type=DeviceType.objects.create(
                manufacturer=manufacturer, model='Device Type', slug='device-type'
            ),
            role=DeviceRole.objects.create(name='Role', slug='role'),
            site=Site.objects.create(name='Site', slug='site'),
        )
        cls.software = models.Software.objects.create(name="TSoftware")
        cls.product_relationship = models.ProductRelationship.objects.create(
            source=models.Software.objects.create(name="Origin Source"),
            destination=models.Software.objects.create(name="Origin Destination")
        )


    def test_alter_object_with_device(self):
        """tests alter_object of this class with device"""
        parent = self.device
        child =  self.product_relationship
        request = RequestFactory().get("/", {'device': parent.pk})
        view = views.ProductRelationshipEditView()
        result = view.alter_object(child, request, tuple(), {})
        self.assertEqual(result.parent, parent)

    def test_alter_object_device_exception_case(self):
        """tests alter_object with missing device"""
        child =  self.product_relationship
        request = RequestFactory().get("/", {'device': -1})
        view = views.ProductRelationshipEditView()
        result = view.alter_object(child, request, tuple(), {})
        self.assertFalse(hasattr(result, "parent"))

    def test_alter_object_with_software(self):
        """tests alter_object of this class with software"""
        parent = self.software
        child =  self.product_relationship
        request = RequestFactory().get("/", {'software': parent.pk})
        view = views.ProductRelationshipEditView()
        result = view.alter_object(child, request, tuple(), {})
        self.assertEqual(result.parent, parent)

    def test_alter_object_software_exception_case(self):
        """tests alter_object with missing software"""
        child =  self.product_relationship
        request = RequestFactory().get("/", {'software': -1})
        view = views.ProductRelationshipEditView()
        result = view.alter_object(child, request, tuple(), {})
        self.assertFalse(hasattr(result, "parent"))
