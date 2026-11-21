from collections.abc import Callable

import numpy as np


def explicit_euler(
    ode_func: Callable, y0: float, x0: float, step_size: float, x_end: float
) -> np.ndarray:
    """Calculate numeric solution at each step to an ODE using Euler's Method

    For dy/dx = y with y(0) = 1 on [0, 1], the global error is O(h).
    The modified Euler method has error O(h**2), while classical Runge-Kutta
    has error O(h**4). Halving the step size therefore reduces the errors by
    approximately 1/2, 1/4, and 1/16, respectively.

    For reference to Euler's method refer to https://en.wikipedia.org/wiki/Euler_method.

    Args:
        ode_func (Callable):  The ordinary differential equation
            as a function of x and y.
        y0 (float): The initial value for y.
        x0 (float): The initial value for x.
        step_size (float): The increment value for x.
        x_end (float): The final value of x to be calculated.

    Returns:
        np.ndarray: Solution of y for every step in x.

    >>> # the exact solution is math.exp(x)
    >>> def f(x, y):
    ...     return y
    >>> y0 = 1
    >>> y = explicit_euler(f, y0, 0.0, 0.01, 5)
    >>> float(y[-1])
    144.77277243257308

    Compare the error ratios for halved step sizes:

    >>> import math
    >>> from maths.euler_modified import euler_modified
    >>> from maths.numerical_analysis.runge_kutta import runge_kutta
    >>> def error(method, h):
    ...     return abs(float(method(f, 1, 0, h, 1)[-1]) - math.e)
    >>> round(error(explicit_euler, 0.05) / error(explicit_euler, 0.1), 2)
    0.52
    >>> round(error(euler_modified, 0.05) / error(euler_modified, 0.1), 2)
    0.26
    >>> round(error(runge_kutta, 0.05) / error(runge_kutta, 0.1), 2)
    0.07
    """
    n = int(np.ceil((x_end - x0) / step_size))
    y = np.zeros((n + 1,))
    y[0] = y0
    x = x0

    for k in range(n):
        y[k + 1] = y[k] + step_size * ode_func(x, y[k])
        x += step_size

    return y


if __name__ == "__main__":
    import doctest

    doctest.testmod()
