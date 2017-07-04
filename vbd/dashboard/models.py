from django.db import models

# Create your models here.
class VEXVersion(models.Model):
    version = models.CharField(max_length=100, blank=False, null=False, unique=True)
    enable = models.BooleanField(default=False)
    
    def __unicode__(self):
        return 'id:{}, version:{}, enable:{}'.format(self.id, self.version, self.enable)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.enable is True:
            VEXVersion.objects.all().update(enable=False)
        
        super(VEXVersion, self).save(force_insert, force_update, using, update_fields)
    
    class Meta:
        db_table = 'vex_version'
        ordering = ['version', ]
        get_latest_by = 'version'

class VEXGolbalSettings(models.Model):
    kubectl_ip_address = models.GenericIPAddressField(max_length=100, blank=True, null=True)
    grafana_http_address = models.CharField(max_length=128, blank=True, null=True)
    
    class Meta:
        db_table = 'vex_global_settings'
    
    def __unicode__(self):
        return 'kubectl_address:{}, grafana_address:{}'.format(self.kubectl_address, self.grafana_address)