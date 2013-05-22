""" Model Plot Data Handler"""
from .simple import SimpleDataSource


def get_field_values(row, fields):
    data = []
    for field in fields:
        data.append(getattr(row, field))
    return data


class ModelDataSource(SimpleDataSource):
    def __init__(self, queryset, fields=None):
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
