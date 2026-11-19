def is_int_palindrome(num: int) -> bool:
    """
    Returns whether `num` is a palindrome or not
    (see for reference https://en.wikipedia.org/wiki/Palindromic_number).

    >>> is_int_palindrome(-121)
    False
    >>> is_int_palindrome(0)
    True
    >>> is_int_palindrome(10)
    False
    >>> is_int_palindrome(11)
    True
    >>> is_int_palindrome(101)
    True
    >>> is_int_palindrome(120)
    False
    >>> is_int_palindrome(7)
    True
    >>> is_int_palindrome(1210)
    False
    >>> is_int_palindrome(1234567890987654321)
    True
    >>> is_int_palindrome(12345678909876543210)
    False
    >>> is_int_palindrome("121")
    Traceback (most recent call last):
        ...
    TypeError: Input must be an integer
    >>> is_int_palindrome(12.21)
    Traceback (most recent call last):
        ...
    TypeError: Input must be an integer
    >>> is_int_palindrome(True)
    Traceback (most recent call last):
        ...
    TypeError: Input must be an integer
    """
    if not isinstance(num, int) or isinstance(num, bool):
        raise TypeError("Input must be an integer")

    if num < 0:
        return False

    num_copy: int = num
    rev_num: int = 0
    while num > 0:
        rev_num = rev_num * 10 + (num % 10)
        num //= 10

    return num_copy == rev_num


if __name__ == "__main__":
    import doctest

    doctest.testmod()
