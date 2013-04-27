from django.db import models


class TimeSeries(models.Model):
    """
    value is used as y axis for the graph
    """
    value = models.IntegerField()
