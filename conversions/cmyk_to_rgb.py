"""
Convert a CMYK colour (percentages) back to RGB (0..255).

This is the inverse of ``rgb_cmyk_conversion.rgb_to_cmyk``. CMYK values are
percentages of paint, so each channel is in the range 0..100:

    R = 255 * (1 - C/100) * (1 - K/100)
    G = 255 * (1 - M/100) * (1 - K/100)
    B = 255 * (1 - Y/100) * (1 - K/100)

``rgb_to_cmyk`` rounds to whole percentages, so the conversion is lossy and a
round trip rgb -> cmyk -> rgb can differ from the original by a few units per
channel. Like the forward algorithm, this is the simple linear formula and not a
colour-managed (ICC profile) conversion.

Reference: https://www.rapidtables.com/convert/color/cmyk-to-rgb.html
"""


def cmyk_to_rgb(
    c_input: int, m_input: int, y_input: int, k_input: int
) -> tuple[int, int, int]:
    """
    Simple CMYK to RGB conversion. Takes percentages (0..100) of CMYK paint and
    returns the RGB channels as integers in 0..255.

    >>> cmyk_to_rgb(0, 0, 0, 0)  # white
    (255, 255, 255)
    >>> cmyk_to_rgb(0, 0, 0, 100)  # black
    (0, 0, 0)
    >>> cmyk_to_rgb(0, 0, 0, 50)  # gray
    (128, 128, 128)
    >>> cmyk_to_rgb(0, 100, 100, 0)  # red
    (255, 0, 0)
    >>> cmyk_to_rgb(100, 0, 100, 0)  # green
    (0, 255, 0)
    >>> cmyk_to_rgb(100, 100, 0, 0)  # blue
    (0, 0, 255)

    Floats are accepted as long as they are in range:

    >>> cmyk_to_rgb(0.0, 50.0, 100.0, 0.0)
    (255, 128, 0)

    The inverse of rgb_to_cmyk, within rounding (+-1 per channel for these colours):

    >>> from conversions.rgb_cmyk_conversion import rgb_to_cmyk
    >>> cmyk_to_rgb(*rgb_to_cmyk(255, 0, 0))
    (255, 0, 0)
    >>> cmyk_to_rgb(*rgb_to_cmyk(0, 255, 0))
    (0, 255, 0)
    >>> cmyk_to_rgb(*rgb_to_cmyk(255, 255, 255))
    (255, 255, 255)
    >>> cmyk_to_rgb(*rgb_to_cmyk(0, 0, 0))
    (0, 0, 0)
    >>> cmyk_to_rgb(*rgb_to_cmyk(128, 128, 128))
    (128, 128, 128)
    >>> all(
    ...     abs(a - b) <= 1
    ...     for rgb in [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 128, 128)]
    ...     for a, b in zip(rgb, cmyk_to_rgb(*rgb_to_cmyk(*rgb)))
    ... )
    True

    Invalid input raises ValueError:

    >>> cmyk_to_rgb(0, 0, 0, "a")
    Traceback (most recent call last):
        ...
    ValueError: Expected int or float, found (<class 'int'>, <class 'int'>, \
<class 'int'>, <class 'str'>)
    >>> cmyk_to_rgb(0, 0, 0, 101)
    Traceback (most recent call last):
        ...
    ValueError: Expected a value in the range 0..100
    >>> cmyk_to_rgb(-1, 0, 0, 0)
    Traceback (most recent call last):
        ...
    ValueError: Expected a value in the range 0..100
    """
    inputs = (c_input, m_input, y_input, k_input)
    if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in inputs):
        msg = f"Expected int or float, found {tuple(type(x) for x in inputs)}"
        raise ValueError(msg)

    if not all(0 <= x <= 100 for x in inputs):
        raise ValueError("Expected a value in the range 0..100")

    # changing range from 0..100 to 0..1
    c, m, y, k = (x / 100 for x in inputs)

    r = round(255 * (1 - c) * (1 - k))
    g = round(255 * (1 - m) * (1 - k))
    b = round(255 * (1 - y) * (1 - k))

    return r, g, b


if __name__ == "__main__":
    from doctest import testmod

    testmod()
