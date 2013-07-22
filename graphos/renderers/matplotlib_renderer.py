#Named such to not clash with matplotlib
from .base import BaseChart

import StringIO
import base64


class BaseMatplotlibChart(BaseChart):

    def get_serieses(self):
        data_only = self.get_data()[1:]
        first_column = [el[0] for el in data_only]
        serieses = []
        for i in range(1, len(self.header)):
            current_column = [el[i] for el in data_only]
            current_series = zip(first_column, current_column)
            serieses.append(current_series)
        return serieses


class LineChart(BaseMatplotlibChart):
    def get_template(self):
        return "graphos/matplotlib_renderer/line_chart.html"

    def get_image(self):
        import numpy as np
        import matplotlib.pyplot as plt
        out = StringIO.StringIO()

        fig = plt.figure()
        ax = fig.add_subplot(111)

        x = np.random.normal(0,1,1000)
        numBins = 50
        ax.hist(x,numBins,color='green',alpha=0.8)
        plt.savefig(out)
        out.seek(0)
        return "data:image/png;base64,%s"%base64.encodestring(out.read())
