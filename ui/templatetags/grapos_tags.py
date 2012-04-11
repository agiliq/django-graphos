from django import template
from django.shortcuts import render_to_response
from django.template.context import Context

register = template.Library()


@register.simple_tag(name="plot_model")
def plot_model(x_model_name, y_model_name='', length=100, frequency=500, width=600, height=300):

    c = Context({
        'length': length,
        'frequency': frequency,
    })
    response = render_to_response('graphos/template.html', context_instance=c)
    return response.content
