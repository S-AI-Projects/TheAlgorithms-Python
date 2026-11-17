"""Hypothesis property tests for ciphers/base32.py (Task R23-T014)."""

import base64
import sys
import os

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from hypothesis import given, settings
from hypothesis import strategies as st

from ciphers.base32 import base32_decode, base32_encode


@settings(max_examples=1000)
@given(st.binary())
def test_encode_matches_standard_base64_reference(b: bytes) -> None:
    """Property: base32_encode(b) must match Python's base64.b32encode(b) for any bytes."""
    assert base32_encode(b) == base64.b32encode(b)


@settings(max_examples=1000)
@given(st.binary())
def test_decode_roundtrip_property(b: bytes) -> None:
    """Property: base32_decode(base32_encode(b)) must equal original bytes b for any bytes."""
    encoded = base32_encode(b)
    decoded = base32_decode(encoded)
    assert decoded == b
