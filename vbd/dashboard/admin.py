from django.contrib import admin

from dashboard.models import VEXVersion, VEXGolbalSettings

# Register your models here.
admin.site.register(VEXVersion)
admin.site.register(VEXGolbalSettings)
