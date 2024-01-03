import math

from PyQt6 import QtWidgets
from sympy import symbols


class BracketingMethods:
    def __init__(self, table, function, xl, xu, tolerance, max_iterations, precision):
        self.expression = function
        self.xl = xl
        self.xu = xu
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.precision = precision
        self.x = symbols('x')
        self.eps = 10**(-self.precision)
        self.table = table
        self.counter = 0

    def bisection(self):
        fl = self.round_to_significant_digit(self.expression.subs(self.x, self.xl).evalf())
        fu = self.round_to_significant_digit(self.expression.subs(self.x, self.xu).evalf())
        xr_old = 0.0
        xr_new = 0.0
        data = []
        zero_flag = False
        if fl * fu > 0:
            print("No root in this interval")
            return None, False, 0
        if fl == 0 or abs(fl) < self.eps:
            print("Root is: ", self.xl)
            data.append(self.xl)
            data.append(self.xu)
            data.append("-")
            data.append(fl)
            data.append(fu)
            data.append(0.0)
            self.add_to_table(data)
            return self.xl, False, 0
        if fu == 0 or abs(fu) < self.eps:
            print("Root is: ", self.xu)
            data.append(self.xl)
            data.append(self.xu)
            data.append("-")
            data.append(fl)
            data.append(fu)
            data.append(0.0)
            self.add_to_table(data)
            return self.xu, False, 0
        for i in range(0, self.max_iterations):
            data = [self.xl, self.xu]
            xr_new = self.round_to_significant_digit((self.xl + self.xu) / 2.0)
            fr = self.round_to_significant_digit(self.expression.subs(self.x, xr_new).evalf())
            data.append(xr_new)
            data.append(fl)
            data.append(fu)
            data.append(fr)
            if fr * fl < 0:
                self.xu = xr_new
            elif fr * fl > 0:
                self.xl = xr_new
            else:
                print("Root found at: ", xr_new, " number of iterations: ", i + 1)
                data.append(0.0)
                self.add_to_table(data)
                return xr_new, False, i + 1
            if xr_new == 0 or abs(xr_new) < self.eps:
                if zero_flag:
                    data.append(0)
                    self.add_to_table(data)
                    return 0, False, i + 1
                data.append("Infinity")
                self.add_to_table(data)
                zero_flag = True
                continue
            ea = abs((xr_new - xr_old) / xr_new) * 100.0
            data.append(ea)
            zero_flag = False
            if ea < self.tolerance:
                print("Root found at: ", xr_new, " number of iterations: ", i + 1)
                self.add_to_table(data)
                return xr_new, False, i + 1
            self.add_to_table(data)
            xr_old = xr_new
        print("max iterations reached, root is: ", xr_new)
        return xr_new, False, self.max_iterations

    def false_position(self):
        fl = self.round_to_significant_digit(self.expression.subs(self.x, self.xl).evalf())
        fu = self.round_to_significant_digit(self.expression.subs(self.x, self.xu).evalf())
        data = []
        zero_flag = False
        if fl * fu > 0:
            print("No root in this interval")
            return None, False, 0
        xr_old = 0.0
        xr_new = 0.0
        il = 0
        iu = 0
        if fl == 0 or abs(fl) < self.eps:
            print("Root is: ", self.xl)
            data.append(self.xl)
            data.append(self.xu)
            data.append("-")
            data.append(fl)
            data.append(fu)
            data.append(0.0)
            self.add_to_table(data)
            return self.xl, False, 0
        if fu == 0 or abs(fu) < self.eps:
            print("Root is: ", self.xu)
            data.append(self.xl)
            data.append(self.xu)
            data.append("-")
            data.append(fl)
            data.append(fu)
            data.append(0.0)
            self.add_to_table(data)
            return self.xu, False, 0
        for i in range(0, self.max_iterations):
            data = [self.xl, self.xu]
            xr_new = self.round_to_significant_digit(self.xu - ((fu * (self.xl - self.xu)) / (fl - fu)))
            fr = self.round_to_significant_digit(self.expression.subs(self.x, xr_new).evalf())
            data.append(xr_new)
            data.append(fl)
            data.append(fu)
            data.append(fr)
            if fr * fl < 0:
                self.xu = xr_new
                il += 1
                iu = 0
                if il >= 2:
                    fl = self.round_to_significant_digit(fl / 2.0)
            elif fr * fl > 0:
                self.xl = xr_new
                iu += 1
                il = 0
                if iu >= 2:
                    fu = self.round_to_significant_digit(fu / 2.0)
            else:
                print("Root found at: ", xr_new, " number of iterations: ", i + 1)
                data.append(0.0)
                self.add_to_table(data)
                return xr_new, False, i + 1
            if xr_new == 0 or abs(xr_new) < self.eps:
                if zero_flag:
                    data.append(0)
                    self.add_to_table(data)
                    return 0, False, i + 1
                data.append("Infinity")
                self.add_to_table(data)
                zero_flag = True
                continue
            ea = abs((xr_new - xr_old) / xr_new) * 100.0
            data.append(ea)
            zero_flag = False
            if ea < self.tolerance:
                print("Root found at: ", xr_new, " number of iterations: ", i + 1)
                self.add_to_table(data)
                return xr_new, False, i + 1
            self.add_to_table(data)
            xr_old = xr_new
        print("max iterations reached, root is: ", xr_new)
        return None, False, self.max_iterations

    def round_to_significant_digit(self, num):
        if num == 0:
            return 0
        else:
            x = round(num, -int(math.floor(math.log10(abs(num)))) + (self.precision - 1))
            return x

    def add_to_table(self, data):
        self.table.setColumnCount(6)
        column_headers = ["Xl", "Xu", "Xr", "Fl", "Fu", "ea"]
        self.table.setHorizontalHeaderLabels(column_headers)
        self.table.insertRow(self.counter)
        for i in range(len(data)):
            self.table.setItem(self.counter, i, QtWidgets.QTableWidgetItem(str(data[i])))
            self.table.setColumnWidth(i, 200)
        self.counter += 1
