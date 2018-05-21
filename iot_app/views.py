from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

# Create your views here.

class IndexView(TemplateView):
    template_name = 'iot_app/index.html'


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'iot_app/generic-form.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'iot_app/profile.html'
