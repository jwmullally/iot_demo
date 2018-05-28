from django.contrib.auth import get_user_model
from rest_framework import filters, viewsets

from . import serializers
from ..iot_app import models

# Create your views here.

class IsOwnerFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class DeviceModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows DeviceModels to be viewed
    """
    queryset = models.DeviceModel.objects.all()
    serializer_class = serializers.DeviceModelSerializer


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Devices to be viewed
    """
    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializer

    def get_queryset(self):
        return super().get_queryset().filter(userdevice__user=self.request.user)


class UserDeviceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows UserDevices to be viewed
    """
    queryset = models.UserDevice.objects.all()
    serializer_class = serializers.UserDeviceSerializer
    filter_backends = (IsOwnerFilterBackend,)
