import string

import sympy
from sympy import sympify, symbols, real_root, Pow
import Open_Methods


# func = "x-2**sin(x)"
# p = sympify(func)
# y = Open_Methods.OpenMethods(p, 0.0001, 50, 4, 3, 5)
# print(y.newton_raphson_2())
def my_function(expression):
    # Traverse the expression tree
    for expr in sympy.preorder_traversal(expression):
        # Check if the operation is a power operation
        if isinstance(expr, Pow):
            # Replace the power operation with real_root
            expression = expression.replace(expr, real_root(expr.base, 1/expr.exp))

    # Evaluate the modified expression
    return expression


x = symbols('x')
oo = x ** 5
u = my_function(oo)
print(u.subs(x, 2).evalf())
