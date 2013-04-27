from django import template
from django.shortcuts import render_to_response
from django.template.context import Context

register = template.Library()


@register.simple_tag(name="plot_model_series")
def plot_model_series(id, x_model_name, x_field_name, count=100, y_max=100, frequency=500, width=600, \
                                        height=300, color='#F33'):
    '''
    This is the function used to plot using the templatetag plot_model
    Options
    id : a unique identification for the plot
    x_model_name : name of the model in which data to be plotted is stored
    x_field_name : field to be plotted
    count : number of values to be retrieved
    y_max : maximum y-length
    frequency : Update delay in milliseconds
    width : width of the plot in pixels
    height : height of the plot in pixels
    color : expected color of the plot
    '''

    # setting minimum limits for safegaurding data from mal-usage
    if int(count) > 1000:
        count = 1000  # maximum data items per request limited to 1000
    if frequency < 10:
        frequency = 10  # minimum timedelay between request set to 10 ms
    c = Context({
        'id': id,
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


@register.simple_tag(name="plot_redis_series")
def plot_redis_series(id, server_address, x_list_name, count=100, y_max=100, frequency=500, width=600, \
                                        height=300, color='#F33'):
    '''
    This is the function used to plot using the templatetag plot_model
    Options
    id : a unique identification for the plot
    x_list_name : redis list to be plotted
    count : number of values to be retrieved
    y_max : maximum y-length
    frequency : Update delay in milliseconds
    width : width of the plot in pixels
    height : height of the plot in pixels
    color : expected color of the plot
    '''

    # setting minimum limits for safegaurding data from mal-usage
    if int(count) > 1000:
        count = 1000  # maximum data items per request limited to 1000
    if frequency < 10:
        frequency = 10  # minimum timedelay between request set to 10 ms
    c = Context({
        'id': id,
        'count': count,
        'frequency': frequency,
        'width': width,
        'height': height,
        'x_list_name': x_list_name,
        'server_address': server_address,
        'y_max': y_max,
        'color': "'%s'" % color,
    })
    response = render_to_response('graphos/redis_template.html', context_instance=c)
    return response.content


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
