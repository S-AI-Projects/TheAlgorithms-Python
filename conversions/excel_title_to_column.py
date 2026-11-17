def excel_title_to_column(column_title: str) -> int:
    """
    Given a string column_title that represents
    the column title in an Excel sheet, return
    its corresponding column number.

    Input Contract:
    - column_title must be an instance of str (TypeError raised otherwise).
    - column_title must be a non-empty string of ASCII letters
      (ValueError raised otherwise).
    - Lowercase column titles (e.g., 'a', 'ab') are accepted and handled
      by converting them to uppercase.

    >>> excel_title_to_column("A")
    1
    >>> excel_title_to_column("B")
    2
    >>> excel_title_to_column("AB")
    28
    >>> excel_title_to_column("Z")
    26
    >>> excel_title_to_column("a")
    1
    >>> excel_title_to_column("ab")
    28
    >>> excel_title_to_column("")
    Traceback (most recent call last):
        ...
    ValueError: Column title must contain only alphabetic characters.
    >>> excel_title_to_column("A1")
    Traceback (most recent call last):
        ...
    ValueError: Column title must contain only alphabetic characters.
    >>> excel_title_to_column(" A")
    Traceback (most recent call last):
        ...
    ValueError: Column title must contain only alphabetic characters.
    >>> excel_title_to_column("\u03b1")
    Traceback (most recent call last):
        ...
    ValueError: Column title must contain only alphabetic characters.
    >>> excel_title_to_column(123)
    Traceback (most recent call last):
        ...
    TypeError: column_title must be a str, got int
    >>> excel_title_to_column(None)
    Traceback (most recent call last):
        ...
    TypeError: column_title must be a str, got NoneType
    """
    if not isinstance(column_title, str):
        msg = f"column_title must be a str, got {type(column_title).__name__}"
        raise TypeError(msg)

    if not column_title or not column_title.isalpha() or not column_title.isascii():
        msg = "Column title must contain only alphabetic characters."
        raise ValueError(msg)

    column_title = column_title.upper()
    answer = 0
    index = len(column_title) - 1
    power = 0

    while index >= 0:
        value = (ord(column_title[index]) - 64) * pow(26, power)
        answer += value
        power += 1
        index -= 1

    return answer


if __name__ == "__main__":
    from doctest import testmod

    testmod()
