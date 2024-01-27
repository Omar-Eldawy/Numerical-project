import sys

from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

from GUI.Linear.LinearMethods import LinearOptions
from GUI.NonLinear.NonLinearMethods import NonLinearOptions


class HomePage(QDialog):

    def __init__(self, widget):
        super(HomePage, self).__init__()
        loadUi("designs/home.ui", self)
        self.nonlinearButton.clicked.connect(self.goToNonLinear)
        self.linearButton.clicked.connect(self.goToLinear)
        self.exitButton.clicked.connect(self.exitProgram)
        self.widget = widget

    def goToNonLinear(self):
        nonlinearPage = NonLinearOptions(self.widget)
        self.widget.addWidget(nonlinearPage)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goToLinear(self):
        linearPage = LinearOptions(self.widget)
        self.widget.addWidget(linearPage)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def exitProgram(self):
        sys.exit()

