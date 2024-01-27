import sys

from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon

from GUI.HomePage import HomePage


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("pictures/icon.jpeg"))
    app.setApplicationName("Numerical Methods")
    app.setApplicationDisplayName("Numerical Methods")
    widget = QtWidgets.QStackedWidget()
    widget.setGeometry(250, 30, 800, 650)
    widget.setFixedWidth(850)
    widget.setFixedHeight(650)
    mainPage = HomePage(widget)
    widget.addWidget(mainPage)
    widget.show()
    sys.exit(app.exec())
