from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from . import models

# Create your views here.

class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'iot_app/generic-form.html'


class UserProfileUpdate(LoginRequiredMixin, UpdateView):
    model = models.UserProfile
    template_name = 'iot_app/generic-form.html'
    fields = ['company', 'address', 'phone_number']

    def get_object(self):
        return models.UserProfile.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse('iot_accounts:profile')
