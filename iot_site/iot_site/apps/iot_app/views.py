from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

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


class DevicePrefsUpdate(UpdateView):
    form_class = models.DevicePrefsForm
    template_name = 'iot_app/generic-form.html'

    def get_queryset(self):
        return models.DevicePrefs.objects.filter(device__user=self.request.user)

    def get_success_url(self):
        return reverse('iot_app:device', args=(self.object.device_id,))
