from django.test import TestCase

from dashboard.models import VEXVersion

class VEXVersionTestCase(TestCase):
    def setUp(self):
        self.test_version_prefix = 'test_case_'

    def test_version_insert(self):
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
