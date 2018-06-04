from django.urls import include, path

from . import views

app_name = 'iot_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('devices/', views.DeviceListView.as_view(), name='device_list'),
    path('devices/<int:pk>', views.DeviceDetailView.as_view(), name='device'),
    path('devices/<int:pk>/prefs', views.DevicePrefsUpdate.as_view(), name='deviceprefs'),
]
