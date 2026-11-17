"""
This is an implementation of Pigeon Hole Sort.
For doctests run following command:

python3 -m doctest -v pigeon_sort.py
or
python -m doctest -v pigeon_sort.py

For manual testing run:
python pigeon_sort.py
"""

from __future__ import annotations


def pigeon_sort(array: list[int]) -> list[int]:
    """
    Implementation of pigeon hole sort algorithm.

    Complexity:
        Time Complexity: O(n + range) where n is len(array) and
        range = max(array) - min(array) + 1. Finding min/max takes O(n),
        populating the holes takes O(n), and collecting elements takes O(range + n).
        Space Complexity: O(range) for the auxiliary hole lists.

    :param array: Collection of comparable items
    :return: Collection sorted in ascending order

    >>> pigeon_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> pigeon_sort([])
    []
    >>> pigeon_sort([-2, -5, -45])
    [-45, -5, -2]
    >>> pigeon_sort([-1000, 50, -200, 0, 1000, -500])
    [-1000, -500, -200, 0, 50, 1000]
    >>> pigeon_sort([100000, 0, -100000])
    [-100000, 0, 100000]
    """
    if len(array) == 0:
        return array

    _min, _max = min(array), max(array)

    # Compute the variables
    holes_range = _max - _min + 1
    holes, holes_repeat = [0] * holes_range, [0] * holes_range

    # Make the sorting.
    for i in array:
        index = i - _min
        holes[index] = i
        holes_repeat[index] += 1

    # Makes the array back by replacing the numbers.
    index = 0
    for i in range(holes_range):
        while holes_repeat[i] > 0:
            array[index] = holes[i]
            index += 1
            holes_repeat[i] -= 1

    # Returns the sorted array.
    return array


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    user_input = input("Enter numbers separated by comma:\n")
    unsorted = [int(x) for x in user_input.split(",")]
    print(pigeon_sort(unsorted))
