from django.urls import include, path

from . import views

app_name = 'iot_accounts'
urlpatterns = [
    path('profile/', views.UserProfileUpdate.as_view(), name='profile'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
]

