import numpy as np
import sympy
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi
from sympy import symbols, sympify, Function, Pow, real_root
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from GUI.NonLinear.Modules.MyCanva import MyCanvas
from GUI.NonLinear.OutputWindow import NonlinearOutputWindow


class OpenMethodsInput(QDialog):
    def __init__(self, method, widget):
        super(OpenMethodsInput, self).__init__()
        loadUi("designs/inputWindowOpenMethods.ui", self)
        self.widget = widget
        self.previousButton.clicked.connect(self.go_to_previous)
        self.solveButton.clicked.connect(self.solve)
        self.toleranceInput.valueChanged.connect(self.set_tolerance)
        self.maxIterationsInput.valueChanged.connect(self.set_max_iteration)
        self.editButton.clicked.connect(self.before_function_applied)
        self.pricesionInput.valueChanged.connect(self.set_significant)
        self.ApplyButton.clicked.connect(self.apply)
        self.upperRangeInput.valueChanged.connect(self.set_upper_range)
        self.lowerRangeInput.valueChanged.connect(self.set_lower_range)
        self.symbol = symbols('x')
        self.canva = MyCanvas()
        self.graphArea.addWidget(self.canva)
        self.toolbar = NavigationToolbar(self.canva, self)
        self.toolBarArea.addWidget(self.toolbar, 0, 0)
        self.X0Input.valueChanged.connect(self.set_x0)
        self.X1Input.valueChanged.connect(self.set_x1)
        self.mInput.valueChanged.connect(self.set_m)
        self.updateGraphButton.clicked.connect(self.update_graph)
        self.method = method
        self.tolerance = 0.0001
        self.maxIteration = 100
        self.x0 = 10.0
        self.x1 = -10.0
        self.m = 1
        self.significantDigits = 16
        self.expression = None
        self.lowerRange = -100
        self.upperRange = 100
        self.tempExpression = None
        self.arrange_window_on_method()
        self.before_function_applied()

    def go_to_previous(self):
        currentIndex = self.widget.currentIndex()
        widgetToRemove = self.widget.currentWidget()
        self.widget.removeWidget(widgetToRemove)
        self.widget.setCurrentIndex(currentIndex - 1)

    def set_tolerance(self, x):
        self.tolerance = x

    def set_max_iteration(self, x):
        self.maxIteration = x

    def set_x0(self, x):
        self.x0 = x

    def set_x1(self, x):
        self.x1 = x

    def set_significant(self, x):
        self.significantDigits = x

    def set_upper_range(self, x):
        self.upperRange = x

    def set_lower_range(self, x):
        self.lowerRange = x

    def set_m(self, x):
        self.m = x

    def arrange_window_on_method(self):
        if self.method == "Secant":
            self.mLabel.hide()
            self.mInput.hide()
        elif self.method == "Newton Raphson 1":
            self.x1Label.hide()
            self.X1Input.hide()
        elif self.method == "Newton Raphson 2" or self.method == "Fixed Point":
            self.mLabel.hide()
            self.mInput.hide()
            self.x1Label.hide()
            self.X1Input.hide()
            if self.method == "Fixed Point":
                self.label_4.setText("Enter equation g(x)")
        else:
            return

    def before_function_applied(self):
        self.afterFunction.hide()
        self.solveButton.hide()
        self.editButton.hide()
        self.lineEdit.setEnabled(True)
        self.lowerRange = -100
        self.upperRange = 100
        self.lowerRangeInput.setValue(self.lowerRange)
        self.upperRangeInput.setValue(self.upperRange)
        self.canva.axes.cla()
        self.canva.draw()
        self.ApplyButton.show()

    def valid_expression(self):
        try:
            test_expression = self.lineEdit.text()
            allowed_variables = set('x')
            expression_symbols = sympify(test_expression).free_symbols
            for symbol in expression_symbols:
                if str(symbol) not in allowed_variables and not isinstance(symbol, Function):
                    return False
            self.expression = sympify(test_expression)
            self.tempExpression = self.expression
            self.handle_power()
            return True
        except Exception as e:
            return False

    def apply(self):
        if self.valid_expression():
            self.afterFunction.show()
            self.solveButton.show()
            self.editButton.show()
            self.ApplyButton.hide()
            self.lineEdit.setEnabled(False)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please enter a valid expression")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()

    def update_graph(self):
        x_axis, y_axis = self.generate_data(1000)
        if x_axis is None:
            return
        self.canva.axes.cla()
        self.canva.plot_data(x_axis, y_axis, self.lineEdit.text(), self.method)

    def generate_data(self, numberOfPoints):
        my_function = lambda x: float(self.expression.subs(self.symbol, x).evalf())
        x_axis = np.linspace(self.lowerRange, self.upperRange, numberOfPoints)
        try:
            y_axis = np.array([my_function(x) for x in x_axis])
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please enter a valid range")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return None, None
        return x_axis, y_axis

    def handle_power(self, temp=None):
        if temp is None:
            for expr in sympy.preorder_traversal(self.expression):
                if isinstance(expr, Pow):
                    self.expression = self.expression.replace(expr, real_root(expr.base, 1 / expr.exp))
        else:
            for expr in sympy.preorder_traversal(self.tempExpression):
                if isinstance(expr, Pow):
                    temp = temp.replace(expr, real_root(expr.base, 1 / expr.exp))
            return temp

    def solve(self):
        if self.valid_interval():
            if self.method == "Fixed Point":
                first_derivative = self.tempExpression.diff(self.symbol)
                first_derivative = self.handle_power(first_derivative)
                derivative = first_derivative.subs(self.symbol, self.x0).evalf()
                if abs(derivative) >= 1:
                    msg = QMessageBox().question(self, "Warning",
                                                 "There is no guarantee the method will converge, do you want to continue ?",
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                                 QMessageBox.StandardButton.No)
                    if msg == QMessageBox.StandardButton.Yes:
                        outputWindow = NonlinearOutputWindow(self.method, self.expression, self.tolerance,
                                                             self.maxIteration,
                                                             self.significantDigits, self.x0, self.x1, self.m, self.widget)
                        self.widget.addWidget(outputWindow)
                        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
                else:
                    outputWindow = NonlinearOutputWindow(self.method, self.expression, self.tolerance,
                                                         self.maxIteration,
                                                         self.significantDigits, self.x0, self.x1, self.m, self.widget)
                    self.widget.addWidget(outputWindow)
                    self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

            else:
                outputWindow = NonlinearOutputWindow(self.method, self.expression, self.tolerance, self.maxIteration,
                                                     self.significantDigits, self.x0, self.x1, self.m, self.widget)
                self.widget.addWidget(outputWindow)
                self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        else:
            return

    def valid_interval(self):
        try:
            fl = self.expression.subs(self.symbol, self.x0).evalf()
            fu = 0.0
            if self.method == "Secant":
                fu = self.expression.subs(self.symbol, self.x1).evalf()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Invalid interval")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return False
        if self.method == "Secant":
            if not self.is_real(fl) or not self.is_real(fu):
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Invalid interval")
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.exec()
                return False
            else:
                return True
        else:
            if not self.is_real(fl):
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Invalid interval")
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.exec()
                return False
            else:
                return True

    def is_real(self, number):
        flag1 = isinstance(number, sympy.core.numbers.Float) or isinstance(number,
                                                                           sympy.core.numbers.Integer) or isinstance(
            number, float) or isinstance(number, int)
        return flag1



