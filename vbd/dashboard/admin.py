from django.contrib import admin

from dashboard.models import VEXVersion, VEXGolbalSettings, ServiceStatus, \
    OperationGroup, Operation, VEXOperation, VEXPerfTestOperation, \
    PerfTestResult, PerfTestConfig


# Register your models here.
admin.site.register(VEXVersion)
admin.site.register(VEXGolbalSettings)

admin.site.register(ServiceStatus)
admin.site.register(OperationGroup)
admin.site.register(Operation)
admin.site.register(VEXOperation)

admin.site.register(VEXPerfTestOperation)
admin.site.register(PerfTestResult)
admin.site.register(PerfTestConfig)






