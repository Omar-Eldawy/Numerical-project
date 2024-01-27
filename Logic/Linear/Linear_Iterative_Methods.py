import copy
import math
import sys

import numpy as np
from PyQt6 import QtWidgets
from numpy import array


class IterativeMethods:
    def __init__(self, A: array, b: array, x0: list, tol: float, max_iter: int, precision=9, table=None):
        self.A = A
        self.b = b
        self.x0 = [float(x) for x in x0]
        self.tol = tol
        self.max_iter = max_iter
        self.precision = precision
        self.table = table
        self.table_counter = 0

    def is_diagonally_dominant(self):
        diagonal = np.abs(self.A.diagonal())  # extract diagonal values as a vector
        row_sums = np.sum(np.abs(self.A), axis=1) - diagonal  # sum all values in each row except the diagonal value
        if np.all(diagonal >= row_sums):
            return True
        else:
            self.scaling()
            diagonal = np.abs(self.A.diagonal())
            row_sums = np.sum(np.abs(self.A), axis=1) - diagonal
            return np.all(diagonal >= row_sums)

    def jacobi(self):
        if self.is_singular():
            print("Singular matrix")
            return 0, -1
        x = self.x0
        for k in range(self.max_iter):
            x_new = np.zeros_like(x)
            for i in range(len(x)):
                s1 = float(np.dot(self.A[i, :i], x[:i]))  # dot product before xi element
                s2 = float(np.dot(self.A[i, i + 1:], x[i + 1:]))  # dot product after xi element
                if self.check_too_big_number(s1) or self.check_too_big_number(s2):
                    return x, -2
                x_new[i] = self.round_to_significant_digit(
                    (self.b[i] - s1 - s2) / float(self.A[i, i]))  # calculate the new xi
            eps = np.linalg.norm(x_new - x)
            self.add_to_table(eps, x_new)
            if eps < self.tol:
                return x, 0
            x = x_new
        return x, -2

    def gauss_seidel(self):
        if self.is_singular():
            print("Singular matrix")
            return 0, -1
        x = self.x0
        for k in range(self.max_iter):
            x_new = np.zeros_like(x)
            for i in range(len(x)):
                s1 = np.dot(self.A[i, :i], x_new[:i])
                s2 = np.dot(self.A[i, i + 1:], x[i + 1:])
                if self.check_too_big_number(s1) or self.check_too_big_number(s2):
                    return x, -2
                x_new[i] = self.round_to_significant_digit((self.b[i] - s1 - s2) / float(self.A[i, i]))
            eps = np.linalg.norm(x_new - x)
            self.add_to_table(eps, x_new)
            if eps < self.tol:
                return x, 0
            x = x_new
        return x, -2

    def is_singular(self):
        if np.linalg.det(self.A) == 0:
            return True
        return False

    def scaling(self):
        array_copy = copy.deepcopy(self.A)
        for i in range(len(self.A)):
            max_vector = np.max(np.abs(self.A[i:, i:]), axis=1)
            after_scaling = array_copy[i:, i] / max_vector
            index_of_max = np.argmax(np.abs(after_scaling))
            self.A[index_of_max + i], self.A[i] = copy.deepcopy(self.A[i]), copy.deepcopy(self.A[index_of_max + i])
            self.b[index_of_max + i], self.b[i] = copy.deepcopy(self.b[i]), copy.deepcopy(self.b[index_of_max + i])

    def round_to_significant_digit(self, num):
        if num == 0:
            return 0
        else:
            x = round(num, -int(math.floor(math.log10(abs(num)))) + (self.precision - 1))
            return x

    def add_to_table(self, epsilon, x):
        counter = len(self.x0)
        self.table.setColumnCount(counter + 1)
        column_headers = [f"X{i}" for i in range(counter)]
        column_headers.append("epsilon")
        self.table.setHorizontalHeaderLabels(column_headers)
        for i in range(counter):
            self.table.insertRow(i + self.table_counter)
            self.table.setItem(self.table_counter, i, QtWidgets.QTableWidgetItem(str(x[i])))
            self.table.setColumnWidth(i, 170)
        self.table.setItem(self.table_counter, counter, QtWidgets.QTableWidgetItem(str(epsilon)))
        self.table.setColumnWidth(counter, 170)
        self.table_counter += 1

    def check_too_big_number(self, number):
        max_float = sys.float_info.max
        return abs(number) > max_float
