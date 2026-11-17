"""Probe script for conversions/excel_title_to_column.py input hardening (Task R23-T011)."""

import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from typing import Any
from conversions.excel_title_to_column import excel_title_to_column


def probe(input_val: Any) -> str:
    try:
        res = excel_title_to_column(input_val)
        return f"Returned {res}"
    except Exception as e:
        return f"{type(e).__name__}: {e}"


if __name__ == "__main__":
    test_cases = [
        ("", "Empty string"),
        ("a", "Lowercase single letter"),
        ("A1", "Alphanumeric with digit"),
        (" A", "Leading space"),
        ("ZZZZ", "Large valid title"),
        (123, "Integer (non-string)"),
        (None, "None (non-string)"),
        (["A"], "List of string (non-string)"),
        ("α", "Non-ASCII Greek letter (Unicode alpha)"),
        ("A B", "Title with internal space"),
        (-5, "Negative integer"),
        (3.14, "Float (non-string)"),
    ]

    print(f"{'Input':<12} | {'Description':<40} | {'Behavior'}")
    print("-" * 90)
    for val, desc in test_cases:
        outcome = probe(val)
        print(f"{repr(val):<12} | {desc:<40} | {outcome}")
