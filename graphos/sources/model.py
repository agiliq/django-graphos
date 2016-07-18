""" Model Plot Data Handler"""
from .simple import SimpleDataSource


def get_field_values(row, fields):
    data = []
    for field in fields:
        value = getattr(row, field)
        data.append(value if not callable(value) else value())
    return data


class ModelDataSource(SimpleDataSource):
    """
    Normalizes data contained in a queryset to format usable by renderers
    """
    def __init__(self, queryset, fields=None):
        """
        : param queryset: :type Django ORM queryset
        : param fields: :type  list of strings
        Example usage:
            queryset = Account.objects.all()
            mds = ModelDataSource(queryset, fields=['year', 'sales', 'expenses'])
            # This assumes the following model Account:
            class Account(models.Model):
                year = models.IntegerField()
                sales = models.DecimalField()
                expenses = models.DecimalField()
                profit = models.DecimalField()
        """
        self.queryset = queryset
        if fields:
            self.fields = fields
        else:
            self.fields = [el.name for el in self.queryset.model._meta.fields]
        self.data = self.create_data()

    def create_data(self):
        data = [self.fields]
        for row in self.queryset:
            data.append(get_field_values(row, self.fields))
        return data
