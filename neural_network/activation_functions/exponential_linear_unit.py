"""
Implements the Exponential Linear Unit or ELU function.

The function takes a vector of K real numbers and a real number alpha as
input and then applies the ELU function to each element of the vector.

Script inspired from its corresponding Wikipedia article
https://en.wikipedia.org/wiki/Rectifier_(neural_networks)
"""

import numpy as np


def exponential_linear_unit(vector: np.ndarray, alpha: float) -> np.ndarray:
    """
         Implements the ELU activation function.
         Parameters:
             vector: the array containing input of elu activation
             alpha: hyper-parameter
         return:
         elu (np.array): The input numpy array after applying elu.

         Mathematically, f(x) = x, x>0 else (alpha * (e^x -1)), x<=0, alpha >=0

    Examples:
    >>> exponential_linear_unit(vector=np.array([2.3,0.6,-2,-3.8]), alpha=0.3)
    array([ 2.3       ,  0.6       , -0.25939942, -0.29328877])

    >>> exponential_linear_unit(vector=np.array([-9.2,-0.3,0.45,-4.56]), alpha=0.067)
    array([-0.06699323, -0.01736518,  0.45      , -0.06629904])

    Edge values: zero maps to zero for any alpha, and large negative inputs
    saturate at -alpha (the exponential underflows to 0):

    >>> exponential_linear_unit(vector=np.array([0.0]), alpha=0.3)
    array([0.])
    >>> exponential_linear_unit(vector=np.array([-1000.0]), alpha=0.3)
    array([-0.3])
    >>> exponential_linear_unit(vector=np.array([-50.0, 50.0]), alpha=1.0)
    array([-1., 50.])

    With alpha = 0 the negative side is flat zero (a plain ReLU):

    >>> exponential_linear_unit(vector=np.array([-2.0, 0.0, 2.0]), alpha=0.0)
    array([-0.,  0.,  2.])

    SELU is ELU multiplied by a scale, so with scale (lambda_) 1 and the same alpha
    the two functions are identical:

    >>> from neural_network.activation_functions.scaled_exponential_linear_unit import (
    ...     scaled_exponential_linear_unit,
    ... )
    >>> x = np.array([-5.0, -1.0, -0.1, 0.0, 0.1, 1.0, 5.0])
    >>> bool(np.array_equal(
    ...     exponential_linear_unit(x, alpha=0.3),
    ...     scaled_exponential_linear_unit(x, alpha=0.3, lambda_=1.0),
    ... ))
    True

    At SELU's documented constants (alpha=1.6732, lambda_=1.0507), SELU equals
    1.0507 * ELU(x, alpha=1.6732):

    >>> bool(np.allclose(
    ...     scaled_exponential_linear_unit(x),
    ...     1.0507 * exponential_linear_unit(x, alpha=1.6732),
    ... ))
    True

    For positive inputs ELU and Leaky ReLU are both the identity, for any alpha:

    >>> from neural_network.activation_functions.leaky_rectified_linear_unit import (
    ...     leaky_rectified_linear_unit,
    ... )
    >>> positive = np.array([0.1, 1.0, 2.5, 100.0])
    >>> bool(np.array_equal(
    ...     exponential_linear_unit(positive, alpha=0.3),
    ...     leaky_rectified_linear_unit(positive, alpha=0.3),
    ... ))
    True
    """
    return np.where(vector > 0, vector, (alpha * (np.exp(vector) - 1)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
