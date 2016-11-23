import json
import sys

from django.template.loader import render_to_string
from ..exceptions import GraphosException
from ..utils import DEFAULT_HEIGHT, DEFAULT_WIDTH, get_random_string, JSONEncoderForHTML
from ..encoders import GraphosEncoder


class BaseChart(object):

    def __init__(self, data_source, html_id=None,
                 width=None, height=None,
                 options=None, encoder=GraphosEncoder,
                 *args, **kwargs):
        """
        : param data_source: :type graphos.sources.base.BaseDataSource subclass instance.
        : param html_id: :type string: Id of the div where you would like chart to be rendered
        : param width: :type integer: Width of the chart div
        : param height: :type integer: Height of the chart div
        """
        self.data_source = data_source
        self.html_id = html_id or get_random_string()
        self.height = height or DEFAULT_HEIGHT
        self.width = width or DEFAULT_WIDTH
        # options could be an object, a list, a dictionary or a nested object or probably anything.
        # Different renderers have different structure for options.
        # Its responsibility of the renderer to read self.options in correct way and to use it in get_js_template.
        self.options = options or {}
        self.header = data_source.get_header()
        self.encoder = encoder
        self.context_data = kwargs

    def get_data(self):
        return self.data_source.get_data()

    def get_data_json(self):
        return json.dumps(self.get_data(), cls=JSONEncoderForHTML)

    def get_options(self):
        options = self.options
        if not 'title' in options:
            options['title'] = "Chart"
        return options

    def get_options_json(self):
        return json.dumps(self.get_options(), cls=JSONEncoderForHTML)

    def get_template(self):
        return 'graphos/as_html.html'

    def get_html_template(self):
        raise GraphosException("Not Implemented")

    def get_js_template(self):
        raise GraphosException("Not Implemented")

    def get_html_id(self):
        return self.html_id

    def get_context_data(self):
        return self.context_data

    def as_html(self):
        context = {
            'html': self.render_html(),
            'js': self.render_js(),
        }
        return render_to_string(self.get_template(), context)

    def render_html(self):
        context = {"chart": self}
        return render_to_string(self.get_html_template(), context)

    def render_js(self):
        context = {"chart": self}
        return render_to_string(self.get_js_template(), context)

    def zip_list(self, *args):
        rv = zip(*args)
        if sys.version_info < (3,0):
            return rv
        return list(rv)
