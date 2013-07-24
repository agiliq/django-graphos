#Named such to not clash with matplotlib
from .base import BaseChart

import StringIO
import base64


class BaseMatplotlibChart(BaseChart):

    def get_template(self):
        return "graphos/matplotlib_renderer/line_chart.html"

    def get_serieses(self):
        data_only = self.get_data()[1:]
        serieses = []
        for i in range(0, len(self.header)):
            current_column = [el[i] for el in data_only]
            serieses.append(current_column)
        return serieses


class LineChart(BaseMatplotlibChart):

    def get_image(self):
        import matplotlib.pyplot as plt
        serieses = self.get_serieses()
        for i in range(1, len(serieses)):
            plt.plot(serieses[0], serieses[i])
        plt.axis("off")
        out = StringIO.StringIO()
        plt.savefig(out)
        out.seek(0)
        return "data:image/png;base64,%s" % base64.encodestring(out.read())


class BarChart(BaseMatplotlibChart):

    def get_image(self):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        serieses = self.get_serieses()
        for i in range(1, len(serieses)):
            ax.bar(serieses[0], serieses[1], 0.35)
        plt.axis("off")
        out = StringIO.StringIO()
        plt.savefig(out)
        out.seek(0)
        return "data:image/png;base64,%s" % base64.encodestring(out.read())
