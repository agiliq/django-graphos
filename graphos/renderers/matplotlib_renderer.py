#Named such to not clash with matplotlib
from .base import BaseChart

from matplotlib.ticker import FormatStrFormatter

import matplotlib.pyplot as plt

try:
    # python 2
    from StringIO import StringIO
except ImportError:
    # python 3
    from io import BytesIO as StringIO

import base64


class BaseMatplotlibChart(BaseChart):

    def get_template(self):
        return "graphos/matplotlib_renderer/line_chart.html"

    def get_serieses(self):
        data_only = self.get_data()[1:]
        serieses = []
        for i in range(0, len(self.header)):
            current_column = [float(el[i]) for el in data_only]
            serieses.append(current_column)
        return serieses


class LineChart(BaseMatplotlibChart):

    def get_image(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        serieses = self.get_serieses()
        for i in range(1, len(serieses)):
            ax.plot(serieses[0], serieses[i])
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        out = StringIO()
        plt.savefig(out)
        out.seek(0)
        return "data:image/png;base64,%s" % base64.encodestring(out.read())


class BarChart(BaseMatplotlibChart):

    def get_image(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        serieses = self.get_serieses()
        for i in range(1, len(serieses)):
            ax.bar(serieses[0], serieses[1], 0.35)
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        out = StringIO()
        plt.savefig(out)
        out.seek(0)
        return "data:image/png;base64,%s" % base64.encodestring(out.read())
