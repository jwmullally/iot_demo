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

    def get_object(self, pk):
        try:
            return models.UserDevice.objects.get(pk=pk)
        except models.UserDevice.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        userdevice = self.get_object(pk)
        client = InfluxDBClient('influxdb', port=80, database='iot_metrics')
        query = self.QUERY_FORMAT.format(serial=userdevice.pk)
        data = client.query(query)
        return Response(data.raw['series'])
