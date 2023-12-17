import copy
import math

import numpy as np
from numpy import array


class IterativeMethods:
    def __init__(self, A: array, b: array, x0: list, tol: float, max_iter: int, precision=17):
        self.A = A
        self.b = b
        self.x0 = [float(x) for x in x0]
        self.tol = tol
        self.max_iter = max_iter
        self.scaling()
        self.precision = precision


    def is_diagonally_dominant(self):
        diagonal = np.abs(self.A.diagonal())  # extract diagonal values as a vector
        row_sums = np.sum(np.abs(self.A), axis=1) - diagonal  # sum all values in each row except the diagonal value
        return np.all(diagonal >= row_sums)

    def jacobi(self):
        if self.is_singular():
            print("Singular matrix")
            return -1
        x = self.x0
        for k in range(self.max_iter):
            x_new = np.zeros_like(x)
            for i in range(len(x)):
                s1 = float(np.dot(self.A[i, :i], x[:i]))  # dot product before xi element
                s2 = float(np.dot(self.A[i, i + 1:], x[i + 1:]))  # dot product after xi element
                x_new[i] = self.round_to_significant_digit((self.b[i] - s1 - s2) / float(self.A[i, i]))  # calculate the new xi
            if np.linalg.norm(x_new - x) < self.tol:
                break
            x = x_new
        return x

    def gauss_seidel(self):
        if self.is_singular():
            print("Singular matrix")
            return -1
        x = self.x0
        for k in range(self.max_iter):
            x_new = np.zeros_like(x)
            for i in range(len(x)):
                s1 = np.dot(self.A[i, :i], x_new[:i])
                s2 = np.dot(self.A[i, i + 1:], x[i + 1:])
                x_new[i] = self.round_to_significant_digit((self.b[i] - s1 - s2) / float(self.A[i, i]))
            if np.linalg.norm(x_new - x) < self.tol:
                break
            x = x_new
        return x

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
            self.A[index_of_max+i], self.A[i] = copy.deepcopy(self.A[i]), copy.deepcopy(self.A[index_of_max+i])
            self.b[index_of_max + i], self.b[i] = copy.deepcopy(self.b[i]), copy.deepcopy(self.b[index_of_max + i])

    def round_to_significant_digit(self, num):
        if num == 0:
            return 0
        else:
            x = round(num, -int(math.floor(math.log10(abs(num)))) + (self.precision - 1))
            return x
