from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.DeviceModel)
admin.site.register(models.Device)
admin.site.register(models.UserDevice)
