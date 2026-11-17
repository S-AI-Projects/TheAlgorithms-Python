import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from conversions.octal_to_hexadecimal import octal_to_hex


@settings(max_examples=2_000, deadline=None)
@given(
    digits=st.text(alphabet="01234567", min_size=1, max_size=64),
    has_prefix=st.booleans(),
)
def test_valid_octal_strings_match_python_reference(
    digits: str, has_prefix: bool
) -> None:
    octal = f"0o{digits}" if has_prefix else digits
    expected = f"0x{hex(int(octal, 8))[2:].upper()}"

    assert octal_to_hex(octal) == expected


@settings(max_examples=2_000, deadline=None)
@given(
    prefix=st.sampled_from(("", "0o")),
    before=st.text(alphabet="01234567", max_size=64),
    invalid_digit=st.sampled_from(("8", "9")),
    after=st.text(alphabet="01234567", max_size=64),
)
def test_octal_strings_with_invalid_digits_raise(
    prefix: str, before: str, invalid_digit: str, after: str
) -> None:
    octal = f"{prefix}{before}{invalid_digit}{after}"

    with pytest.raises(ValueError, match="Not a Valid Octal Number"):
        octal_to_hex(octal)
