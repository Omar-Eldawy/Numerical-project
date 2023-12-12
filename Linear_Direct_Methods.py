import copy

from numpy import array


class LinearSolver:
    def __init__(self, a: array, b: list):
        self.a = a  # coefficients matrix
        self.b = b  # constants matrix

    def gauss_elimination(self):
        flag = self.forward_elimination()
        if flag == -1:
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
        if flag == -1:
            print("Singular matrix")
            return -1
        return self.b