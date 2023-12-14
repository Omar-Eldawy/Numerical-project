import sys

from PyQt6 import QtWidgets


class ProgramGUI:

    def __init__(self):
        self.home_page = self.create_home_page()
        self.widget = QtWidgets.QStackedWidget()
        self.widget.addWidget(self.home_page)

    def create_home_page(self):
        from homePage import HomePage  # Move the import statement here
        return HomePage()

    @staticmethod
    def getWidget(self):
        return self.widget


program = ProgramGUI()
