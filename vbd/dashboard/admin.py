from django.contrib import admin

from dashboard.models import VEXVersion, VEXGolbalSettings, ServiceStatus, \
    OperationGroup, BasicOperation, VEXOperation

# Register your models here.
admin.site.register(VEXVersion)
admin.site.register(VEXGolbalSettings)

admin.site.register(ServiceStatus)
admin.site.register(OperationGroup)
admin.site.register(BasicOperation)
admin.site.register(VEXOperation)





