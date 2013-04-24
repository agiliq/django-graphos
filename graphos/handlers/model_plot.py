""" Model Plot Data Handler"""

from .base_plot import BasePlotDataHandler


class ModelPlotDataHandler(BasePlotDataHandler):

    model_name = ''
    field_name = ''

    def __init__(self, id, model_name, field_name, count, *args, **kwargs):

        self.model_name = model_name
        self.field_name = field_name

        super(ModelPlotDataHandler, self).__init__(
            id, model_name, field_name, count, *args, **kwargs)

    def get_data_instance(self):

        try:

            ct = ContentType.objects.get(model=self.model_name.lower())
            series = ct.model_class().objects.order_by('-id')[:count]

            try:
                t = [float(
                    element.serializable_value(field_name))
                    for element in series]
                t.reverse()
            except ValueError:
                t = 'Non-plottable values in the models.'

        except ContentType.DoesNotExist:
            t = 'Model or Field cannot be found.'

        return t

    def get_data(self):

        data = super(SQLitePlotDataHandler, self).get_data()

        data.update({
            'x_model_name': self.model_name,
            'x_field_name': self.field_name,
        })

        return data

    def get_template(self):

        template = 'graphos/model_template.html'

        return template
