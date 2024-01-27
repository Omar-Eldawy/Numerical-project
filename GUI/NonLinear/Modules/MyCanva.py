import matplotlib
import mplcursors
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
matplotlib.use("QtAgg")


class MyCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=0.3, height=0.3, dpi=70):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

    def plot_data(self, x, y, function='y', method=None):
        self.axes.plot(x, y, label="y = " + function)
        if method == "Fixed Point":
            self.axes.plot(x, x, label="y = x")
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("y")
        self.axes.set_title(function)
        self.axes.legend()
        self.axes.grid(True)
        mplcursors.cursor(hover=True)
        self.draw()
