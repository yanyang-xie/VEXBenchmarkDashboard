from django.db import models

SERVICE_STATUS_TYPE = [('Shell', 'Shell'), ('Http', 'Http')]
SERVICE_STATUS_FLAG = [('0', 'Running'), ('1', 'Stopped')]

# Create your models here.
class VEXVersion(models.Model):
    version = models.CharField(max_length=100, blank=False, null=False, unique=True)
    
    # the default vex version for deployment
    is_default = models.BooleanField(default=False)
    
    def __unicode__(self):
        return 'id:{}, version:{}, is_default:{}'.format(self.id, self.version, self.is_default)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_default is True:
            VEXVersion.objects.all().update(is_default=False)
        
        super(VEXVersion, self).save(force_insert, force_update, using, update_fields)
    
    class Meta:
        db_table = 'vex_version'
        ordering = ['version', ]
        get_latest_by = 'version'

'''
class ServiceStatus(models.Model):
    status_cmd = models.CharField(max_length=512, blank=True, null=True)
    status_cmd_type = models.CharField(max_length=100, choices=SERVICE_STATUS_TYPE, blank=False, null=False, default=SERVICE_STATUS_TYPE[-1][0])
    status_cmd_timeout = models.IntegerField(blank=False, null=False, default=120)
    status_flag = models.BooleanField(choices=SERVICE_STATUS_TYPE, blank=False, null=False, default=SERVICE_STATUS_FLAG[-1][0])
    
    # store the response message from status CMD
    status_response = models.CharField(max_length=1024, blank=True, null=True)
    
    class Meta:
        db_table = 'service_status'
    
    def __unicode__(self):
        return 'id:{}, status:[cmd:{}, cmd_type:{}, cmd_timeout:{}, flag:{}, response:{}]'\
                .format(self.id, self.status_cmd, self.status_cmd_type, self.status_cmd_timeout, self.status_flag, self.status_response)

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
    description = models.CharField(max_length=1024, blank=True, null=True)
    
    group = models.ForeignKey(OperationGroup)
    status = models.ForeignKey(ServiceStatus, on_delete=models.CASCADE, unique=True)
    
    class Meta:
        db_table = 'operation'

    #class Meta:
    #    abstract = True
        
    def __unicode__(self):
        return 'id:{}, name:{}, start_command:{}, stop_command:{}, status:{}, group:{}'\
                .format(self.id, self.name, self.start_command, self.stop_command, self.status, self.group)

class VEXOperation(BasicOperation):
    deploy_command = models.CharField(max_length=512, blank=True, null=True)
    deploy_version = models.ForeignKey(VEXVersion, null=True, blank=True)
    
    class Meta:
        db_table = 'deploy_operation'
        
    def __unicode__(self):
        return 'id:{}, name:{}, start_command:{}, stop_command:{}, status_command:{}, status_command_type:{}, status_flag:{}, deploy_command:{}, group:{}'\
                    .format(self.id, self.name, self.start_command, self.stop_command, self.status_command, self.status_command_type, self.status_flag, self.deploy_command, self.group.name)
'''

class VEXGolbalSettings(models.Model):
    kubectl_ip_address = models.GenericIPAddressField(max_length=100, blank=True, null=True)
    grafana_http_address = models.CharField(max_length=128, blank=True, null=True)
    
    # whether all the vex components use same version
    use_default_version = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'vex_global_settings'
    
    def __unicode__(self):
        return 'kubectl_address:{}, grafana_address:{}, use_default_version:{}'.format(self.kubectl_address, self.grafana_address, self.use_default_version)