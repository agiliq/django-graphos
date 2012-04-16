from django import template
from django.shortcuts import render_to_response
from django.template.context import Context

register = template.Library()


@register.simple_tag(name="plot_model")
def plot_model(x_model_name, x_field_name, count=100, y_max=100, frequency=500, width=600, \
                                        height=300, color='#F33'):
    '''
    This is the function used to plot using the templatetag plot_model
    Options
    x_model_name : name of the model in which data to be plotted is stored
    x_field_name : field to be plotted
    count : number of values to be retrieved
    y_max : maximum y-length
    frequency : Update delay in milliseconds
    width : width of the plot in pixels
    height : height of the plot in pixels
    color : expected color of the plot
    '''

    c = Context({
        'count': count,
        'frequency': frequency,
        'width': width,
        'height': height,
        'x_model_name': x_model_name,
        'x_field_name': x_field_name,
        'y_max': y_max,
        'color': "'%s'" % color,
    })
    response = render_to_response('graphos/model_template.html', context_instance=c)
    return response.content
