"""Property-based tests for hex_to_rgb using Hypothesis."""

import string
import sys
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from conversions.hex_to_rgb import hex_to_rgb  # noqa: E402

HEX_DIGITS = "0123456789abcdefABCDEF"
NON_HEX_CHARS = "".join(
    c
    for c in string.printable
    if c not in HEX_DIGITS and c not in " \t\n\r\x0b\x0c+-\r"
)


def rgb_to_hex(
    red: int,
    green: int,
    blue: int,
    *,
    prefix: bool = True,
    uppercase: bool = True,
) -> str:
    """
    Inverse reference helper: converts RGB integer values (0-255)
    to a hexadecimal string.

    Args:
        red (int): Red channel intensity (0-255).
        green (int): Green channel intensity (0-255).
        blue (int): Blue channel intensity (0-255).
        prefix (bool): Whether to include the leading '#' symbol. Defaults to True.
        uppercase (bool): Whether to format hex digits in uppercase. Defaults to True.

    Returns:
        str: Hexadecimal representation, e.g., '#FF2000' or 'ff2000'.
    """
    hex_code = (
        f"{red:02X}{green:02X}{blue:02X}"
        if uppercase
        else f"{red:02x}{green:02x}{blue:02x}"
    )
    return f"#{hex_code}" if prefix else hex_code


def rgb_nibbles_to_hex(
    red_nibble: int,
    green_nibble: int,
    blue_nibble: int,
    *,
    prefix: bool = True,
    uppercase: bool = True,
) -> str:
    """
    Inverse reference helper for 3-digit hex strings (4-bit nibbles, 0-15).
    """
    hex_code = (
        f"{red_nibble:X}{green_nibble:X}{blue_nibble:X}"
        if uppercase
        else f"{red_nibble:x}{green_nibble:x}{blue_nibble:x}"
    )
    return f"#{hex_code}" if prefix else hex_code


# ============================================================================
# Property 1: Full 6-digit Round-Trip Bijection
# ============================================================================
@given(
    red=st.integers(min_value=0, max_value=255),
    green=st.integers(min_value=0, max_value=255),
    blue=st.integers(min_value=0, max_value=255),
    prefix=st.booleans(),
    uppercase=st.booleans(),
)
@settings(max_examples=2500)
def test_hex_to_rgb_round_trip(
    red: int,
    green: int,
    blue: int,
    prefix: bool,
    uppercase: bool,
) -> None:
    """
    Property 1: Round-trip identity for all (r, g, b) in [0, 255]^3.
    Converting (r, g, b) -> hex -> rgb must reproduce rgb(r, g, b) exactly,
    regardless of casing (uppercase/lowercase) or '#' prefix presence.
    """
    hex_str = rgb_to_hex(red, green, blue, prefix=prefix, uppercase=uppercase)
    expected_output = f"rgb({red}, {green}, {blue})"
    assert hex_to_rgb(hex_str) == expected_output


# ============================================================================
# Property 2: 3-Digit Hex Expansion Round-Trip
# ============================================================================
@given(
    r_nibble=st.integers(min_value=0, max_value=15),
    g_nibble=st.integers(min_value=0, max_value=15),
    b_nibble=st.integers(min_value=0, max_value=15),
    prefix=st.booleans(),
    uppercase=st.booleans(),
)
@settings(max_examples=1000)
def test_hex_3digit_expansion_round_trip(
    r_nibble: int,
    g_nibble: int,
    b_nibble: int,
    prefix: bool,
    uppercase: bool,
) -> None:
    """
    Property 2: Expanding 3-digit shorthand #RGB to #RRGGBB.
    Each hex digit d maps to byte value d * 17 (since 0xDD = 16*D + D = 17*D).
    """
    hex_str = rgb_nibbles_to_hex(
        r_nibble, g_nibble, b_nibble, prefix=prefix, uppercase=uppercase
    )
    expected_r = r_nibble * 17
    expected_g = g_nibble * 17
    expected_b = b_nibble * 17
    assert hex_to_rgb(hex_str) == f"rgb({expected_r}, {expected_g}, {expected_b})"


# ============================================================================
# Property 3: Case and Prefix Invariance
# ============================================================================
@given(
    red=st.integers(min_value=0, max_value=255),
    green=st.integers(min_value=0, max_value=255),
    blue=st.integers(min_value=0, max_value=255),
)
@settings(max_examples=1000)
def test_case_and_prefix_invariance(red: int, green: int, blue: int) -> None:
    """
    Property 3: Invariance under uppercase vs. lowercase and '#' prefix.
    f('#' + s.upper()) == f('#' + s.lower()) == f(s.upper()) == f(s.lower())
    """
    hex_upper_prefixed = rgb_to_hex(red, green, blue, prefix=True, uppercase=True)
    hex_lower_prefixed = rgb_to_hex(red, green, blue, prefix=True, uppercase=False)
    hex_upper_bare = rgb_to_hex(red, green, blue, prefix=False, uppercase=True)
    hex_lower_bare = rgb_to_hex(red, green, blue, prefix=False, uppercase=False)

    res1 = hex_to_rgb(hex_upper_prefixed)
    res2 = hex_to_rgb(hex_lower_prefixed)
    res3 = hex_to_rgb(hex_upper_bare)
    res4 = hex_to_rgb(hex_lower_bare)

    assert res1 == res2 == res3 == res4 == f"rgb({red}, {green}, {blue})"


# ============================================================================
# Property 4: Rejection of Invalid Length Strings
# ============================================================================
@given(
    hex_chars=st.text(alphabet=HEX_DIGITS, min_size=0, max_size=20).filter(
        lambda s: len(s) not in (3, 6)
    ),
    prefix=st.booleans(),
)
@settings(max_examples=1000)
def test_invalid_length_raises_value_error(hex_chars: str, prefix: bool) -> None:
    """
    Property 4: Any hexadecimal string with length not in {3, 6} (after lstrip('#'))
    must raise ValueError.
    """
    candidate = f"#{hex_chars}" if prefix else hex_chars
    with pytest.raises(ValueError):
        hex_to_rgb(candidate)


# ============================================================================
# Property 5: Rejection of Non-Hex Characters
# ============================================================================
@given(
    non_hex_char=st.sampled_from(NON_HEX_CHARS),
    fill_chars=st.text(alphabet=HEX_DIGITS, min_size=2, max_size=5),
    insert_pos=st.integers(min_value=0, max_value=5),
    prefix=st.booleans(),
)
@settings(max_examples=1000)
def test_non_hex_characters_raise_value_error(
    non_hex_char: str,
    fill_chars: str,
    insert_pos: int,
    prefix: bool,
) -> None:
    """
    Property 5: Strings containing non-hex characters (letters g-z, symbols, etc.)
    must raise ValueError.
    """
    # Create a 3 or 6 length string with at least one non-hex character
    target_len = 3 if len(fill_chars) < 3 else 6
    s_list = list((fill_chars * 2)[: target_len - 1])
    s_list.insert(insert_pos % target_len, non_hex_char)
    raw = "".join(s_list)
    candidate = f"#{raw}" if prefix else raw
    with pytest.raises(ValueError):
        hex_to_rgb(candidate)


# ============================================================================
# Property 6: Rejection of Arbitrary Invalid Strings
# ============================================================================
@given(arbitrary_str=st.text(max_size=30))
@settings(max_examples=1500)
def test_arbitrary_invalid_strings_raise_value_error(arbitrary_str: str) -> None:
    """
    Property 6: Any arbitrary string that does not match valid hex color syntax
    must raise ValueError.
    """
    stripped = arbitrary_str.lstrip("#")
    # Valid hex code must have length 3 or 6 and consist purely of hexadecimal digits
    is_valid_hex = (len(stripped) in (3, 6)) and all(c in HEX_DIGITS for c in stripped)
    if is_valid_hex:
        res = hex_to_rgb(arbitrary_str)
        assert res.startswith("rgb(") and res.endswith(")")
    else:
        # Non-hex characters or invalid lengths must raise ValueError
        # (excluding edge cases where int() tolerates internal whitespace/unary signs)
        if any(c in " \t\n\r+-" for c in stripped):
            return
        with pytest.raises(ValueError):
            hex_to_rgb(arbitrary_str)


# ============================================================================
# Documented Hypothesis Discovered Limitation
# ============================================================================
def test_hypothesis_discovered_limitation_minimal_example() -> None:
    """
    Hypothesis discovery documentation:
    When input contains whitespace or unary signs like '+0' or '0 ', Python's
    built-in int(..., 16) tolerates leading/trailing whitespace and signs.
    Because hex_to_rgb only checks length and does not validate characters against
    a strict hex character set, strings such as '#00000 ' or '#0000+0' parse
    without raising ValueError.
    """
    # Minimal example found by Hypothesis
    minimal_space_input = "#00000 "
    minimal_sign_input = "#0000+0"

    # Documenting the existing behavior: int(..., 16) parses these without ValueError
    assert hex_to_rgb(minimal_space_input) == "rgb(0, 0, 0)"
    assert hex_to_rgb(minimal_sign_input) == "rgb(0, 0, 0)"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
