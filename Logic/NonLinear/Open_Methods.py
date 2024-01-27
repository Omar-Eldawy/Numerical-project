import math
import sys

import sympy
from PyQt6 import QtWidgets
from sympy import symbols


class OpenMethods:
    def __init__(self, table, function, tolerance, max_iterations, precision, x0, x1=0.0, m=1):
        self.expression = function
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.precision = precision
        self.x = symbols('x')
        self.x0 = x0
        self.x1 = x1
        self.m = m
        self.eps = 10 ** (-10)
        self.table = table
        self.counter = 0
        self.oscillating = [sys.float_info.max, sys.float_info.max]

    def secant(self):
        x0 = self.round_to_significant_digit(self.x0)
        x1 = self.round_to_significant_digit(self.x1)
        x2 = 0.0
        zero_flag = False
        for i in range(0, self.max_iterations):
            data = [x0, x1]
            try:
                fx0 = self.round_to_significant_digit(self.expression.subs(self.x, x0).evalf())
                fx1 = self.round_to_significant_digit(self.expression.subs(self.x, x1).evalf())
                x2 = self.round_to_significant_digit(x1 - self.round_to_significant_digit(fx1 * (x1 - x0))
                                                     / self.round_to_significant_digit((fx1 - fx0)))
                data.append(x2)
                data.append(fx0)
                data.append(fx1)
            except Exception as e:
                print("Zero division error")
                data.append("Infinity")
                self.add_to_table("Secant", data)
                return None, False, i + 1
            if self.is_real(x2):
                try:
                    fx2 = self.round_to_significant_digit(self.expression.subs(self.x, x2).evalf())
                except Exception as e:
                    data.append("Infinity")
                    self.add_to_table("Secant", data)
                    return None, False, i + 1
                if fx2 == 0 or abs(fx2) < self.eps:
                    print("Root found at: ", x2, " number of iterations: ", i + 1)
                    data.append(0.0)
                    self.add_to_table("Secant", data)
                    if x2 < self.eps:
                        return 0, False, i + 1
                    return x2, False, i + 1
                elif x2 == 0 or abs(x2) < self.eps:
                    data.append("Infinity")
                    self.add_to_table("Secant", data)
                    continue
                else:
                    ea = abs((x2 - x1) / x2) * 100.0
                    data.append(ea)
                    if ea < self.tolerance:
                        print("Root found at: ", x2, " number of iterations: ", i + 1)
                        self.add_to_table("Secant", data)
                        return x2, False, i + 1
                    if self.oscillating[i % 2] - x1 == 0.0:
                        print("Root found at: ", x1, " number of iterations: ", i + 1)
                        self.add_to_table("Newton Raphson 1", data)
                        return self.oscillating, True, i + 1
                    self.oscillating[i % 2] = x1
                    # if (ea >= 90 and i >= 30) or x1 >= sys.float_info.max or x1 <= -sys.float_info.max:
                    #     print("diverged")
                    #     self.add_to_table("Secant", data)
                    #     return None, False, i + 1
                self.add_to_table("Secant", data)
                x0 = x1
                x1 = x2
            else:
                print("diverged")
                self.add_to_table("Secant", data)
                return None, False, i + 1
        print("max iterations reached, root is: ", x2)
        return None, False, self.max_iterations

    def newton_raphson_1(self):
        x0 = self.round_to_significant_digit(self.x0)
        x1 = 0.0
        first_derivative = self.expression.diff(self.x)
        for i in range(0, self.max_iterations):
            data = [x0]
            try:
                fx0 = self.round_to_significant_digit(self.expression.subs(self.x, x0).evalf())
                fdx0 = self.round_to_significant_digit(first_derivative.subs(self.x, x0).evalf())
                x1 = self.round_to_significant_digit(x0 - self.m * (fx0 / fdx0))
                data.append(x1)
                data.append(fx0)
                data.append(fdx0)
            except Exception as e:
                print("Zero division error")
                data.append("Infinity")
                self.add_to_table("Newton Raphson 1", data)
                return None, False, i + 1
            if self.is_real(x1):
                try:
                    fx1 = self.round_to_significant_digit(self.expression.subs(self.x, x1).evalf())
                except Exception as e:
                    data.append("Infinity")
                    self.add_to_table("Newton Raphson 1", data)
                    return None, False, i + 1
                if fx1 == 0 or abs(fx1) < self.eps:
                    print("Root found at: ", x1, " number of iterations: ", i + 1)
                    data.append(0.0)
                    self.add_to_table("Newton Raphson 1", data)
                    if x1 < self.eps:
                        return 0, False, i + 1
                    return x1, False, i + 1
                elif x1 == 0 or abs(x1) < self.eps:
                    data.append("Infinity")
                    self.add_to_table("Newton Raphson 1", data)
                    continue
                else:
                    ea = abs((x1 - x0) / x1) * 100.0
                    data.append(ea)
                    if ea < self.tolerance:
                        print("Root found at: ", x1, " number of iterations: ", i + 1)
                        self.add_to_table("Newton Raphson 1", data)
                        return x1, False, i + 1
                    if self.oscillating[i % 2] - x1 == 0.0:
                        print("Root found at: ", x1, " number of iterations: ", i + 1)
                        self.add_to_table("Newton Raphson 1", data)
                        return self.oscillating, True, i + 1
                    self.oscillating[i % 2] = x1
                    # if (ea >= 90 and i >= 30) or x1 >= sys.float_info.max or x1 <= -sys.float_info.max:
                    #     print("diverged")
                    #     self.add_to_table("Newton Raphson 1", data)
                    #     return None, False, i + 1
                self.add_to_table("Newton Raphson 1", data)
                x0 = x1
            else:
                print("diverged")
                self.add_to_table("Newton Raphson 1", data)
                return None, False, i + 1
        return None, False, self.max_iterations

    def newton_raphson_2(self):
        x0 = self.round_to_significant_digit(self.x0)
        x1 = 0.0
        first_derivative = self.expression.diff(self.x)
        second_derivative = first_derivative.diff(self.x)
        for i in range(0, self.max_iterations):
            data = [x0]
            try:
                fx0 = self.round_to_significant_digit(self.expression.subs(self.x, x0).evalf())
                fdx0 = self.round_to_significant_digit(first_derivative.subs(self.x, x0).evalf())
                fddx0 = self.round_to_significant_digit(second_derivative.subs(self.x, x0).evalf())
                x1 = self.round_to_significant_digit(x0 - self.round_to_significant_digit((fx0 * fdx0))
                                                     / (self.round_to_significant_digit(fdx0 ** 2) -
                                                        self.round_to_significant_digit(fx0 * fddx0)))
                data.append(x1)
                data.append(fx0)
                data.append(fdx0)
                data.append(fddx0)
            except Exception as e:
                print("Zero division error")
                data.append("Infinity")
                self.add_to_table("Newton Raphson 2", data)
                return None, False, i + 1
            if self.is_real(x1):
                try:
                    fx1 = self.round_to_significant_digit(self.expression.subs(self.x, x1).evalf())
                except Exception as e:
                    data.append("Infinity")
                    self.add_to_table("Newton Raphson 2", data)
                    return None, False, i + 1
                if fx1 == 0 or abs(fx1) < self.eps:
                    print("Root found at: ", x1, " number of iterations: ", i + 1)
                    data.append(0.0)
                    self.add_to_table("Newton Raphson 2", data)
                    if x1 < self.eps:
                        return 0, False, i + 1
                    return x1, False, i + 1
                elif x1 == 0 or abs(x1) < self.eps:
                    data.append("Infinity")
                    self.add_to_table("Newton Raphson 2", data)
                    continue
                else:
                    ea = abs((x1 - x0) / x1) * 100.0
                    data.append(ea)
                    if ea < self.tolerance:
                        print("Root found at: ", x1, " number of iterations: ", i + 1)
                        self.add_to_table("Newton Raphson 2", data)
                        return x1, False, i + 1
                    if self.oscillating[i % 2] - x1 == 0.0:
                        print("Root found at: ", x1, " number of iterations: ", i + 1)
                        self.add_to_table("Newton Raphson 1", data)
                        return self.oscillating, True, i + 1
                    self.oscillating[i % 2] = x1
                    # if (ea >= 90 and i >= 30) or x1 >= sys.float_info.max or x1 <= -sys.float_info.max:
                    #     print("diverged")
                    #     self.add_to_table("Newton Raphson 2", data)
                    #     return None, False, i + 1
                self.add_to_table("Newton Raphson 2", data)
                x0 = x1
            else:
                print("diverged")
                self.add_to_table("Newton Raphson 2", data)
                return None, False, i + 1
        return None, False, self.max_iterations

    def fixed_point(self):
        x0 = self.round_to_significant_digit(self.x0)
        x1 = 0.0
        for i in range(0, self.max_iterations):
            data = [x0]
            try:
                x1 = self.round_to_significant_digit(self.expression.subs(self.x, x0).evalf())
                data.append(x1)
            except Exception as e:
                print("Zero division error")
                self.add_to_table("Fixed Point", data)
                return None, False, i + 1
            data.append(x1)
            if self.is_real(x1):
                try:
                    fx1 = self.round_to_significant_digit(self.expression.subs(self.x, x1).evalf())
                except Exception as e:
                    data.append("Infinity")
                    self.add_to_table("Fixed Point", data)
                    return None, False, i + 1
                if fx1 == 0 or abs(fx1) < self.eps:
                    print("Root found at: ", x1, " number of iterations: ", i + 1)
                    data.append(0.0)
                    self.add_to_table("Fixed Point", data)
                    if x1 < self.eps:
                        return 0, False, i + 1
                    return x1, False, i + 1
                elif x1 == 0 or abs(x1) < self.eps:
                    data.append("Infinity")
                    self.add_to_table("Fixed Point", data)
                    continue
                else:
                    ea = abs((x1 - x0) / x1) * 100.0
                    data.append(ea)
                    if ea < self.tolerance:
                        print("Root found at: ", x1, " number of iterations: ", i + 1)
                        self.add_to_table("Fixed Point", data)
                        return x1, False, i + 1
                    if self.oscillating[i % 2] - x1 == 0.0:
                        print("Root found at: ", x1, " number of iterations: ", i + 1)
                        self.add_to_table("Fixed Point", data)
                        return self.oscillating, True, i + 1
                    self.oscillating[i % 2] = x1
                self.add_to_table("Fixed Point", data)
                x0 = x1
            else:
                print("diverged")
                data.append("Infinity")
                self.add_to_table("Fixed Point", data)
                return None, False, i + 1
        return None, False, self.max_iterations

    def round_to_significant_digit(self, num):
        if num == 0:
            return 0
        else:
            x = round(num, -int(math.floor(math.log10(abs(num)))) + (self.precision - 1))
            return x

    def is_real(self, number):
        flag1 = isinstance(number, sympy.core.numbers.Float) or isinstance(number,
                                                                           sympy.core.numbers.Integer) or isinstance(
            number, float) or isinstance(number, int)
        return flag1

    def add_to_table(self, method, data):
        column_headers = []
        if method == "Fixed Point":
            column_headers = ["X0", "X1", "ea"]
            self.table.setColumnCount(3)
        elif method == "Newton Raphson 1":
            column_headers = ["X0", "X1", "f(X0)", "f'(X0)", "ea"]
            self.table.setColumnCount(5)
        elif method == "Newton Raphson 2":
            column_headers = ["X0", "X1", "f(X0)", "f'(X0)", "f''(X0)", "ea"]
            self.table.setColumnCount(6)
        elif method == "Secant":
            column_headers = ["X0", "X1", "X2", "f(X0)", "f(X1)", "ea"]
            self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(column_headers)
        self.table.insertRow(self.counter)
        for i in range(len(data)):
            self.table.setItem(self.counter, i, QtWidgets.QTableWidgetItem(str(data[i])))
            self.table.setColumnWidth(i, 200)
        self.counter += 1
