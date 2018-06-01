from django.urls import path

from . import views

app_name = 'iot_query'
urlpatterns = [
    path('', views.query, name='query'),
]
