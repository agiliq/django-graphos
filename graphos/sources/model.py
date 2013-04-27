""" Model Plot Data Handler"""
from .simple import SimpleDataSource


def get_field_values(row, fields):
    data = []
    for field in fields:
        data.append(getattr(row, field))
    return data


class ModelDataSource(SimpleDataSource):
    def __init__(self, quertyset, fields=None):
        self.queryset = quertyset
        if fields:
            self.fields = fields
        else:
            self.fields = [el.name for el in self.quertyset.model._meta.fields]
        self.data = self.get_data()

    def get_data(self):
        data = [self.fields]
        for row in self.queryset:
            data.append(get_field_values(row, self.fields))
        return data

    def get_header(self):
        return self.fields
