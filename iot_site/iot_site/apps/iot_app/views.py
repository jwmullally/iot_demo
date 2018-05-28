from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView

from . import models

# Create your views here.

class IndexView(TemplateView):
    template_name = 'iot_app/index.html'


class UserDeviceListView(ListView):
    model = models.UserDevice
    ordering = ['-date']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class UserDeviceView(DetailView):
    model = models.UserDevice

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
