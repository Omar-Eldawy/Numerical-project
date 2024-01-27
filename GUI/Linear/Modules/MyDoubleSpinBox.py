from PyQt6 import QtCore
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QDoubleSpinBox
from PyQt6.QtCore import Qt


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
