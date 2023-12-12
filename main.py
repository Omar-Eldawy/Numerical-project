from Linear_Direct_Methods import LinearSolver
import numpy as np
from Linear_Iterative_Methods import IterativeMethods

equations = np.array([[3, 7, 13], [1, 5, 3], [12, 3, -5]])
answers = np.array([76, 28, 1])
# print(np.linalg.solve(equations, answers))
# x = LinearSolver(equations, answers)
# print(x.gauss_elimination())
# print(x.gauss_jordan())
y = IterativeMethods(equations, answers, [1.0, 1, 1], 0.0001, 200)
print(np.linalg.solve(equations, answers))
print(y.gauss_seidel())
