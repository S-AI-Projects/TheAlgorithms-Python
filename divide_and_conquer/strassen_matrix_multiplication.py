"""
https://en.wikipedia.org/wiki/Strassen_algorithm
"""

from __future__ import annotations

import math


def default_matrix_multiplication(a: list, b: list) -> list:
    """
    Multiplication only for 2x2 matrices

    >>> default_matrix_multiplication([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    >>> default_matrix_multiplication([[0, 0], [0, 0]], [[1, 2], [3, 4]])
    [[0, 0], [0, 0]]
    >>> default_matrix_multiplication([[1, 2]], [[3, 4]])
    Traceback (most recent call last):
        ...
    Exception: Matrices are not 2x2
    """
    if len(a) != 2 or len(a[0]) != 2 or len(b) != 2 or len(b[0]) != 2:
        raise Exception("Matrices are not 2x2")
    return [
        [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
        [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]],
    ]


def matrix_addition(matrix_a: list, matrix_b: list) -> list:
    """
    Element-wise addition of two matrices of the same shape.

    >>> matrix_addition([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[6, 8], [10, 12]]
    >>> matrix_addition([[5]], [[3]])
    [[8]]
    >>> matrix_addition([[1, 2]], [[1]])
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    """
    return [
        [matrix_a[row][col] + matrix_b[row][col] for col in range(len(matrix_a[row]))]
        for row in range(len(matrix_a))
    ]


def matrix_subtraction(matrix_a: list, matrix_b: list) -> list:
    """
    Element-wise subtraction of two matrices of the same shape.

    >>> matrix_subtraction([[5, 6], [7, 8]], [[1, 2], [3, 4]])
    [[4, 4], [4, 4]]
    >>> matrix_subtraction([[10]], [[3]])
    [[7]]
    >>> matrix_subtraction([[1, 2]], [[1]])
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    """
    return [
        [matrix_a[row][col] - matrix_b[row][col] for col in range(len(matrix_a[row]))]
        for row in range(len(matrix_a))
    ]


def extract_submatrix(matrix: list, rows: range, cols: range) -> list:
    """
    Extract a submatrix from matrix given row and column index ranges.

    >>> extract_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], range(0, 2), range(1, 3))
    [[2, 3], [5, 6]]
    >>> extract_submatrix([[1, 2], [3, 4]], range(1, 2), range(0, 1))
    [[3]]
    >>> extract_submatrix([[1, 2]], range(0, 2), range(0, 2))
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    """
    return [[matrix[i][j] for j in cols] for i in rows]


def split_matrix(a: list) -> tuple[list, list, list, list]:
    """
    Given an even-length matrix, returns the top_left, top_right, bot_left, bot_right
    quadrant.

    >>> split_matrix([[4,3,2,4],[2,3,1,1],[6,5,4,3],[8,4,1,6]])
    ([[4, 3], [2, 3]], [[2, 4], [1, 1]], [[6, 5], [8, 4]], [[4, 3], [1, 6]])
    >>> split_matrix([
    ...     [4,3,2,4,4,3,2,4],[2,3,1,1,2,3,1,1],[6,5,4,3,6,5,4,3],[8,4,1,6,8,4,1,6],
    ...     [4,3,2,4,4,3,2,4],[2,3,1,1,2,3,1,1],[6,5,4,3,6,5,4,3],[8,4,1,6,8,4,1,6]
    ... ])  # doctest: +NORMALIZE_WHITESPACE
    ([[4, 3, 2, 4], [2, 3, 1, 1], [6, 5, 4, 3], [8, 4, 1, 6]], [[4, 3, 2, 4],
      [2, 3, 1, 1], [6, 5, 4, 3], [8, 4, 1, 6]], [[4, 3, 2, 4], [2, 3, 1, 1],
      [6, 5, 4, 3], [8, 4, 1, 6]], [[4, 3, 2, 4], [2, 3, 1, 1], [6, 5, 4, 3],
      [8, 4, 1, 6]])
    >>> split_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    Traceback (most recent call last):
        ...
    Exception: Odd matrices are not supported!
    """
    if len(a) % 2 != 0 or len(a[0]) % 2 != 0:
        raise Exception("Odd matrices are not supported!")

    mid = len(a) // 2

    rows_top, rows_bot = range(mid), range(mid, len(a))
    cols_left, cols_right = range(mid), range(mid, len(a))

    return (
        extract_submatrix(a, rows_top, cols_left),  # Top-left
        extract_submatrix(a, rows_top, cols_right),  # Top-right
        extract_submatrix(a, rows_bot, cols_left),  # Bottom-left
        extract_submatrix(a, rows_bot, cols_right),  # Bottom-right
    )


def matrix_dimensions(matrix: list) -> tuple[int, int]:
    """
    Return the dimensions (rows, columns) of a 2D matrix.

    >>> matrix_dimensions([[1, 2], [3, 4]])
    (2, 2)
    >>> matrix_dimensions([[1, 2, 3], [4, 5, 6]])
    (2, 3)
    >>> matrix_dimensions([])
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    """
    return len(matrix), len(matrix[0])


def print_matrix(matrix: list) -> None:
    """
    Print each row of the matrix on a new line.

    >>> print_matrix([[1, 2], [3, 4]])
    [1, 2]
    [3, 4]
    >>> print_matrix([[42]])
    [42]
    >>> print_matrix(123)  # type: ignore[arg-type]
    Traceback (most recent call last):
        ...
    TypeError: 'int' object is not iterable
    """
    print("\n".join(str(line) for line in matrix))


def actual_strassen(matrix_a: list, matrix_b: list) -> list:
    """
    Recursive function to calculate the product of two matrices, using the Strassen
    Algorithm.

    Time complexity:
        The recurrence is T(n) = 7 T(n/2) + \u0398(n^2), which solves to
        T(n) = \u0398(n^{log_2 7}) \u2248 \u0398(n^{2.8074}). This is asymptotically
        faster than the naive \u0398(n^3) algorithm for sufficiently large n.

    Space complexity:
        Uses additional memory for temporary submatrices and padding; overall
        space complexity is O(n^2).

    Notes:
        This function expects square matrices whose size is a power of two.
        Matrices of other sizes are handled by `strassen` which pads to the
        next power of two.

    It only supports square matrices of any size that is a power of 2.

    Strassen's algorithm reduces the number of recursive multiplications needed to
    multiply two n x n matrices from the 8 required by the naive divide-and-conquer
    approach down to 7, at the cost of a few extra matrix additions/subtractions
    (which are cheaper, O(n^2), operations). Each matrix is split into four
    (n/2) x (n/2) quadrants; 7 products of quadrant combinations are computed
    recursively, and those products are combined with additions/subtractions to
    form the four quadrants of the result.

    Time complexity: O(n^log2(7)) ~= O(n^2.807), an improvement over the O(n^3) of
    the standard/naive matrix multiplication algorithm.
    Space complexity: O(n^2) for storing the intermediate quadrant matrices, plus
    O(log n) recursion stack depth.

    Examples:
        >>> actual_strassen([[1, 2], [3, 4]], [[5, 6], [7, 8]])
        [[19, 22], [43, 50]]
        >>> a = [
        ...     [1, 2, 3, 4],
        ...     [5, 6, 7, 8],
        ...     [9, 1, 2, 3],
        ...     [4, 5, 6, 7],
        ... ]
        >>> b = [
        ...     [7, 6, 5, 4],
        ...     [3, 2, 1, 9],
        ...     [8, 7, 6, 5],
        ...     [4, 3, 2, 1],
        ... ]
        >>> actual_strassen(a, b)
        [[53, 43, 33, 41], [141, 115, 89, 117], [94, 79, 64, 58], [119, 97, 75, 98]]
        >>> actual_strassen(
        ...     [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        ...     [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        ... )
        Traceback (most recent call last):
            ...
        Exception: Odd matrices are not supported!
    """
    if matrix_dimensions(matrix_a) == (2, 2):
        return default_matrix_multiplication(matrix_a, matrix_b)

    a, b, c, d = split_matrix(matrix_a)
    e, f, g, h = split_matrix(matrix_b)

    t1 = actual_strassen(a, matrix_subtraction(f, h))
    t2 = actual_strassen(matrix_addition(a, b), h)
    t3 = actual_strassen(matrix_addition(c, d), e)
    t4 = actual_strassen(d, matrix_subtraction(g, e))
    t5 = actual_strassen(matrix_addition(a, d), matrix_addition(e, h))
    t6 = actual_strassen(matrix_subtraction(b, d), matrix_addition(g, h))
    t7 = actual_strassen(matrix_subtraction(a, c), matrix_addition(e, f))

    top_left = matrix_addition(matrix_subtraction(matrix_addition(t5, t4), t2), t6)
    top_right = matrix_addition(t1, t2)
    bot_left = matrix_addition(t3, t4)
    bot_right = matrix_subtraction(matrix_subtraction(matrix_addition(t1, t5), t3), t7)

    # construct the new matrix from our 4 quadrants
    new_matrix = []
    for i in range(len(top_right)):
        new_matrix.append(top_left[i] + top_right[i])
    for i in range(len(bot_right)):
        new_matrix.append(bot_left[i] + bot_right[i])
    return new_matrix


def strassen(matrix1: list, matrix2: list) -> list:
    """
    Multiply two matrices using Strassen's divide-and-conquer algorithm.

    Time complexity:
        \u0398(n^{log_2 7}) \u2248 \u0398(n^{2.8074})
        (recurrence T(n) = 7 T(n/2) + \u0398(n^2)).

    Space complexity:
        O(n^2) due to padding and temporary matrices used during recursion.

    Multiply two matrices using Strassen's algorithm, which runs in
    O(n^log2(7)) ~= O(n^2.807) time, compared to O(n^3) for naive matrix
    multiplication. This implementation pads both input matrices with zeros
    until they are square matrices whose dimension is a power of 2 (required
    by the divide-and-conquer recursion in actual_strassen), performs the
    multiplication, then trims the padding back off the result.

    Examples:

    >>> strassen([[2,1,3],[3,4,6],[1,4,2],[7,6,7]], [[4,2,3,4],[2,1,1,1],[8,6,4,2]])
    [[34, 23, 19, 15], [68, 46, 37, 28], [28, 18, 15, 12], [96, 62, 55, 48]]
    >>> strassen([[3,7,5,6,9],[1,5,3,7,8],[1,4,4,5,7]], [[2,4],[5,2],[1,7],[5,5],[7,8]])
    [[139, 163], [121, 134], [100, 121]]
    >>> strassen([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 2], [3, 4], [5, 6]])
    [[22, 28], [49, 64], [76, 100]]
    >>> strassen([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    >>> strassen([[1, 2]], [[3, 4]])
    Traceback (most recent call last):
        ...
    Exception: Unable to multiply these matrices, please check the dimensions.
    Matrix A: [[1, 2]]
    Matrix B: [[3, 4]]
    """
    if matrix_dimensions(matrix1)[1] != matrix_dimensions(matrix2)[0]:
        msg = (
            "Unable to multiply these matrices, please check the dimensions.\n"
            f"Matrix A: {matrix1}\n"
            f"Matrix B: {matrix2}"
        )
        raise Exception(msg)
    dimension1 = matrix_dimensions(matrix1)
    dimension2 = matrix_dimensions(matrix2)

    if dimension1[0] == dimension1[1] and dimension2[0] == dimension2[1]:
        return [matrix1, matrix2]

    maximum = max(*dimension1, *dimension2)
    maxim = int(math.pow(2, math.ceil(math.log2(maximum))))
    new_matrix1 = matrix1
    new_matrix2 = matrix2

    # Adding zeros to the matrices to convert them both into square matrices of equal
    # dimensions that are a power of 2
    for i in range(maxim):
        if i < dimension1[0]:
            for _ in range(dimension1[1], maxim):
                new_matrix1[i].append(0)
        else:
            new_matrix1.append([0] * maxim)
        if i < dimension2[0]:
            for _ in range(dimension2[1], maxim):
                new_matrix2[i].append(0)
        else:
            new_matrix2.append([0] * maxim)

    final_matrix = actual_strassen(new_matrix1, new_matrix2)

    # Removing the additional zeros
    for i in range(maxim):
        if i < dimension1[0]:
            for _ in range(dimension2[1], maxim):
                final_matrix[i].pop()
        else:
            final_matrix.pop()
    return final_matrix


if __name__ == "__main__":
    matrix1 = [
        [2, 3, 4, 5],
        [6, 4, 3, 1],
        [2, 3, 6, 7],
        [3, 1, 2, 4],
        [2, 3, 4, 5],
        [6, 4, 3, 1],
        [2, 3, 6, 7],
        [3, 1, 2, 4],
        [2, 3, 4, 5],
        [6, 2, 3, 1],
    ]
    matrix2 = [[0, 2, 1, 1], [16, 2, 3, 3], [2, 2, 7, 7], [13, 11, 22, 4]]
    print(strassen(matrix1, matrix2))
