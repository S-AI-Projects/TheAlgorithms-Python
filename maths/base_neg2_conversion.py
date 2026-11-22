def decimal_to_negative_base_2(num: int) -> int:
    """
    This function returns the number negative base 2
        of the decimal number of the input data.

    Args:
        num (int): The decimal integer to convert.

    Returns:
        int: The negative base 2 number.

    Raises:
        TypeError: If num is not an integer (e.g., float, bool, str, None).

    Examples:
        >>> decimal_to_negative_base_2(0)
        0
        >>> decimal_to_negative_base_2(-19)
        111101
        >>> decimal_to_negative_base_2(4)
        100
        >>> decimal_to_negative_base_2(7)
        11011
        >>> decimal_to_negative_base_2(3.5)
        Traceback (most recent call last):
        ...
        TypeError: num must be an integer, not float
        >>> decimal_to_negative_base_2(True)
        Traceback (most recent call last):
        ...
        TypeError: num must be an integer, not bool
        >>> decimal_to_negative_base_2("10")
        Traceback (most recent call last):
        ...
        TypeError: num must be an integer, not str
        >>> decimal_to_negative_base_2(None)
        Traceback (most recent call last):
        ...
        TypeError: num must be an integer, not NoneType
        >>> decimal_to_negative_base_2(10**18)
        1001000100001110010111111010011111000101001000000000000000000
    """
    if isinstance(num, bool) or not isinstance(num, int):
        msg = f"num must be an integer, not {type(num).__name__}"
        raise TypeError(msg)
    if num == 0:
        return 0
    ans = ""
    while num != 0:
        num, rem = divmod(num, -2)
        if rem < 0:
            rem += 2
            num += 1
        ans = str(rem) + ans
    return int(ans)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
