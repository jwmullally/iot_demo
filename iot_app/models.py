from datetime import date

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class DeviceModel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Device(models.Model):
    serial = models.IntegerField(primary_key=True, unique=True)
    model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    def __str__(self):
        return '{} #{}'.format(self.model, self.serial)


class UserDevice(models.Model):
    device = models.OneToOneField(Device, primary_key=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    def __str__(self):
        return "{}'s - {}".format(self.user, self.device)
