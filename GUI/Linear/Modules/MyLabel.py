from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


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
