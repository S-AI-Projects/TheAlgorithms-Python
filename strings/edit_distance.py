def edit_distance(source: str, target: str) -> int:
    """
    Edit distance algorithm is a string metric, i.e., it is a way of quantifying how
    dissimilar two strings are to one another. It is measured by counting the minimum
    number of operations required to transform one string into another.

    This implementation assumes that the cost of operations (insertion, deletion and
    substitution) is always 1

    Args:
    source: the initial string with respect to which we are calculating the edit
        distance for the target
    target: the target string, formed after performing n operations on the source string

    >>> edit_distance("GATTIC", "GALTIC")
    1
    >>> edit_distance("NUM3", "HUM2")
    2
    >>> edit_distance("cap", "CAP")
    3
    >>> edit_distance("Cat", "")
    3
    >>> edit_distance("cat", "cat")
    0
    >>> edit_distance("", "123456789")
    9
    >>> edit_distance("Be@uty", "Beautyyyy!")
    5
    >>> edit_distance("lstring", "lsstring")
    1
    >>> edit_distance("same", "same")
    0
    >>> edit_distance("kitten", "sitting")
    3
    >>> edit_distance("sitting", "kitten")
    3
    >>> edit_distance("", "")
    0
    >>> edit_distance(1, "a")
    Traceback (most recent call last):
        ...
    TypeError: edit_distance() arguments must be strings
    """
    if not isinstance(source, str) or not isinstance(target, str):
        raise TypeError("edit_distance() arguments must be strings")

    if len(source) == 0:
        return len(target)
    elif len(target) == 0:
        return len(source)

    delta = int(source[-1] != target[-1])  # Substitution
    return min(
        edit_distance(source[:-1], target[:-1]) + delta,
        edit_distance(source, target[:-1]) + 1,
        edit_distance(source[:-1], target) + 1,
    )


if __name__ == "__main__":
    print(edit_distance("ATCGCTG", "TAGCTAA"))  # Answer is 4
