from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

from GUI.NonLinear.BracketingMethods.InputWindow import BracketingInput
from GUI.NonLinear.OpenMethods.InputWindow import OpenMethodsInput


class NonLinearOptions(QDialog):
    def __init__(self, widget):
        super(NonLinearOptions, self).__init__()
        loadUi("designs/nonlinearMethodsWindow.ui", self)
        self.previousButton.clicked.connect(self.go_to_previous)
        self.BisectionButton.clicked.connect(lambda: self.select_method("Bisection"))
        self.FalsePositionButton.clicked.connect(lambda: self.select_method("False Position"))
        self.FixedPointButton.clicked.connect(lambda: self.select_method("Fixed Point"))
        self.OriginalNewtonButton.clicked.connect(lambda: self.select_method("Newton Raphson 1"))
        self.ModifiedNewtonButton.clicked.connect(lambda: self.select_method("Newton Raphson 2"))
        self.SecantButton.clicked.connect(lambda: self.select_method("Secant"))
        self.widget = widget

    def go_to_previous(self):
        currentIndex = self.widget.currentIndex()
        widgetToRemove = self.widget.currentWidget()
        self.widget.removeWidget(widgetToRemove)
        self.widget.setCurrentIndex(currentIndex - 1)

    def select_method(self, method):
        if method == "Bisection":
            inputWindow = BracketingInput("Bisection", self.widget)
        elif method == "False Position":
            inputWindow = BracketingInput("False Position", self.widget)
        elif method == "Fixed Point":
            inputWindow = OpenMethodsInput("Fixed Point", self.widget)
        elif method == "Newton Raphson 1":
            inputWindow = OpenMethodsInput("Newton Raphson 1", self.widget)
        elif method == "Newton Raphson 2":
            inputWindow = OpenMethodsInput("Newton Raphson 2", self.widget)
        elif method == "Secant":
            inputWindow = OpenMethodsInput("Secant", self.widget)
        else:
            return None
        self.widget.addWidget(inputWindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
