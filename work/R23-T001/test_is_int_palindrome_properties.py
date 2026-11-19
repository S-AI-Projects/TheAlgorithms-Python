import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from maths.is_int_palindrome import is_int_palindrome


@settings(max_examples=1000)
@given(n=st.integers(min_value=0))
def test_non_negative_integers(n: int) -> None:
    """
    Property: For all n >= 0, is_int_palindrome(n) must equal
    the string reversal equivalence: str(n) == str(n)[::-1].
    """
    expected = str(n) == str(n)[::-1]
    assert is_int_palindrome(n) == expected


@settings(max_examples=1000)
@given(n=st.integers(max_value=-1))
def test_negative_integers(n: int) -> None:
    """
    Property: For all n < 0, is_int_palindrome(n) is False.
    """
    assert is_int_palindrome(n) is False


@settings(max_examples=1000)
@given(
    prefix=st.integers(min_value=1, max_value=10**18),
    middle=st.integers(min_value=0, max_value=9),
    is_odd_length=st.booleans(),
)
def test_constructed_palindromes(prefix: int, middle: int, is_odd_length: bool) -> None:
    """
    Property: Any integer constructed by mirroring digits is palindromic.
    Includes large ints (up to 37+ digits).
    """
    prefix_str = str(prefix)
    if is_odd_length:
        pal_str = prefix_str + str(middle) + prefix_str[::-1]
    else:
        pal_str = prefix_str + prefix_str[::-1]
    pal_int = int(pal_str)
    assert is_int_palindrome(pal_int) is True


@settings(max_examples=1000)
@given(
    bad_input=st.one_of(
        st.floats(allow_nan=True, allow_infinity=True),
        st.text(),
        st.booleans(),
        st.none(),
        st.lists(st.integers()),
    )
)
def test_non_integer_inputs_raise_type_error(bad_input: object) -> None:
    """
    Property: Calling is_int_palindrome with non-integer inputs raises TypeError.
    """
    with pytest.raises(TypeError):
        is_int_palindrome(bad_input)  # type: ignore[arg-type]
