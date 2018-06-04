from datetime import date

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class DeviceModel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    tag = models.CharField(max_length=8, primary_key=True)

    def __str__(self):
        return self.tag


class Device(models.Model):
    serial = models.IntegerField(primary_key=True, unique=True)
    model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    user = models.ForeignKey(User, db_index=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{} #{}'.format(self.model, self.serial)


class DevicePrefs(models.Model):
    device = models.OneToOneField(Device, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{} user preferences".format(self.device)
