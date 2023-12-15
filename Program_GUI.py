import sys
import numpy as np

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QDoubleSpinBox, QGridLayout, QLabel, QVBoxLayout
from PyQt6.uic import loadUi
from PySide6.QtWidgets import QScrollArea


class HomePage(QDialog):

    def __init__(self):
        super(HomePage, self).__init__()
        loadUi("designs/home.ui", self)
        self.nonlinearButton.clicked.connect(self.goToNonLinear)
        self.linearButton.clicked.connect(self.goToLinear)
        self.exitButton.clicked.connect(self.exitProgram)

    def goToNonLinear(self):
        return  # phase 2

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
        inputWindow = InputWindow(self.operations[0])
        widget.addWidget(inputWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToGaussElimination(self):
        inputWindow = InputWindow(self.operations[1])
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
        inputWindow = InputWindow(self.operations[4])
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
        self.maxIteration = 0
        self.tolerance = 0.0
        self.initialGuess = np.array([])
        self.equations = np.array([])
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

    def set_max_iteration(self, x):
        self.maxIteration = x

    def set_tolerance(self, x):
        self.tolerance = x

    def arrange_initial_guess_area(self):
        for i in range(self.numberOfEquations):
            label = Label().label
            label.setText("x" + str(i))
            self.gridLayout_4.addWidget(label, 0, i)
            self.gridLayout_4.addWidget(DoubleSpinBox().doubleSpinBox, 1, i)

    def solve(self):
        return


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
        self.label.setFixedWidth(30)
        self.label.setFixedHeight(30)
        self.label.setStyleSheet("font-size: 16px;"
                                 "color: #652173;"
                                 "border: 1.3px solid ;"
                                 "border-radius: 5px;")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    widget.setGeometry(250, 30, 800, 650)
    widget.setFixedWidth(850)
    widget.setFixedHeight(650)
    mainPage = HomePage()
    widget.addWidget(mainPage)
    widget.show()
    sys.exit(app.exec())
