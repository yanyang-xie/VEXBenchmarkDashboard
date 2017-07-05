from django.test import TestCase

from dashboard.models import VEXVersion, ServiceStatus, SERVICE_STATUS_TYPE, \
    BasicOperation


class VEXVersionTestCase(TestCase):
    def setUp(self):
        self.test_version_prefix = 'test_case_'

    def test_version_model(self):
        VEXVersion.objects.create(version=self.test_version_prefix + '1000', is_default=True)
        v1 = VEXVersion.objects.get(version=self.test_version_prefix + '1000')
        self.assertEqual(v1.is_default, True)
        
        VEXVersion.objects.create(version=self.test_version_prefix + '2000', is_default=True)
        v2 = VEXVersion.objects.get(version=self.test_version_prefix + '2000')
        self.assertEqual(v2.is_default, True)
        
        v1 = VEXVersion.objects.get(version=self.test_version_prefix + '1000')
        self.assertEqual(v1.is_default, False)
    
    def tearDown(self):
        VEXVersion.objects.filter(version__startswith='test_case_').delete()

class ServiceStatusTestCase(TestCase):
    def setUp(self):
        self.cmd = 'http://www.baidu.com'
    
    def test_service_status_model(self):
        ServiceStatus.objects.create(status_cmd=self.cmd)
        
        s1 = ServiceStatus.objects.get(status_cmd=self.cmd)
        self.assertEqual(s1.status_cmd_type, SERVICE_STATUS_TYPE[-1][0])
    
    def tearDown(self):
        s1 = ServiceStatus.objects.get(status_cmd=self.cmd)
        s1.delete()

class BasicOperationTestCase(TestCase):
    def setUp(self):
        self.op_name = 'Core VEX'
        self.status_cmd = 'http://www.sina.com'
    
    def test_basic_operation_model(self):
        BasicOperation.objects.create(name=self.op_name)
        b1 = BasicOperation.objects.get(name=self.op_name)
        self.assertEqual(b1.name, self.op_name)
        b1.delete()
        
    def test_basic_operation_delete_model(self):
        s1 = ServiceStatus.objects.create(status_cmd=self.status_cmd)
        
        BasicOperation.objects.create(name=self.op_name, status=s1)
        b1 = BasicOperation.objects.get(name=self.op_name)
        self.assertEqual(b1.name, self.op_name)
        self.assertEqual(b1.status.status_cmd, self.status_cmd)
        
        b1.delete()
        s1 = ServiceStatus.objects.filter(status_cmd=self.status_cmd)
        self.assertEqual(len(s1), 0)
        
        
