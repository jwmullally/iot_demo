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


class QueryView(views.APIView):
    """
    API endpoint to fetch UserDevice metrics
    """

    QUERY_FORMAT = 'SELECT "value" FROM "iot_metrics"."autogen"."sensor" WHERE time > now() - 5m {serial_query} {sensor_query} GROUP BY "serial", "sensor"'

    def __gen_query(self, userdevices, sensors):
        # Proof of concept, replace with a query builder or token+AST string builder
        serial_query = 'AND (' + ' OR '.join('"serial"=\'{}\''.format(userdevice.pk) for userdevice in userdevices) + ')'
        if sensors:
            sensor_query = 'AND (' + ' OR '.join('"sensor"=\'{}\''.format(sensor.tag) for sensor in sensors) + ')'
        else:
            sensor_query = ''
        query = self.QUERY_FORMAT.format(serial_query=serial_query, sensor_query=sensor_query)
        return query

    def get(self, request, format=None):
        """
        ?device: Serial of the device(s) to query. Required
        ?sensor: Sensor(s) to query. If unspecified, all sensors will be returned.
        """
        userdevice_pks = tuple(request.query_params.getlist('device'))
        if not userdevice_pks:
            return Response({})
        queryset = models.UserDevice.objects.filter(user=self.request.user)
        userdevices = queryset.filter(pk__in=userdevice_pks)
        if not userdevices:
            raise Http404
        sensor_pks = tuple(request.query_params.getlist('sensor', []))
        if sensor_pks:
            sensors = models.Sensor.objects.filter(pk__in=sensor_pks)
            if not sensors:
                raise Http404
        else:
            sensors = models.Sensor.objects.all()
        client = InfluxDBClient(
                host=settings.INFLUXDB['HOST'],
                port=settings.INFLUXDB['PORT'],
                username=settings.INFLUXDB['USER'],
                password=settings.INFLUXDB['PASSWORD'],
                database=settings.INFLUXDB['DATABASE'])
        query = self.__gen_query(userdevices, sensors)
        data = client.query(query)
        return Response(data.raw)
