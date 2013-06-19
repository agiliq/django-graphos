#Named such to not clash with matplotlib
from .base import BaseChart

import StringIO
import base64


class LineChart(BaseChart):
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
