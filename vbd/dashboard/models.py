from django.db import models

STATUS_TYPE = [('Shell', 'Shell'), ('Http', 'Http')]

class ServiceStatus():
    name = models.CharField(max_length=60, blank=False, null=False, unique=True)
    

class OperationGroup(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, unique=True)
    
    class Meta:
        db_table = 'operation_group'
    
    def __unicode__(self):
        return 'id:{}, name:{}'.format(self.id, self.name)

class BasicOperation(models.Model):
    name = models.CharField(max_length=512, blank=False, null=False)
    start_command = models.CharField(max_length=512, blank=True, null=True)
    stop_command = models.CharField(max_length=512, blank=True, null=True)
    status_command = models.CharField(max_length=512, blank=True, null=True)
    status_flag = models.BooleanField(default=False)
    status_command_type = models.CharField(max_length=100, choices=STATUS_TYPE, blank=False, null=False, default=STATUS_TYPE[-1][0])
    timeout = models.IntegerField(blank=False, null=False, default=120)
    short_description = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return 'id:{}, name:{}, start_command:{}, stop_command:{}, status_command:{}, status_command_type:{}, status_flag:{}'\
                    .format(self.id, self.name, self.start_command, self.stop_command, self.status_command, self.status_command_type, self.status_flag)

class Operation(BasicOperation):
    deploy_command = models.CharField(max_length=512, blank=True, null=True)
    group = models.ForeignKey(OperationGroup)
    
    class Meta:
        db_table = 'operation'
        
    def __unicode__(self):
        return 'id:{}, name:{}, start_command:{}, stop_command:{}, status_command:{}, status_command_type:{}, status_flag:{}, deploy_command:{}, group:{}'\
                    .format(self.id, self.name, self.start_command, self.stop_command, self.status_command, self.status_command_type, self.status_flag, self.deploy_command, self.group.name)


# Create your models here.
class VEXVersion(models.Model):
    version = models.CharField(max_length=100, blank=False, null=False, unique=True)
    
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