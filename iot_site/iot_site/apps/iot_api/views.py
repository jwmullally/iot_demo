from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from influxdb import InfluxDBClient
from rest_framework import filters, mixins, views, viewsets
from rest_framework.response import Response

from . import serializers
from ..iot_app import models

# Create your views here.

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
    serializer_class = serializers.DeviceSerializer

    def get_queryset(self):
        return models.Device.objects.filter(user=self.request.user)


class DevicePrefsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    """
    API endpoint that allows DevicePrefs to be viewed and updated
    """
    serializer_class = serializers.DevicePrefsSerializer

    def get_queryset(self):
        return models.DevicePrefs.objects.filter(device__user=self.request.user)


class QueryView(views.APIView):
    """
    API endpoint to fetch Device metrics

    Params::
        ?device: Serial of the device(s) to query. Required
        ?sensor: Sensor(s) to query. If unspecified, all sensors will be returned.

    Example::
        ?device=1001&device=1002
        ?device=1001&sensor=a
    """

    QUERY_FORMAT = 'SELECT "value" FROM "iot_metrics"."autogen"."sensor" WHERE time > now() - 5m {serial_query} {sensor_query} GROUP BY "serial", "sensor"'

    def __gen_query(self, devices, sensors):
        # Proof of concept, replace with a query builder or token+AST string builder
        serial_query = 'AND (' + ' OR '.join('"serial"=\'{}\''.format(device.pk) for device in devices) + ')'
        if sensors:
            sensor_query = 'AND (' + ' OR '.join('"sensor"=\'{}\''.format(sensor.tag) for sensor in sensors) + ')'
        else:
            sensor_query = ''
        query = self.QUERY_FORMAT.format(serial_query=serial_query, sensor_query=sensor_query)
        return query

    def get(self, request, format=None):
        device_pks = tuple(request.query_params.getlist('device'))
        if not device_pks:
            return Response({})
        devices = models.Device.objects.filter(user=self.request.user, pk__in=device_pks)
        if not devices:
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
        query = self.__gen_query(devices, sensors)
        data = client.query(query)
        return Response(data.raw)
