from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('devicemodel', views.DeviceModelViewSet, base_name="devicemodel")
router.register('device', views.DeviceViewSet, base_name="device")
router.register('userdevice', views.UserDeviceViewSet, base_name="userdevice")

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
