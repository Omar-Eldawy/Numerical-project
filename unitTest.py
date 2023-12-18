import math
import sys

from Linear_Direct_Methods import LinearSolver
import numpy as np
from Linear_Iterative_Methods import IterativeMethods
from decimal import Decimal, getcontext, ROUND_HALF_UP

# from sigfig import round

equations = np.array([[20.0, 12, -16], [10.00, 37.00, -43], [-16.00, -43.00, 50]])
answers = np.array([45, 1.751, 9])
# print(np.linalg.solve(equations, answers))
x = LinearSolver(equations, answers)

# print(x.gauss_elimination())
# print(x.gauss_jordan_elimination())

# # print(x.gauss_jordan())
# # y = IterativeMethods(equations, answers, [1.0, 1, 1], 0.0001, 200)
# # print(np.linalg.solve(equations, answers))
# # print(y.gauss_seidel())
# print(x.gauss_jordan())
# print(x.doolittle())


# print(x.cholesky_lu())
# # print(x.gauss_jordan())

def round_to_significant_digit(number, digits):
    rounded_number = np.around(number, digits - int(np.floor(np.log10(abs(number)))) - 1)
    return rounded_number


print(round_to_significant_digit(1.99943, 3))


def check_too_big_number(number):
    max_float = sys.float_info.max
    return abs(number) > max_float

s= 1e300 ** 1e400
print(check_too_big_number(s))