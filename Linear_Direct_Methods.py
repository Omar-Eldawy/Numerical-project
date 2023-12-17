import copy

import numpy as np
from numpy import array


class LinearSolver:
    def __init__(self, a: array, b: list):
        self.a = a  # coefficients matrix
        self.b = b  # constants matrix

    def gauss_elimination(self):
        flag = self.forward_elimination()
        if isinstance(flag, int) and flag == -1:
            print("Singular matrix")
            return -1
        return self.backward_substitution()

    def forward_elimination(self):
        for i in range(len(self.a)):
            self.partial_pivoting(i)
            if self.a[i][i] == 0:
                return -1  # singular matrix
            for j in range(i + 1, len(self.a)):
                factor = self.a[j][i] / self.a[i][i]
                for k in range(len(self.a)):
                    self.a[j][k] -= factor * self.a[i][k]
                self.b[j] -= factor * self.b[i]
        return 0

    def gauss_jordan_elimination(self):
        for i in range(len(self.a)):
            self.partial_pivoting(i)
            if self.a[i][i] == 0:
                return -1  # singular matrix
            scale = self.a[i][i]
            for j in range(len(self.a)):
                self.a[i][j] /= scale
            self.b[i] /= scale
            for j in range(len(self.a)):
                if i != j:
                    factor = self.a[j][i] / self.a[i][i]
                    for k in range(len(self.a)):
                        self.a[j][k] -= factor * self.a[i][k]
                    self.b[j] -= factor * self.b[i]
        return self.b

    def backward_substitution(self):
        x = [0 for i in range(len(self.a))]  # generate a list of zeros representing the number of variables
        for i in range(len(self.a) - 1, -1, -1):
            x[i] = self.b[i] / self.a[i][i]
            for j in range(i - 1, -1, -1):
                self.b[j] -= self.a[j][i] * x[i]
        return x

    def partial_pivoting(self, current_row):
        max_row = current_row
        for j in range(current_row + 1, len(self.a)):
            if abs(self.a[j][current_row]) > abs(self.a[max_row][current_row]):
                max_row = j
        self.a[current_row], self.a[max_row] = copy.deepcopy(self.a[max_row]), copy.deepcopy(self.a[current_row])
        self.b[current_row], self.b[max_row] = copy.deepcopy(self.b[max_row]), copy.deepcopy(self.b[current_row])

    def gauss_jordan(self):
        flag = self.gauss_jordan_elimination()
        if isinstance(flag, int) and flag == -1:
            print("Singular matrix")
            return -1
        return self.b

    def doolittle_decomposition(self, scaling_factors, pivot_rows, tol=1e-10):
        scaling_factors, pivot_rows = self.get_scaling_factors(scaling_factors, pivot_rows)
        for k in range(len(self.a)):
            pivot_rows = self.get_pivot(scaling_factors, pivot_rows, k)
            if abs(self.a[pivot_rows[k], k] / scaling_factors[pivot_rows[k]]) < tol:
                return -1
            for i in range(k + 1, len(self.a)):
                factor = self.a[pivot_rows[i], k] / self.a[pivot_rows[k], k]
                self.a[pivot_rows[i], k] = factor
                for j in range(k + 1, len(self.a)):
                    self.a[pivot_rows[i], j] -= factor * self.a[pivot_rows[k], j]
        return pivot_rows

    def doolittle_substitution(self, o):
        y = np.zeros(len(self.a), dtype=float)
        x = np.zeros(len(self.a), dtype=float)
        for i in range(len(self.a)):
            y[i] = self.b[o[i]]
            for j in range(i):
                y[i] -= self.a[o[i], j] * y[j]
        for i in range(len(self.a) - 1, -1, -1):
            x[i] = y[i]
            for j in range(i + 1, len(self.a)):
                x[i] -= self.a[o[i], j] * x[j]
            x[i] /= self.a[o[i], i]
        return x

    def get_scaling_factors(self, s, o):
        for i in range(len(self.a)):
            s[i] = max(abs(self.a[i, :]))
            o[i] = i
        return s, o

    def get_pivot(self, s, o, k):
        p = k
        big = abs(self.a[o[k], k] / s[o[k]])
        for i in range(k + 1, len(self.a)):
            dummy = abs(self.a[o[i], k] / s[o[i]])
            if dummy > big:
                big = dummy
                p = i
        dummy = o[p]
        o[p] = o[k]
        o[k] = dummy
        return o

    def doolittle(self, tol=1e-10):
        scaling_factors = np.zeros(len(self.a))
        pivot_rows = np.zeros(len(self.a), dtype=int)
        pivot_rows = self.doolittle_decomposition(scaling_factors, pivot_rows, tol)
        if isinstance(pivot_rows, int) and pivot_rows == -1:
            print("Singular matrix")
            return -1
        return self.doolittle_substitution(pivot_rows)

    def crout_lu_decomposition(self):
        n = len(self.a)
        L = np.zeros((n, n))
        U = np.eye(n)

        for j in range(n):
            for i in range(j, n):
                L[i, j] = self.a[i, j] - L[i, :j].dot(U[:j, j])
            for i in range(j + 1, n):
                U[j, i] = (self.a[j, i] - L[j, :j].dot(U[:j, i])) / L[j, j]

        return L, U

    def crout_forward_substitution(self, L):
        n = len(self.b)
        y = np.zeros(n)

        for i in range(n):
            y[i] = (self.b[i] - L[i, :i].dot(y[:i])) / L[i, i]

        return y

    def crout_backward_substitution(self, U, y):
        n = len(y)
        x = np.zeros(n)

        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - U[i, i + 1:].dot(x[i + 1:])) / U[i, i]

        return x

    def crout_lu(self, tol=1e-10):
        L, U = self.crout_lu_decomposition()
        if np.any(abs(np.diagonal(L)) < tol):
            print("Singular matrix")
            return -1
        y = self.crout_forward_substitution(L)
        x = self.crout_backward_substitution(U, y)
        return x

    def is_positive_definite(self):
        # Check if the matrix is symmetric
        if not np.allclose(self.a, self.a.T):
            print("Matrix is not symmetric")
            return False

        # Check if the matrix is positive-definite
        if not np.all(np.linalg.eigvals(self.a) > 0):
            print("Matrix is not positive-definite")
            return False
        return True

    def cholesky_lu_decomposition(self):
        n = len(self.a)
        L = np.zeros((n, n))
        if not self.is_positive_definite():
            return -1, -1
        for i in range(n):
            for k in range(i + 1):
                tmp_sum = sum(L[i][j] * L[k][j] for j in range(k))

                if i == k:  # Diagonal elements
                    L[i][k] = np.sqrt(self.a[i][i] - tmp_sum)
                else:
                    L[i][k] = (1.0 / L[k][k] * (self.a[i][k] - tmp_sum))
        return L, L.T  # matrix, transpose of matrix

    def cholesky_forward_substitution(self, L):
        n = len(self.b)
        y = np.zeros(n)

        for i in range(n):
            y[i] = (self.b[i] - L[i, :i].dot(y[:i])) / L[i, i]

        return y

    def cholesky_backward_substitution(self, U, y):
        n = len(y)
        x = np.zeros(n)

        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - U[i, i + 1:].dot(x[i + 1:])) / U[i, i]

        return x

    def cholesky_lu(self):
        L, U = self.cholesky_lu_decomposition()
        if isinstance(L, int) and L == -1:
            print("Not positive-definite matrix")
            return -1
        y = self.cholesky_forward_substitution(L)
        x = self.cholesky_backward_substitution(U, y)
        return x
