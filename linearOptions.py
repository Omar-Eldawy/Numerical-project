import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QWidget
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIcon
from homePage import HomePage


class LinearOptions(QDialog, HomePage):

    def __init__(self):
        super(LinearOptions, self).__init__()
        loadUi("designs/linearMethodsWindow.ui", self)
        self.GaussJordanButton.clicked.connect(self.goToGaussJordan)
        self.GaussEliminationButton.clicked.connect(self.goToGaussElimination)
        self.JacobiButton.clicked.connect(self.goToJacobi)
        self.GaussSeidelButton.clicked.connect(self.goToGaussSeidel)
        self.LUButton.clicked.connect(self.goToLU)
        self.previousButton.clicked.connect(self.goToPrevious)

    def goToGaussJordan(self):
        return

    def goToGaussElimination(self):
        return

    def goToJacobi(self):
        return

    def goToGaussSeidel(self):
        return

    def goToLU(self):
        return

    def goToPrevious(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)

# app = QApplication(sys.argv)
# home_page = LinearOptions()
# widget = QtWidgets.QStackedWidget()
# widget.addWidget(home_page)
# widget.setFixedWidth(800)
# widget.setFixedHeight(650)
# widget.setGeometry(250, 30, 800, 700)
# app.setWindowIcon(QIcon("pictures/appIcon.png"))
# app.setApplicationName("Numerical Methods")
# widget.show()
# sys.exit(app.exec())
