import random
from django import template

register = template.Library()


@register.simple_tag
def random_chart_type():
    chart_type = ['line', 'column', 'spline', 'scatter']
    return random.choice(chart_type)
