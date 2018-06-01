from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from influxdb import InfluxDBClient
from rest_framework import filters, views, viewsets
from rest_framework.response import Response

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


class SensorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Sensors to be viewed
    """
    queryset = models.Sensor.objects.all()
    serializer_class = serializers.SensorSerializer


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


class UserDeviceMetricsDetail(views.APIView):
    """
    API endpoint to fetch UserDevice metrics
    """

    QUERY_FORMAT = 'SELECT "value" FROM "iot_metrics"."autogen"."sensor" WHERE time > now() - 5m AND "serial"=\'{serial}\' GROUP BY "serial", "sensor"'

    def get(self, request, pk, format=None):
        queryset = models.UserDevice.objects.filter(user=self.request.user)
        try:
            userdevice = queryset.get(pk=pk)
        except models.UserDevice.DoesNotExist:
            raise Http404
        client = InfluxDBClient(
                host=settings.INFLUXDB['HOST'],
                port=settings.INFLUXDB['PORT'],
                username=settings.INFLUXDB['USER'],
                password=settings.INFLUXDB['PASSWORD'],
                database=settings.INFLUXDB['DATABASE'])
        query = self.QUERY_FORMAT.format(serial=userdevice.pk)
        data = client.query(query)
        return Response(data.raw)
