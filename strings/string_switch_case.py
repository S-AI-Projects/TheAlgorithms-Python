import re

"""
general info:
https://en.wikipedia.org/wiki/Naming_convention_(programming)#Python_and_Ruby

pascal case [ an upper Camel Case ]: https://en.wikipedia.org/wiki/Camel_case

camel case: https://en.wikipedia.org/wiki/Camel_case

kebab case [ can be found in general info ]:
https://en.wikipedia.org/wiki/Naming_convention_(programming)#Python_and_Ruby

snake case: https://en.wikipedia.org/wiki/Snake_case
"""


# assistant functions
def split_input(str_: str) -> list[list[str]]:
    """
    Split a string into whitespace-separated word groups at punctuation.

    The input must be a string; otherwise, ``TypeError`` is raised. Unicode
    letters and digits are preserved, while underscores and punctuation split
    words.

    >>> split_input("one two 31235three4four")
    [['one', 'two', '31235three4four']]
    >>> split_input("---")
    [[], [], [], []]
    >>> split_input("café 日本語")
    [['café', '日本語']]
    >>> split_input(None)
    Traceback (most recent call last):
    ...
    TypeError: input must be a string
    """
    if not isinstance(str_, str):
        raise TypeError("input must be a string")
    return [char.split() for char in re.split(r"[^\w\s]|_", str_)]


def to_simple_case(str_: str) -> str:
    """
    Convert a string to simple case, preserving Unicode letters and digits.

    The input must be a string; otherwise, ``TypeError`` is raised. Empty or
    separator-only strings return an empty string.

    >>> to_simple_case("one two 31235three4four")
    'OneTwo31235three4four'
    >>> to_simple_case("This should be combined")
    'ThisShouldBeCombined'
    >>> to_simple_case("The first letters are capitalized, then string is merged")
    'TheFirstLettersAreCapitalizedThenStringIsMerged'
    >>> to_simple_case("special characters :, ', %, ^, $, are ignored")
    'SpecialCharactersAreIgnored'
    >>> to_simple_case("")
    ''
    >>> to_simple_case("---___!!!")
    ''
    >>> to_simple_case("café 日本語")
    'Café日本語'
    >>> to_simple_case(None)
    Traceback (most recent call last):
    ...
    TypeError: input must be a string
    """
    string_split = split_input(str_)
    return "".join(
        ["".join([char.capitalize() for char in sub_str]) for sub_str in string_split]
    )


def to_complex_case(text: str, upper: bool, separator: str) -> str:
    """
    Convert a string to upper or lower case words joined by ``separator``.

    The text must be a string; otherwise, ``TypeError`` is raised. Empty or
    separator-only text returns an empty string.

    Examples:
    >>> to_complex_case("one two 31235three4four", True, "_")
    'ONE_TWO_31235THREE4FOUR'
    >>> to_complex_case("one two 31235three4four", False, "-")
    'one-two-31235three4four'
    >>> to_complex_case("", False, "_")
    ''
    >>> to_complex_case("---___!!!", False, "_")
    ''
    >>> to_complex_case("café 日本語", False, "_")
    'café_日本語'
    >>> to_complex_case(None, False, "_")
    Traceback (most recent call last):
    ...
    TypeError: input must be a string
    """
    string_split = split_input(text)
    if upper:
        res_str = "".join(
            [
                separator.join([char.upper() for char in sub_str])
                for sub_str in string_split
            ]
        )
    else:
        res_str = "".join(
            [
                separator.join([char.lower() for char in sub_str])
                for sub_str in string_split
            ]
        )
    return res_str


# main content
def to_pascal_case(text: str) -> str:
    """
    Convert a string to Pascal case.

    The input must be a string; otherwise, ``TypeError`` is raised. Empty or
    separator-only strings return an empty string.

    >>> to_pascal_case("one two 31235three4four")
    'OneTwo31235three4four'
    >>> to_pascal_case("")
    ''
    >>> to_pascal_case("---")
    ''
    >>> to_pascal_case("café")
    'Café'
    >>> to_pascal_case(None)
    Traceback (most recent call last):
    ...
    TypeError: input must be a string
    """
    return to_simple_case(text)


def to_camel_case(text: str) -> str:
    """
    Convert a string to camel case.

    The input must be a string; otherwise, ``TypeError`` is raised. Empty or
    separator-only strings return an empty string.

    >>> to_camel_case("one two 31235three4four")
    'oneTwo31235three4four'
    >>> to_camel_case("")
    ''
    >>> to_camel_case("---")
    ''
    >>> to_camel_case("café 日本語")
    'café日本語'
    >>> to_camel_case(None)
    Traceback (most recent call last):
    ...
    TypeError: input must be a string
    """
    res_str = to_simple_case(text)
    return res_str[0].lower() + res_str[1:] if res_str else ""


def to_snake_case(text: str, upper: bool) -> str:
    """
    Convert a string to snake case.

    The input must be a string; otherwise, ``TypeError`` is raised. Empty or
    separator-only strings return an empty string.

    >>> to_snake_case("one two 31235three4four", True)
    'ONE_TWO_31235THREE4FOUR'
    >>> to_snake_case("one two 31235three4four", False)
    'one_two_31235three4four'
    >>> to_snake_case("", False)
    ''
    >>> to_snake_case("---", False)
    ''
    >>> to_snake_case("café 日本語", False)
    'café_日本語'
    >>> to_snake_case(None, False)
    Traceback (most recent call last):
    ...
    TypeError: input must be a string
    """
    return to_complex_case(text, upper, "_")


def to_kebab_case(text: str, upper: bool) -> str:
    """
    Convert a string to kebab case.

    The input must be a string; otherwise, ``TypeError`` is raised. Empty or
    separator-only strings return an empty string.

    >>> to_kebab_case("one two 31235three4four", True)
    'ONE-TWO-31235THREE4FOUR'
    >>> to_kebab_case("one two 31235three4four", False)
    'one-two-31235three4four'
    >>> to_kebab_case("", False)
    ''
    >>> to_kebab_case("---", False)
    ''
    >>> to_kebab_case("café 日本語", False)
    'café-日本語'
    >>> to_kebab_case(None, False)
    Traceback (most recent call last):
    ...
    TypeError: input must be a string
    """
    return to_complex_case(text, upper, "-")


if __name__ == "__main__":
    __import__("doctest").testmod()
