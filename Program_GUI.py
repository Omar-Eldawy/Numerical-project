import math
import sys
import time

import mplcursors
import numpy as np
import sympy.core.numbers

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon

from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QDoubleSpinBox, QGridLayout, QLabel, QMessageBox
from PyQt6.uic import loadUi
from PySide6.QtWidgets import QScrollArea
from numpy import isreal
from sympy import sympify, symbols, I, oo, log, exp, sin, SympifyError, Function, solve, sqrt, cos, tan, Interval, \
    solve_univariate_inequality

import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from Bracketing_Methods import BracketingMethods
from Linear_Direct_Methods import LinearSolver
from Linear_Iterative_Methods import IterativeMethods
from Open_Methods import OpenMethods

matplotlib.use("QtAgg")


def round_to_significant_digit(num, significant):
    if num == 0:
        return 0
    else:
        x = round(num, -int(math.floor(math.log10(abs(num)))) + (significant - 1))
        return x


class HomePage(QDialog):

    def __init__(self):
        super(HomePage, self).__init__()
        loadUi("designs/home.ui", self)
        self.nonlinearButton.clicked.connect(self.goToNonLinear)
        self.linearButton.clicked.connect(self.goToLinear)
        self.exitButton.clicked.connect(self.exitProgram)

    def goToNonLinear(self):
        nonlinearPage = NonLinearOptions()
        widget.addWidget(nonlinearPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToLinear(self):
        linearPage = LinearOptions()
        widget.addWidget(linearPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def exitProgram(self):
        sys.exit()


class LinearOptions(QDialog):

    def __init__(self):
        super(LinearOptions, self).__init__()
        loadUi("designs/linearMethodsWindow.ui", self)
        self.GaussJordanButton.clicked.connect(self.goToGaussJordan)
        self.GaussEliminationButton.clicked.connect(self.goToGaussElimination)
        self.JacobiButton.clicked.connect(self.goToJacobi)
        self.SeidelButton.clicked.connect(self.goToGaussSeidel)
        self.LUButton.clicked.connect(self.goToLU)
        self.previousButton.clicked.connect(self.goToPrevious)
        self.operations = ["Gauss Jordan", "Gauss Elimination", "Jacobi", "Gauss Seidel", "LU"]

    def goToGaussJordan(self):
        inputWindow = LinearWindow(self.operations[0])
        widget.addWidget(inputWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToGaussElimination(self):
        inputWindow = LinearWindow(self.operations[1])
        widget.addWidget(inputWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToJacobi(self):
        inputWindow = InputWindow(self.operations[2])
        widget.addWidget(inputWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToGaussSeidel(self):
        inputWindow = InputWindow(self.operations[3])
        widget.addWidget(inputWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToLU(self):
        inputWindow = LinearWindow(self.operations[4], self.LUcomboBox.currentText())
        widget.addWidget(inputWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToPrevious(self):
        currentIndex = widget.currentIndex()
        widgetToRemove = widget.currentWidget()
        widget.removeWidget(widgetToRemove)
        widget.setCurrentIndex(currentIndex - 1)


class InputWindow(QDialog):
    def __init__(self, operation):
        super(InputWindow, self).__init__()
        loadUi("designs/inputWindow.ui", self)
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
        currentIndex = widget.currentIndex()
        widgetToRemove = widget.currentWidget()
        widget.removeWidget(widgetToRemove)
        widget.setCurrentIndex(currentIndex - 1)

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
                                              self.initialGuess, self.significantDigits)
                widget.addWidget(outputWindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                msg = QMessageBox().question(self, "Warning",
                                             "The matrix is not diagonally dominant do you want to continue ?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)
                if msg == QMessageBox.StandardButton.Yes:
                    outputWindow = SolutionWindow(self.equations, self.B, self.operation, self.tolerance,
                                                  self.maxIteration,
                                                  self.initialGuess, self.significantDigits)
                    widget.addWidget(outputWindow)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                else:
                    return
        elif self.operation == "Gauss Seidel":
            gauss_seidel = IterativeMethods(self.equations, self.B, self.initialGuess, self.tolerance,
                                            self.maxIteration, self.significantDigits)
            if gauss_seidel.is_diagonally_dominant():
                outputWindow = SolutionWindow(self.equations, self.B, self.operation, self.tolerance, self.maxIteration,
                                              self.initialGuess, self.significantDigits)
                widget.addWidget(outputWindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                msg = QMessageBox().question(self, "Warning",
                                             "The matrix is not diagonally dominant do you want to continue ?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)
                if msg == QMessageBox.StandardButton.Yes:
                    outputWindow = SolutionWindow(self.equations, self.B, self.operation, self.tolerance,
                                                  self.maxIteration,
                                                  self.initialGuess, self.significantDigits)
                    widget.addWidget(outputWindow)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
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


class LinearWindow(QDialog):
    def __init__(self, operation, LU=""):
        super(LinearWindow, self).__init__()
        loadUi("designs/inputWindowLinear.ui", self)
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
        currentIndex = widget.currentIndex()
        widgetToRemove = widget.currentWidget()
        widget.removeWidget(widgetToRemove)
        widget.setCurrentIndex(currentIndex - 1)

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
            outputWindow = SolutionWindow(self.equations, self.B, self.operation, 0, 0, 0, self.significantDigits)
            widget.addWidget(outputWindow)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif self.operation == "Gauss Elimination":
            outputWindow = SolutionWindow(self.equations, self.B, self.operation, 0, 0, 0, self.significantDigits)
            widget.addWidget(outputWindow)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            if self.LU == "Doolittle Form":
                outputWindow = SolutionWindow(self.equations, self.B, self.LU, 0, 0, 0, self.significantDigits)
                widget.addWidget(outputWindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif self.LU == "Crout Form":
                outputWindow = SolutionWindow(self.equations, self.B, self.LU, 0, 0, 0, self.significantDigits)
                widget.addWidget(outputWindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                cholesky = LinearSolver(self.equations, self.B)
                if not cholesky.is_positive_definite():
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setText("The matrix is not positive definite")
                    msg.setIcon(QMessageBox.Icon.Critical)
                    msg.exec()
                    return
                outputWindow = SolutionWindow(self.equations, self.B, self.LU, 0, 0, 0, self.significantDigits)
                widget.addWidget(outputWindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)

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


class SolutionWindow(QDialog):
    def __init__(self, A, b, operation, tol=0, max_iter=0, x0=None, significantDigits=9):
        super(SolutionWindow, self).__init__()
        loadUi("designs/outPutWindow.ui", self)
        direct = ["Gauss Jordan", "Gauss Elimination", "Doolittle Form", "Crout Form", "Cholesky Form"]
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
        currentIndex = widget.currentIndex()
        widgetToRemove = widget.currentWidget()
        widget.removeWidget(widgetToRemove)
        widget.setCurrentIndex(currentIndex - 1)

    def solve(self):
        if self.operation == "Gauss Jordan":
            start = time.perf_counter()
            self.answer = self.direct.gauss_jordan()
            end = time.perf_counter()
            self.total_time = end - start
        elif self.operation == "Gauss Elimination":
            start = time.perf_counter()
            self.answer = self.direct.gauss_elimination()
            end = time.perf_counter()
            self.total_time = end - start
        elif self.operation == "Jacobi":
            start = time.perf_counter()
            self.answer, self.flag = self.indirect.jacobi()
            end = time.perf_counter()
            self.total_time = end - start
        elif self.operation == "Gauss Seidel":
            start = time.perf_counter()
            self.answer, self.flag = self.indirect.gauss_seidel()
            end = time.perf_counter()
            self.total_time = end - start
        elif self.operation == "Doolittle Form":
            start = time.perf_counter()
            self.answer = self.direct.doolittle()
            end = time.perf_counter()
            self.total_time = end - start
        elif self.operation == "Crout Form":
            start = time.perf_counter()
            self.answer = self.direct.crout_lu()
            end = time.perf_counter()
            self.total_time = end - start
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
        # self.widget_2.hide()
        self.label_4.hide()
        self.timerLabel.hide()
        self.tableWidget.hide()
        self.diverge.hide()

    def diverge_window(self):
        self.noSolutionLabel.hide()
        self.diverge.show()


class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        super(DoubleSpinBox, self).__init__()
        self.doubleSpinBox = QDoubleSpinBox()
        self.doubleSpinBox.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.doubleSpinBox.setMinimum(-1e+17)
        self.doubleSpinBox.setMaximum(1e+17)
        self.doubleSpinBox.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.doubleSpinBox.setDecimals(9)
        self.doubleSpinBox.setStyleSheet("""
            QDoubleSpinBox {
                border: 1.3px solid ;
                border-radius: 5px;
                padding: 4px;
                font-size: 10px;
			    background-color:#6e737a;
            }
            QDoubleSpinBox::up-button, QSpinBox::down-button {
                width: 11px;
                height: 11px;
            }
            QDoubleSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
            }
            QDoubleSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
            }
            """)
        self.doubleSpinBox.valueChanged.connect(self.value_changed)

    def value_changed(self):
        pass


class Label(QLabel):
    def __init__(self):
        super(Label, self).__init__()
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedWidth(100)
        self.label.setFixedHeight(30)
        self.label.setStyleSheet("font-size: 16px;"
                                 "color: #652173;"
                                 "border: 1.3px solid ;"
                                 "border-radius: 5px;")


class NonLinearOptions(QDialog):
    def __init__(self):
        super(NonLinearOptions, self).__init__()
        loadUi("designs/nonlinearMethodsWindow.ui", self)
        self.previousButton.clicked.connect(self.go_to_previous)
        self.BisectionButton.clicked.connect(self.go_to_bisection)
        self.FalsePositionButton.clicked.connect(self.go_to_false_position)
        self.FixedPointButton.clicked.connect(self.go_to_fixed_point)
        self.OriginalNewtonButton.clicked.connect(self.go_to_newton_raphson)
        self.ModifiedNewtonButton.clicked.connect(self.go_to_modified_newton)
        self.SecantButton.clicked.connect(self.go_to_secant)

    def go_to_previous(self):
        currentIndex = widget.currentIndex()
        widgetToRemove = widget.currentWidget()
        widget.removeWidget(widgetToRemove)
        widget.setCurrentIndex(currentIndex - 1)

    def go_to_bisection(self):
        inputWindow = BracketingInput("Bisection")
        widget.addWidget(inputWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_false_position(self):
        inputWindow = BracketingInput("False Position")
        widget.addWidget(inputWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_fixed_point(self):
        inputWindow = OpenMethodsInput("Fixed Point")
        widget.addWidget(inputWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_newton_raphson(self):
        inputWindow = OpenMethodsInput("Newton Raphson 1")
        widget.addWidget(inputWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_modified_newton(self):
        inputWindow = OpenMethodsInput("Newton Raphson 2")
        widget.addWidget(inputWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_secant(self):
        inputWindow = OpenMethodsInput("Secant")
        widget.addWidget(inputWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class BracketingInput(QDialog):
    def __init__(self, method):
        super(BracketingInput, self).__init__()
        loadUi("designs/inputWindowBracketing.ui", self)
        self.method = method
        self.previousButton.clicked.connect(self.go_to_previous)
        self.solveButton.clicked.connect(self.solve)
        self.ApplyButton.clicked.connect(self.apply)
        self.editButton.clicked.connect(self.before_function_applied)
        self.toleranceInput.valueChanged.connect(self.set_tolerance)
        self.maxIterationsInput.valueChanged.connect(self.set_max_iteration)
        self.XlInput.valueChanged.connect(self.set_xl)
        self.XuInput.valueChanged.connect(self.set_xu)
        self.pricesionInput.valueChanged.connect(self.set_significant)
        self.symbol = symbols('x')
        self.canva = MyCanvas()
        self.graphArea.addWidget(self.canva)
        self.toolbar = NavigationToolbar(self.canva, self)
        self.toolBarArea.addWidget(self.toolbar, 0, 0)
        self.upperRangeInput.valueChanged.connect(self.set_upper_range)
        self.lowerRangeInput.valueChanged.connect(self.set_lower_range)
        self.updateGraphButton.clicked.connect(self.update_graph)
        self.tolerance = 0.0001
        self.maxIteration = 100
        self.xl = -10.0
        self.xu = 10.0
        self.significantDigits = 16
        self.expression = None
        self.lowerRange = -100
        self.upperRange = 100
        self.before_function_applied()

    def go_to_previous(self):
        currentIndex = widget.currentIndex()
        widgetToRemove = widget.currentWidget()
        widget.removeWidget(widgetToRemove)
        widget.setCurrentIndex(currentIndex - 1)

    def set_tolerance(self, x):
        self.tolerance = x

    def set_max_iteration(self, x):
        self.maxIteration = x

    def set_xl(self, x):
        self.xl = x

    def set_xu(self, x):
        self.xu = x

    def set_significant(self, x):
        self.significantDigits = x

    def set_upper_range(self, x):
        self.upperRange = x

    def set_lower_range(self, x):
        self.lowerRange = x

    def solve(self):
        if self.valid_interval():
            outputWindow = NonlinearOutputWindow(self.method, self.expression, self.tolerance, self.maxIteration,
                                                 self.significantDigits, self.xl, self.xu)
            widget.addWidget(outputWindow)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            return

    def valid_interval(self):
        try:
            fl = self.expression.subs(self.symbol, self.xl).evalf()
            fu = self.expression.subs(self.symbol, self.xu).evalf()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Invalid interval")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return False
        if not self.is_real(fl) or not self.is_real(fu) or fl * fu > 0:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Invalid interval")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return False
        else:
            return True

    def is_real(self, number):
        flag1 = isinstance(number, sympy.core.numbers.Float) or isinstance(number, sympy.core.numbers.Integer)
        return flag1

    def before_function_applied(self):
        self.afterFunction.hide()
        self.solveButton.hide()
        self.editButton.hide()
        self.lineEdit.setEnabled(True)
        self.lowerRange = -100
        self.upperRange = 100
        self.lowerRangeInput.setValue(self.lowerRange)
        self.upperRangeInput.setValue(self.upperRange)
        self.canva.axes.cla()
        self.canva.draw()
        self.ApplyButton.show()

    def apply(self):
        if self.valid_expression():
            self.afterFunction.show()
            self.solveButton.show()
            self.editButton.show()
            self.ApplyButton.hide()
            self.lineEdit.setEnabled(False)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please enter a valid expression")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()

    def generate_data(self, numberOfPoints):
        my_function = lambda x: float(self.expression.subs(self.symbol, x).evalf())
        x_axis = np.linspace(self.lowerRange, self.upperRange, numberOfPoints)
        try:
            y_axis = np.array([my_function(x) for x in x_axis])
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please enter a valid range")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return None, None
        return x_axis, y_axis

    def update_graph(self):
        x_axis, y_axis = self.generate_data(200)
        if x_axis is None:
            return
        self.canva.axes.cla()
        self.canva.plot_data(x_axis, y_axis, self.lineEdit.text())

    def valid_expression(self):
        try:
            test_expression = self.lineEdit.text()
            allowed_variables = set('x')
            expression_symbols = sympify(test_expression).free_symbols
            for symbol in expression_symbols:
                if str(symbol) not in allowed_variables and not isinstance(symbol, Function):
                    return False
            self.expression = sympify(test_expression)
            return True
        except Exception as e:
            return False


class OpenMethodsInput(QDialog):
    def __init__(self, method):
        super(OpenMethodsInput, self).__init__()
        loadUi("designs/inputWindowOpenMethods.ui", self)
        self.previousButton.clicked.connect(self.go_to_previous)
        self.solveButton.clicked.connect(self.solve)
        self.toleranceInput.valueChanged.connect(self.set_tolerance)
        self.maxIterationsInput.valueChanged.connect(self.set_max_iteration)
        self.editButton.clicked.connect(self.before_function_applied)
        self.pricesionInput.valueChanged.connect(self.set_significant)
        self.ApplyButton.clicked.connect(self.apply)
        self.upperRangeInput.valueChanged.connect(self.set_upper_range)
        self.lowerRangeInput.valueChanged.connect(self.set_lower_range)
        self.symbol = symbols('x')
        self.canva = MyCanvas()
        self.graphArea.addWidget(self.canva)
        self.toolbar = NavigationToolbar(self.canva, self)
        self.toolBarArea.addWidget(self.toolbar, 0, 0)
        self.X0Input.valueChanged.connect(self.set_x0)
        self.X1Input.valueChanged.connect(self.set_x1)
        self.mInput.valueChanged.connect(self.set_m)
        self.updateGraphButton.clicked.connect(self.update_graph)
        self.method = method
        self.tolerance = 0.0001
        self.maxIteration = 100
        self.x0 = 10.0
        self.x1 = -10.0
        self.m = 1
        self.significantDigits = 16
        self.expression = None
        self.lowerRange = -100
        self.upperRange = 100
        self.arrange_window_on_method()
        self.before_function_applied()

    def go_to_previous(self):
        currentIndex = widget.currentIndex()
        widgetToRemove = widget.currentWidget()
        widget.removeWidget(widgetToRemove)
        widget.setCurrentIndex(currentIndex - 1)

    def set_tolerance(self, x):
        self.tolerance = x

    def set_max_iteration(self, x):
        self.maxIteration = x

    def set_x0(self, x):
        self.x0 = x

    def set_x1(self, x):
        self.x1 = x

    def set_significant(self, x):
        self.significantDigits = x

    def set_upper_range(self, x):
        self.upperRange = x

    def set_lower_range(self, x):
        self.lowerRange = x

    def set_m(self, x):
        self.m = x

    def arrange_window_on_method(self):
        if self.method == "Secant":
            self.mLabel.hide()
            self.mInput.hide()
        elif self.method == "Newton Raphson 1":
            self.x1Label.hide()
            self.X1Input.hide()
        elif self.method == "Newton Raphson 2" or self.method == "Fixed Point":
            self.mLabel.hide()
            self.mInput.hide()
            self.x1Label.hide()
            self.X1Input.hide()
        else:
            return

    def before_function_applied(self):
        self.afterFunction.hide()
        self.solveButton.hide()
        self.editButton.hide()
        self.lineEdit.setEnabled(True)
        self.lowerRange = -100
        self.upperRange = 100
        self.lowerRangeInput.setValue(self.lowerRange)
        self.upperRangeInput.setValue(self.upperRange)
        self.canva.axes.cla()
        self.canva.draw()
        self.ApplyButton.show()

    def valid_expression(self):
        try:
            test_expression = self.lineEdit.text()
            allowed_variables = set('x')
            expression_symbols = sympify(test_expression).free_symbols
            for symbol in expression_symbols:
                if str(symbol) not in allowed_variables and not isinstance(symbol, Function):
                    return False
            self.expression = sympify(test_expression)
            return True
        except Exception as e:
            return False

    def apply(self):
        if self.valid_expression():
            self.afterFunction.show()
            self.solveButton.show()
            self.editButton.show()
            self.ApplyButton.hide()
            self.lineEdit.setEnabled(False)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please enter a valid expression")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()

    def update_graph(self):
        x_axis, y_axis = self.generate_data(200)
        if x_axis is None:
            return
        self.canva.axes.cla()
        self.canva.plot_data(x_axis, y_axis, self.lineEdit.text(), self.method)

    def generate_data(self, numberOfPoints):
        my_function = lambda x: float(self.expression.subs(self.symbol, x).evalf())
        x_axis = np.linspace(self.lowerRange, self.upperRange, numberOfPoints)
        try:
            y_axis = np.array([my_function(x) for x in x_axis])
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please enter a valid range")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return None, None
        return x_axis, y_axis

    def solve(self):
        if self.method == "Fixed Point":
            first_derivative = self.expression.diff(self.symbol)
            derivative = first_derivative.subs(self.symbol, self.x0).evalf()
            if abs(derivative) >= 1:
                msg = QMessageBox().question(self, "Warning",
                                             "There is no guaranty the method will converge, do you want to continue ?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)
                if msg == QMessageBox.StandardButton.Yes:
                    outputWindow = NonlinearOutputWindow(self.method, self.expression, self.tolerance,
                                                         self.maxIteration,
                                                         self.significantDigits, self.x0, self.x1, self.m)
                    widget.addWidget(outputWindow)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                outputWindow = NonlinearOutputWindow(self.method, self.expression, self.tolerance,
                                                     self.maxIteration,
                                                     self.significantDigits, self.x0, self.x1, self.m)
                widget.addWidget(outputWindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)

        else:
            outputWindow = NonlinearOutputWindow(self.method, self.expression, self.tolerance, self.maxIteration,
                                                 self.significantDigits, self.x0, self.x1, self.m)
            widget.addWidget(outputWindow)
            widget.setCurrentIndex(widget.currentIndex() + 1)


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


class NonlinearOutputWindow(QDialog):
    def __init__(self, method, function, tolerance, max_iterations, precision, xl, xu=-10.0, m=1):
        super(NonlinearOutputWindow, self).__init__()
        loadUi("designs/nonlinearOutPutWindow.ui", self)
        self.method = method
        self.time = 0
        self.previousButton.clicked.connect(self.go_to_previous)
        bracketingMethods = ["Bisection", "False Position"]
        if method in bracketingMethods:
            self.bracketing = BracketingMethods(self.tableWidget, function, xl, xu, tolerance, max_iterations, precision)
        else:
            self.open = OpenMethods(self.tableWidget, function, tolerance, max_iterations, precision, xl, xu, m)
        self.flag = self.solve()
        if self.flag is None:
            self.outputLabel.setText("The method diverged")
        else:
            self.outputLabel.setText("The root value is equal to " + str(self.flag))
        self.timerLabel.setText(f'Time: {self.time:.7f} nano seconds')

    def go_to_previous(self):
        currentIndex = widget.currentIndex()
        widgetToRemove = widget.currentWidget()
        widget.removeWidget(widgetToRemove)
        widget.setCurrentIndex(currentIndex - 1)

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("pictures/icon.jpeg"))
    app.setApplicationName("Numerical Methods")
    app.setApplicationDisplayName("Numerical Methods")
    widget = QtWidgets.QStackedWidget()
    widget.setGeometry(250, 30, 800, 650)
    widget.setFixedWidth(850)
    widget.setFixedHeight(650)
    mainPage = HomePage()
    widget.addWidget(mainPage)
    widget.show()
    sys.exit(app.exec())
