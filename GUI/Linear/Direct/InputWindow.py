import math

import numpy as np
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi

from GUI.Linear.Modules.MyDoubleSpinBox import DoubleSpinBox
from GUI.Linear.Modules.MyLabel import Label
from GUI.Linear.OutputWindow import SolutionWindow
from Logic.Linear.Linear_Direct_Methods import LinearSolver


def round_to_significant_digit(num, significant):
    if num == 0:
        return 0
    else:
        x = round(num, -int(math.floor(math.log10(abs(num)))) + (significant - 1))
        return x


class LinearWindow(QDialog):
    def __init__(self, operation, LU="", widget=None):
        super(LinearWindow, self).__init__()
        loadUi("designs/linearDirectInputWindow.ui", self)
        self.widget = widget
        self.numberOfEquations = 0
        self.equations = 0
        self.B = 0
        self.operation = operation
        self.LU = LU
        self.significantDigits = 9
        self.previousButton.clicked.connect(self.go_to_previous)
        self.solveButton.clicked.connect(self.solve)
        self.equationsInput.valueChanged.connect(self.set_number_of_equations)
        self.percisionInput.valueChanged.connect(self.set_significant)

    def go_to_previous(self):
        currentIndex = self.widget.currentIndex()
        widgetToRemove = self.widget.currentWidget()
        self.widget.removeWidget(widgetToRemove)
        self.widget.setCurrentIndex(currentIndex - 1)

    def set_significant(self, x):
        self.significantDigits = x
        print(self.significantDigits)

    def set_number_of_equations(self, x):
        self.numberOfEquations = x
        if x > 0:
            self.arrange_equations_input()
        else:
            while self.gridLayout_6.count():
                item = self.gridLayout_6.takeAt(0)
                current = item.widget()
                if current:
                    current.deleteLater()

    def arrange_equations_input(self):
        while self.gridLayout_6.count():
            item = self.gridLayout_6.takeAt(0)
            current = item.widget()
            if current:
                current.deleteLater()
        label0 = Label().label
        self.gridLayout_6.addWidget(label0, 0, 0)
        for i in range(1, self.numberOfEquations + 1):
            label = Label().label
            label.setText("X" + str(i - 1))
            label1 = Label().label
            label1.setText(str(i - 1))
            self.gridLayout_6.addWidget(label, 0, i)
            self.gridLayout_6.addWidget(label1, i, 0)
        final_label = Label().label
        final_label.setText("b")
        self.gridLayout_6.addWidget(final_label, 0, self.numberOfEquations + 1)
        for i in range(1, self.numberOfEquations + 1):
            for j in range(1, self.numberOfEquations + 2):
                box = DoubleSpinBox().doubleSpinBox
                self.gridLayout_6.addWidget(box, i, j)

    def solve(self):
        if self.numberOfEquations == 0:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("The number of equations must be greater than 0")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return
        elif self.numberOfEquations == 1:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("the Answer is right in front of you :)")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return
        self.store_equations_values()
        if self.operation == "Gauss Jordan":
            outputWindow = SolutionWindow(self.equations, self.B, self.operation, 0, 0, 0, self.significantDigits, self.widget)
        elif self.operation == "Gauss Elimination":
            outputWindow = SolutionWindow(self.equations, self.B, self.operation, 0, 0, 0, self.significantDigits, self.widget)
        else:
            if self.LU == "Doolittle Form":
                outputWindow = SolutionWindow(self.equations, self.B, self.LU, 0, 0, 0, self.significantDigits, self.widget)
            elif self.LU == "Crout Form":
                outputWindow = SolutionWindow(self.equations, self.B, self.LU, 0, 0, 0, self.significantDigits, self.widget)
            else:
                cholesky = LinearSolver(self.equations, self.B)
                if not cholesky.is_positive_definite():
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setText("The matrix is not positive definite")
                    msg.setIcon(QMessageBox.Icon.Critical)
                    msg.exec()
                    return
                outputWindow = SolutionWindow(self.equations, self.B, self.LU, 0, 0, 0, self.significantDigits, self.widget)
        self.widget.addWidget(outputWindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def store_equations_values(self):
        self.equations = np.zeros((self.numberOfEquations, self.numberOfEquations))
        self.B = np.zeros(self.numberOfEquations)
        for i in range(self.numberOfEquations):
            for j in range(self.numberOfEquations):
                self.equations[i][j] = round_to_significant_digit(
                    self.gridLayout_6.itemAtPosition(i + 1, j + 1).widget().value(), self.significantDigits)
        for i in range(self.numberOfEquations):
            self.B[i] = round_to_significant_digit(
                self.gridLayout_6.itemAtPosition(i + 1, self.numberOfEquations + 1).widget().value(),
                self.significantDigits)

