from django import template
from django.shortcuts import render
from django.urls import reverse


CHART_TEMPLATES = 'iot_charts/{}_chart.html'

register = template.Library()


@register.simple_tag
def chart(chart_type, chart_id, query_params):
    """
    Render a chart template using the provided metrics URL for an AJAX fetch.

    Sample usage::

      {% with "device="|addstr:device.pk as query_params %}
        {% chart 'line' device.pk query_params %}
      {% endwith %}

    """
    data_url = '{}?{}'.format(reverse('query'), query_params)
    template_name = CHART_TEMPLATES.format(chart_type)
    chart_template = template.loader.get_template(template_name)
    context = {
        'chart_id': chart_id,
        'data_url': data_url,
        }
    return chart_template.render(context)
