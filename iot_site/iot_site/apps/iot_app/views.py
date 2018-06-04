from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView

from . import models

# Create your views here.

class IndexView(TemplateView):
    template_name = 'iot_app/index.html'


class DeviceListView(ListView):
    model = models.Device
    ordering = ['-date']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class DeviceDetailView(DetailView):
    model = models.Device

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
