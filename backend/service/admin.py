from django.contrib import admin
from .models import DeviceType, Device, Object

admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(Object)


admin.site.site_header = "СТЕК"