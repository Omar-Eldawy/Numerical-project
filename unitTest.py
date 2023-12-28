import string

from sympy import sympify, symbols
import Open_Methods


func = "x-2**sin(x)"
p = sympify(func)
y = Open_Methods.OpenMethods(p, 0.0001, 50, 4, 3, 5)
print(y.newton_raphson_2())
