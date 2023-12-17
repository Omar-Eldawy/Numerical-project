import sys

from Linear_Direct_Methods import LinearSolver
import numpy as np
from Linear_Iterative_Methods import IterativeMethods

equations = np.array([[4, 12, -16], [10, 37, -43], [-16, -43, 98]])
answers = np.array([45, 1.751, 9])
print(np.linalg.solve(equations, answers))
x = LinearSolver(equations, answers)
# print(x.gauss_elimination())
# print(x.gauss_jordan())
# y = IterativeMethods(equations, answers, [1.0, 1, 1], 0.0001, 200)
# print(np.linalg.solve(equations, answers))
# print(y.gauss_seidel())
# print(x.gauss_jordan())
print(x.cholesky_lu())
# print(x.gauss_jordan())