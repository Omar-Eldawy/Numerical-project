import sys
import time

import numpy as np

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon

from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QDoubleSpinBox, QGridLayout, QLabel, QMessageBox
from PyQt6.uic import loadUi
from PySide6.QtWidgets import QScrollArea

from Linear_Direct_Methods import LinearSolver
from Linear_Iterative_Methods import IterativeMethods


class HomePage(QDialog):

    def __init__(self):
        super(HomePage, self).__init__()
        loadUi("designs/home.ui", self)
        self.nonlinearButton.clicked.connect(self.goToNonLinear)
        self.linearButton.clicked.connect(self.goToLinear)
        self.exitButton.clicked.connect(self.exitProgram)

    def goToNonLinear(self):
        msg = QMessageBox()
        msg.setWindowTitle("Phase 2")
        msg.setText("Coming Soon :)")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

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
        self.numberOfEquations = 1
        self.maxIteration = 2
        self.tolerance = 0.0001
        self.initialGuess = 0
        self.equations = 0
        self.B = 0
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
        if self.numberOfEquations == 1:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("The number of equations must be greater than 1")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return
        self.store_equations_values()
        self.store_initial_guess_values()
        if self.operation == "Jacobi":
            jacobi = IterativeMethods(self.equations, self.B, self.initialGuess, self.tolerance, self.maxIteration)
            if jacobi.is_diagonally_dominant():
                outputWindow = SolutionWindow(self.equations, self.B, self.operation, self.tolerance, self.maxIteration,
                                              self.initialGuess)
                widget.addWidget(outputWindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("The matrix is not diagonally dominant")
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.exec()

        elif self.operation == "Gauss Seidel":
            gauss_seidel = IterativeMethods(self.equations, self.B, self.initialGuess, self.tolerance,
                                            self.maxIteration)
            if gauss_seidel.is_diagonally_dominant():
                outputWindow = SolutionWindow(self.equations, self.B, self.operation, self.tolerance, self.maxIteration,
                                              self.initialGuess)
                widget.addWidget(outputWindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("The matrix is not diagonally dominant")
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.exec()
        else:
            pass

    def store_equations_values(self):
        self.equations = np.zeros((self.numberOfEquations, self.numberOfEquations))
        self.B = np.zeros(self.numberOfEquations)
        for i in range(self.numberOfEquations):
            for j in range(self.numberOfEquations):
                self.equations[i][j] = self.gridLayout_6.itemAtPosition(i + 1, j + 1).widget().value()
        for i in range(self.numberOfEquations):
            self.B[i] = self.gridLayout_6.itemAtPosition(i + 1, self.numberOfEquations + 1).widget().value()

    def store_initial_guess_values(self):
        self.initialGuess = np.zeros(self.numberOfEquations)
        for i in range(self.numberOfEquations):
            self.initialGuess[i] = self.gridLayout_4.itemAtPosition(1, i).widget().value()


class LinearWindow(QDialog):
    def __init__(self, operation, LU=""):
        super(LinearWindow, self).__init__()
        loadUi("designs/inputWindowLinear.ui", self)
        self.numberOfEquations = 1
        self.equations = 0
        self.B = 0
        self.operation = operation
        self.LU = LU
        self.previousButton.clicked.connect(self.go_to_previous)
        self.solveButton.clicked.connect(self.solve)
        self.equationsInput.valueChanged.connect(self.set_number_of_equations)

    def go_to_previous(self):
        currentIndex = widget.currentIndex()
        widgetToRemove = widget.currentWidget()
        widget.removeWidget(widgetToRemove)
        widget.setCurrentIndex(currentIndex - 1)

    def set_number_of_equations(self, x):
        self.numberOfEquations = x
        self.arrange_equations_input()

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
        if self.numberOfEquations == 1:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("The number of equations must be greater than 1")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return
        self.store_equations_values()
        if self.operation == "Gauss Jordan":
            outputWindow = SolutionWindow(self.equations, self.B, self.operation)
            widget.addWidget(outputWindow)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif self.operation == "Gauss Elimination":
            outputWindow = SolutionWindow(self.equations, self.B, self.operation)
            widget.addWidget(outputWindow)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            if self.LU == "Doolittle Form":
                outputWindow = SolutionWindow(self.equations, self.B, self.LU)
                widget.addWidget(outputWindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif self.LU == "Crout Form":
                outputWindow = SolutionWindow(self.equations, self.B, self.LU)
                widget.addWidget(outputWindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                cholesky = LinearSolver(self.equations, self.B)
                if cholesky.is_singular():
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setText("The matrix is not positive definite")
                    msg.setIcon(QMessageBox.Icon.Critical)
                    msg.exec()
                    return
                outputWindow = SolutionWindow(self.equations, self.B, self.LU)
                widget.addWidget(outputWindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)

    def store_equations_values(self):
        self.equations = np.zeros((self.numberOfEquations, self.numberOfEquations))
        self.B = np.zeros(self.numberOfEquations)
        for i in range(self.numberOfEquations):
            for j in range(self.numberOfEquations):
                self.equations[i][j] = self.gridLayout_6.itemAtPosition(i + 1, j + 1).widget().value()
        for i in range(self.numberOfEquations):
            self.B[i] = self.gridLayout_6.itemAtPosition(i + 1, self.numberOfEquations + 1).widget().value()


class SolutionWindow(QDialog):
    def __init__(self, A, b, operation, tol=0, max_iter=0, x0=None):
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
        if self.operation in direct:
            self.direct = LinearSolver(self.A, self.b)
        else:
            self.indirect = IterativeMethods(self.A, self.b, self.x0, self.tol, self.max_iter)
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
            self.answer = self.indirect.jacobi()
            end = time.perf_counter()
            self.total_time = end - start
        elif self.operation == "Gauss Seidel":
            start = time.perf_counter()
            self.answer = self.indirect.gauss_seidel()
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
            self.answer = self.direct.cholesky_lu(self.A, self.b)
            end = time.perf_counter()
            self.total_time = end - start

    def show_answer(self):
        self.solve()
        if isinstance(self.answer, int) and self.answer == -1:
            self.toggle_visibility()
        else:
            self.timerLabel.setText(f'Time: {self.total_time:.7f} nano seconds')
            for i in range(len(self.A)):
                label = Label().label
                label.setText("X" + str(i))
                label1 = Label().label
                label1.setText(str(round(self.answer[i], 9)))
                label1.setStyleSheet("font-size: 9px;")
                self.gridLayout_4.addWidget(label, 0, i)
                self.gridLayout_4.addWidget(label1, 1, i)

    def toggle_visibility(self):
        self.noSolutionLabel.show()
        self.guessHolder.hide()
        self.widget_2.hide()
        self.label_4.hide()
        self.timerLabel.hide()


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
