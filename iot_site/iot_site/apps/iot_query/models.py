from django import forms
from django.db import models

from ..iot_app.models import UserDevice, Sensor

# Create your models here.

class QueryForm(forms.Form):
    device = forms.ModelMultipleChoiceField(
            queryset = UserDevice.objects.none(),
            widget = forms.CheckboxSelectMultiple,
            )
    sensor = forms.ModelMultipleChoiceField(
            queryset = Sensor.objects.all(),
            widget = forms.CheckboxSelectMultiple,
            )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['device'].queryset = UserDevice.objects.filter(user=user)
