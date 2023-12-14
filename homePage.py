import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QWidget
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIcon

import Program_GUI


class HomePage(QDialog):

    def __init__(self):
        super(HomePage, self).__init__()
        self.linear_options = None
        self.non_linear_options = None
        loadUi("designs/home.ui", self)
        self.nonlinearButton.clicked.connect(self.goToNonLinear)
        self.linearButton.clicked.connect(self.goToLinear)
        self.exitButton.clicked.connect(self.exitProgram)

    def goToNonLinear(self):
        return  # phase 2

    def goToLinear(self):
        self.linear_options = self.create_linear_options()
        Program_GUI.ProgramGUI.getWidget().addWidget(self.linear_options)
        Program_GUI.ProgramGUI.getWidget().setCurrentIndex(Program_GUI.ProgramGUI.getWidget().currentIndex() + 1)

    def create_linear_options(self):
        from linearOptions import LinearOptions  # Move the import statement here
        return LinearOptions()

    def exitProgram(self):
        sys.exit()

    def __main__(self):
        app = QtWidgets.QApplication(sys.argv)
        Program_GUI.ProgramGUI.getWidget().setFixedWidth(800)
        Program_GUI.ProgramGUI.getWidget().setFixedHeight(650)
        Program_GUI.ProgramGUI.getWidget().setGeometry(250, 30, 800, 700)
        Program_GUI.ProgramGUI.getWidget().show()
        sys.exit(app.exec())
