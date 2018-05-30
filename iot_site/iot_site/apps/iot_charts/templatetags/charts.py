from django import template
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe


CHART_TEMPLATES = 'iot_charts/{}_chart.html'

register = template.Library()


@register.simple_tag
def chart(chart_type, chart_id, data_view, *args):
    """
    Render a chart template using the provided metrics URL for an AJAX fetch.

    Sample usage::

        {% chart 'line' userdevice.pk 'userdevicemetrics-detail' userdevice.pk %}

    """
    data_url = reverse(data_view, args=args)
    template_name = CHART_TEMPLATES.format(chart_type)
    chart_template = template.loader.get_template(template_name)
    context = {
        'chart_id': chart_id,
        'data_url': data_url,
        }
    return mark_safe(chart_template.render(context))
