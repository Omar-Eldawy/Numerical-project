from Linear_Solver import LinearSolver
import numpy as np

equations = np.array([[4.0, 6, 2, -2], [2, 0, 5, -2], [-4, -3, -5, 4], [8, 18, -2, 3]])
answers = np.array([8.0, 4, 1, 40])
print(np.linalg.solve(equations, answers))
x = LinearSolver(equations, answers)
print(x.gauss_elimination())

