from django.urls import include, path

from . import views

app_name = 'iot_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('devices/', views.UserDeviceListView.as_view(), name='userdevice_list'),
    path('devices/<int:pk>', views.UserDeviceView.as_view(), name='userdevice'),
]
