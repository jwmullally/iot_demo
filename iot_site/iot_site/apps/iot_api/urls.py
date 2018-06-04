from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('devicemodel', views.DeviceModelViewSet, base_name="devicemodel")
router.register('sensor', views.SensorViewSet, base_name="sensor")
router.register('device', views.DeviceViewSet, base_name="device")
router.register('deviceprefs', views.DevicePrefsViewSet, base_name="deviceprefs")

urlpatterns = [
    path('', include(router.urls)),
    path('query', views.QueryView.as_view(), name='query'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
