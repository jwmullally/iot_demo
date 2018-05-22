from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from . import views

app_name = 'iot_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('devices/', views.UserDeviceListView.as_view(), name='userdevice_list'),
    path('devices/<int:pk>', views.UserDeviceView.as_view(), name='userdevice'),
    path('accounts/register/', views.RegisterUser.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]
