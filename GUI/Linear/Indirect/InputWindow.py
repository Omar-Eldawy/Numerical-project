import math

import numpy as np
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi


from GUI.Linear.Modules.MyDoubleSpinBox import DoubleSpinBox
from GUI.Linear.Modules.MyLabel import Label
from GUI.Linear.OutputWindow import SolutionWindow
from Logic.Linear.Linear_Iterative_Methods import IterativeMethods


def round_to_significant_digit(num, significant):
    if num == 0:
        return 0
    else:
        x = round(num, -int(math.floor(math.log10(abs(num)))) + (significant - 1))
        return x


class InputWindow(QDialog):
    def __init__(self, operation, widget):
        super(InputWindow, self).__init__()
        loadUi("designs/linearIterativeInputWindow.ui", self)
        self.widget = widget
        self.operation = operation
        self.numberOfEquations = 0
        self.maxIteration = 50
        self.tolerance = 0.0001
        self.initialGuess = 0
        self.equations = 0
        self.B = 0
        self.significantDigits = 9
        self.percisionInput.valueChanged.connect(self.set_significant)
        self.previousButton.clicked.connect(self.go_to_previous)
        self.equationsInput.valueChanged.connect(self.set_number_of_equations)
        self.maxIterationsInput.valueChanged.connect(self.set_max_iteration)
        self.toleranceInput.valueChanged.connect(self.set_tolerance)
        self.solveButton.clicked.connect(self.solve)

    def go_to_previous(self):
        currentIndex = self.widget.currentIndex()
        widgetToRemove = self.widget.currentWidget()
        self.widget.removeWidget(widgetToRemove)
        self.widget.setCurrentIndex(currentIndex - 1)

    def set_significant(self):
        self.significantDigits = self.percisionInput.value()

    def set_number_of_equations(self, x):
        self.numberOfEquations = x
        self.arrange_initial_guess_area()
        self.arrange_equations_input()

    def set_max_iteration(self, x):
        self.maxIteration = x

    def set_tolerance(self, x):
        self.tolerance = x

    def arrange_initial_guess_area(self):
        while self.gridLayout_4.count():
            item = self.gridLayout_4.takeAt(0)
            current = item.widget()
            if current:
                current.deleteLater()

        for i in range(self.numberOfEquations):
            label = Label().label
            label.setText("x" + str(i))
            self.gridLayout_4.addWidget(label, 0, i)
            self.gridLayout_4.addWidget(DoubleSpinBox().doubleSpinBox, 1, i)

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
            msg.setText("Answer is right in front of you :)")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return
        self.store_equations_values()
        self.store_initial_guess_values()
        if self.operation == "Jacobi":
            jacobi = IterativeMethods(self.equations, self.B, self.initialGuess, self.tolerance, self.maxIteration,
                                      self.significantDigits)
            if jacobi.is_diagonally_dominant():
                outputWindow = SolutionWindow(self.equations, self.B, self.operation, self.tolerance, self.maxIteration,
                                              self.initialGuess, self.significantDigits, self.widget)
                self.widget.addWidget(outputWindow)
                self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
            else:
                msg = QMessageBox().question(self, "Warning",
                                             "The matrix is not diagonally dominant do you want to continue ?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)
                if msg == QMessageBox.StandardButton.Yes:
                    outputWindow = SolutionWindow(self.equations, self.B, self.operation, self.tolerance,
                                                  self.maxIteration,
                                                  self.initialGuess, self.significantDigits, self.widget)
                    self.widget.addWidget(outputWindow)
                    self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
                else:
                    return
        elif self.operation == "Gauss Seidel":
            gauss_seidel = IterativeMethods(self.equations, self.B, self.initialGuess, self.tolerance,
                                            self.maxIteration, self.significantDigits)
            if gauss_seidel.is_diagonally_dominant():
                outputWindow = SolutionWindow(self.equations, self.B, self.operation, self.tolerance, self.maxIteration,
                                              self.initialGuess, self.significantDigits, self.widget)
                self.widget.addWidget(outputWindow)
                self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
            else:
                msg = QMessageBox().question(self, "Warning",
                                             "The matrix is not diagonally dominant do you want to continue ?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)
                if msg == QMessageBox.StandardButton.Yes:
                    outputWindow = SolutionWindow(self.equations, self.B, self.operation, self.tolerance,
                                                  self.maxIteration,
                                                  self.initialGuess, self.significantDigits, self.widget)
                    self.widget.addWidget(outputWindow)
                    self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
                else:
                    return
        else:
            pass

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

    def store_initial_guess_values(self):
        self.initialGuess = np.zeros(self.numberOfEquations)
        for i in range(self.numberOfEquations):
            self.initialGuess[i] = round_to_significant_digit(self.gridLayout_4.itemAtPosition(1, i).widget().value(),
                                                              self.significantDigits)

