from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse

from ..iot_app import models


class DeviceModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.DeviceModel
        fields = ('url', 'name')


class SensorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Sensor
        fields = ('url', 'tag')


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Device
        fields = ('url', 'serial', 'model', 'date')


class UserDeviceSerializer(serializers.HyperlinkedModelSerializer):
    device = serializers.HyperlinkedRelatedField(view_name='device-detail', queryset=models.Device.objects.all())

    class Meta:
        model = models.UserDevice
        fields = ('url', 'device', 'date')
