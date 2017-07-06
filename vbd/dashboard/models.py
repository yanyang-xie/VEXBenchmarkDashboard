from django.db import models

SERVICE_STATUS_TYPE = [('Shell', 'Shell'), ('Http', 'Http')]
SERVICE_STATUS_FLAG = [(True, 'Running'), (False, 'Stopped')]
SERVICE_STATUS_FLAG_DICT = {True:'Running', False: 'Stopped'}

# By default, all the vex component has same version, but also can has its special version 
class VEXVersion(models.Model):
    version = models.CharField(max_length=100, blank=False, null=False, unique=True)
    
    # the default vex version for deployment
    is_default = models.BooleanField(default=True)
    
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

class ServiceStatus(models.Model):
    status_cmd = models.CharField(max_length=512, blank=False, null=False, default="1234")
    status_cmd_type = models.CharField(max_length=100, choices=SERVICE_STATUS_TYPE, blank=False, null=False, default=SERVICE_STATUS_TYPE[-1][0])
    status_cmd_timeout = models.IntegerField(blank=False, null=False, default=120)
    status_flag = models.BooleanField(choices=SERVICE_STATUS_FLAG, blank=False, null=False, default=SERVICE_STATUS_FLAG[-1][0])
    
    # store the response message from status CMD
    status_response = models.CharField(max_length=1024, blank=True, null=True)
    
    class Meta:
        db_table = 'service_status'
    
    def __unicode__(self):
        return 'id:{}, status:[cmd:{}, cmd_type:{}, cmd_timeout:{}, flag:{}, response:{}]'\
                .format(self.id, self.status_cmd, self.status_cmd_type, self.status_cmd_timeout, self.status_flag, self.status_response)

class OperationGroup(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, unique=True)
    sort_key = models.IntegerField(blank=False, null=False, unique=True)
    
    class Meta:
        db_table = 'operation_group'
        ordering = ['-sort_key', ]
    
    def __unicode__(self):
        return 'id:{}, name:{}, sore_key:{}'.format(self.id, self.name, self.sort_key)

class BasicOperation(models.Model):
    name = models.CharField(max_length=512, blank=False, null=False)
    start_command = models.CharField(max_length=512, blank=True, null=True)
    stop_command = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    status = models.OneToOneField(ServiceStatus, blank=True, null=True)
    
    def delete(self, using=None):
        if self.status is not None:
            self.status.delete()
        models.Model.delete(self, using=using)

    class Meta:
        abstract = True
        
    def __unicode__(self):
        return 'id:{}, name:{}, start_command:{}, stop_command:{}, status:{}'\
                .format(self.id, self.name, self.start_command, self.stop_command, self.status)

class Operation(BasicOperation):
    group = models.ForeignKey(OperationGroup,blank=True, null=True)
    
    class Meta:
        db_table = 'operation'
    
    def __unicode__(self):
        return 'id:{}, name:{}, start_command:{}, stop_command:{}, status:{}, group:{}'\
                .format(self.id, self.name, self.start_command, self.stop_command, self.status, self.group)

class VEXOperation(BasicOperation):
    deploy_command = models.CharField(max_length=512, blank=False, null=False)
    deploy_version = models.ForeignKey(VEXVersion, null=True, blank=True)
    
    # get status info from vex components, parse build info and running version from response of status 
    build_info = models.CharField(max_length=512, blank=True, null=True)
    running_version = models.CharField(max_length=512, blank=True, null=True)
    
    class Meta:
        db_table = 'vex_operation'
        
    def __unicode__(self):
        return 'id:{}, name:{}, start_command:{}, stop_command:{}, status:{}, deploy_command:{}, deploy_version:{}, build_info:{}, running_version'\
                .format(self.id, self.name, self.start_command, self.stop_command, self.status, self.deploy_command, self.deploy_version, self.build_info, self.running_version)

class VEXGolbalSettings(models.Model):
    kubectl_ip_address = models.GenericIPAddressField(max_length=100, blank=True, null=True)
    grafana_http_address = models.CharField(max_length=128, blank=True, null=True)
    
    # whether all the vex components use same version
    use_default_version = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'vex_global_settings'
    
    def __unicode__(self):
        return 'kubectl_address:{}, grafana_address:{}, use_default_version:{}'.format(self.kubectl_ip_address, self.grafana_http_address, self.use_default_version)