from django.db import models


class TimeSeries(models.Model):
    """
    value is used as y axis for the graph
    """
    value = models.IntegerField()


class Account(models.Model):
    year = models.CharField(max_length=4)
    sales = models.PositiveIntegerField()
    expenses = models.PositiveIntegerField()
    ceo = models.CharField(max_length=10)
    created_on = models.DateTimeField(auto_now_add=True)
