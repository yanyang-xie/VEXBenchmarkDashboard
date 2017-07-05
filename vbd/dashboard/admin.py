from django.contrib import admin

from dashboard.models import VEXVersion, VEXGolbalSettings, ServiceStatus, \
    OperationGroup, Operation, VEXOperation

# Register your models here.
admin.site.register(VEXVersion)
admin.site.register(VEXGolbalSettings)

admin.site.register(ServiceStatus)
admin.site.register(OperationGroup)
admin.site.register(Operation)
admin.site.register(VEXOperation)





