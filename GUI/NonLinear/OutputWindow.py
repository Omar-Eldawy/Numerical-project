import time

from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi
from Logic.NonLinear.Bracketing_Methods import BracketingMethods
from Logic.NonLinear.Open_Methods import OpenMethods


class NonlinearOutputWindow(QDialog):
    def __init__(self, method, function, tolerance, max_iterations, precision, xl, xu=-10.0, m=1, widget=None):
        super(NonlinearOutputWindow, self).__init__()
        loadUi("designs/nonlinearOutPutWindow.ui", self)
        self.widget = widget
        self.method = method
        self.time = 0
        self.oscilating = False
        self.previousButton.clicked.connect(self.go_to_previous)
        bracketingMethods = ["Bisection", "False Position"]
        if method in bracketingMethods:
            self.bracketing = BracketingMethods(self.tableWidget, function, xl, xu, tolerance, max_iterations,
                                                precision)
        else:
            self.open = OpenMethods(self.tableWidget, function, tolerance, max_iterations, precision, xl, xu, m)
        self.flag, self.oscillating, self.numberOfIterations = self.solve()
        if self.flag is None:
            self.outputLabel.setText("The method diverged")
        elif self.oscillating:
            self.outputLabel.setText(f'The method is oscillating around {self.flag[0]} and {self.flag[1]}')
        else:
            self.outputLabel.setText("The root value is equal to " + str(self.flag))
        self.timerLabel.setText(f'Time: {self.time:.7f} nano seconds')
        self.iterationsLabel.setText(f'Number of iterations : {self.numberOfIterations}')

    def go_to_previous(self):
        currentIndex = self.widget.currentIndex()
        widgetToRemove = self.widget.currentWidget()
        self.widget.removeWidget(widgetToRemove)
        self.widget.setCurrentIndex(currentIndex - 1)

    def solve(self):
        if self.method == "Bisection":
            start = time.perf_counter()
            answer = self.bracketing.bisection()
            end = time.perf_counter()
            self.time = end - start
            return answer
        elif self.method == "False Position":
            start = time.perf_counter()
            answer = self.bracketing.false_position()
            end = time.perf_counter()
            self.time = end - start
            return answer
        elif self.method == "Fixed Point":
            start = time.perf_counter()
            answer = self.open.fixed_point()
            end = time.perf_counter()
            self.time = end - start
            return answer
        elif self.method == "Newton Raphson 1":
            start = time.perf_counter()
            answer = self.open.newton_raphson_1()
            end = time.perf_counter()
            self.time = end - start
            return answer
        elif self.method == "Newton Raphson 2":
            start = time.perf_counter()
            answer = self.open.newton_raphson_2()
            end = time.perf_counter()
            self.time = end - start
            return answer
        else:
            start = time.perf_counter()
            answer = self.open.secant()
            end = time.perf_counter()
            self.time = end - start
            return answer
