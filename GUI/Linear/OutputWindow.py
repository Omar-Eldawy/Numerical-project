import math
import time

from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

from GUI.Linear.Modules.MyLabel import Label
from Logic.Linear.Linear_Direct_Methods import LinearSolver
from Logic.Linear.Linear_Iterative_Methods import IterativeMethods


def round_to_significant_digit(num, significant):
    if num == 0:
        return 0
    else:
        x = round(num, -int(math.floor(math.log10(abs(num)))) + (significant - 1))
        return x


class SolutionWindow(QDialog):
    def __init__(self, A, b, operation, tol=0, max_iter=0, x0=None, significantDigits=9, widget=None):
        super(SolutionWindow, self).__init__()
        loadUi("designs/linearOutputWindow.ui", self)
        direct = ["Gauss Jordan", "Gauss Elimination", "Doolittle Form", "Crout Form", "Cholesky Form"]
        self.widget = widget
        self.previousButton.clicked.connect(self.go_to_previous)
        self.noSolutionLabel.hide()
        self.A = A
        self.b = b
        self.operation = operation
        self.tol = tol
        self.max_iter = max_iter
        self.x0 = x0
        self.answer = 0
        self.total_time = 0
        self.significantDigits = significantDigits
        self.flag = 0
        self.diverge.hide()
        if self.operation in direct:
            self.direct = LinearSolver(self.A, self.b, significantDigits, self.tableWidget)
        else:
            self.indirect = IterativeMethods(self.A, self.b, self.x0, self.tol, self.max_iter, significantDigits,
                                             self.tableWidget)
        self.show_answer()

    def go_to_previous(self):
        currentIndex = self.widget.currentIndex()
        widgetToRemove = self.widget.currentWidget()
        self.widget.removeWidget(widgetToRemove)
        self.widget.setCurrentIndex(currentIndex - 1)

    def solve(self):
        if self.operation == "Gauss Jordan":
            start = time.perf_counter()
            self.answer = self.direct.gauss_jordan()
        elif self.operation == "Gauss Elimination":
            start = time.perf_counter()
            self.answer = self.direct.gauss_elimination()
        elif self.operation == "Jacobi":
            start = time.perf_counter()
            self.answer, self.flag = self.indirect.jacobi()
        elif self.operation == "Gauss Seidel":
            start = time.perf_counter()
            self.answer, self.flag = self.indirect.gauss_seidel()
        elif self.operation == "Doolittle Form":
            start = time.perf_counter()
            self.answer = self.direct.doolittle()
        elif self.operation == "Crout Form":
            start = time.perf_counter()
            self.answer = self.direct.crout_lu()
        else:
            start = time.perf_counter()
            self.answer = self.direct.cholesky_lu()
        end = time.perf_counter()
        self.total_time = end - start

    def show_answer(self):
        self.solve()
        if isinstance(self.answer, int) and (self.answer == -1 or self.flag == -1):
            self.toggle_visibility()
        elif self.flag == -2:
            self.diverge_window()
            self.timerLabel.setText(f'Time: {self.total_time:.7f} nano seconds')
            for i in range(len(self.A)):
                label = Label().label
                label.setText("X" + str(i))
                label1 = Label().label
                label1.setText(str(round_to_significant_digit(self.answer[i], self.significantDigits)))
                label1.setStyleSheet("font-size: 9px;")
                self.gridLayout_4.addWidget(label, 0, i)
                self.gridLayout_4.addWidget(label1, 1, i)
        else:
            self.timerLabel.setText(f'Time: {self.total_time:.7f} nano seconds')
            for i in range(len(self.A)):
                label = Label().label
                label.setText("X" + str(i))
                label1 = Label().label
                label1.setText(str(round_to_significant_digit(self.answer[i], self.significantDigits)))
                label1.setStyleSheet("font-size: 9px;")
                self.gridLayout_4.addWidget(label, 0, i)
                self.gridLayout_4.addWidget(label1, 1, i)

    def toggle_visibility(self):
        self.noSolutionLabel.show()
        self.guessHolder.hide()
        self.label_4.hide()
        self.timerLabel.hide()
        self.tableWidget.hide()
        self.diverge.hide()

    def diverge_window(self):
        self.noSolutionLabel.hide()
        self.diverge.show()

