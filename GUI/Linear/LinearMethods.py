from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

from GUI.Linear.Direct.InputWindow import LinearWindow
from GUI.Linear.Indirect.InputWindow import InputWindow


class LinearOptions(QDialog):

    def __init__(self, widget):
        super(LinearOptions, self).__init__()
        loadUi("designs/linearMethodsWindow.ui", self)
        self.GaussJordanButton.clicked.connect(lambda: self.select_method("Gauss Jordan"))
        self.GaussEliminationButton.clicked.connect(lambda: self.select_method("Gauss Elimination"))
        self.JacobiButton.clicked.connect(lambda: self.select_method("Jacobi"))
        self.SeidelButton.clicked.connect(lambda: self.select_method("Gauss Seidel"))
        self.LUButton.clicked.connect(lambda: self.select_method("LU"))
        self.previousButton.clicked.connect(self.goToPrevious)
        self.operations = ["Gauss Jordan", "Gauss Elimination", "Jacobi", "Gauss Seidel", "LU"]
        self.widget = widget

    def goToPrevious(self):
        currentIndex = self.widget.currentIndex()
        widgetToRemove = self.widget.currentWidget()
        self.widget.removeWidget(widgetToRemove)
        self.widget.setCurrentIndex(currentIndex - 1)

    def select_method(self, method):
        if method == self.operations[0]:
            inputWindow = LinearWindow(self.operations[0], None, self.widget)
        elif method == self.operations[1]:
            inputWindow = LinearWindow(self.operations[1], None, self.widget)
        elif method == self.operations[2]:
            inputWindow = InputWindow(self.operations[2], self.widget)
        elif method == self.operations[2]:
            inputWindow = InputWindow(self.operations[2], self.widget)
        elif method == self.operations[3]:
            inputWindow = InputWindow(self.operations[3], self.widget)
        elif method == self.operations[4]:
            inputWindow = LinearWindow(self.operations[4], self.LUcomboBox.currentText(), self.widget)
        else:
            return None
        self.widget.addWidget(inputWindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
