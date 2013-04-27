"""Base Plot Data Handler"""


class BaseDataSource(object):

    id = ''
    count = ''
    frequency = ''
    width = ''
    height = ''
    y_max = ''
    color = ''

    def __init__(
            self, id, count=100, frequency=500, width=600,
            height=300, y_max=100, color='#F33', **kwargs):

        self.id = id
        self.count = count
        self.frequency = frequency
        self.width = width
        self.height = height
        self.y_max = y_max
        self.color = color

    def get_data_instance(self):
        pass

    def get_data(self):
        data = {
            'id': self.id,
            'count': self.count,
            'frequency': self.frequency,
            'width': self.width,
            'height': self.height,
            'y_max': self.y_max,
            'color': "'%s'" % self.color,
        }

        return data

    def get_template(self):
        pass

    def get_color(self):
        return "'%s'" % self.color
