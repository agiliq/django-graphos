from django import template
from django.shortcuts import render_to_response
from django.template.context import Context

register = template.Library()


@register.simple_tag(name="plot")
def plot(chart):
    '''
    '''

    series = chart.get_series_objects_json()
    options = chart.get_options_json()
    template = chart.get_template()

    c = Context({'series': series, 'chart':chart, 'options': options})

    response = render_to_response(template, context_instance=c)

    return response.content
