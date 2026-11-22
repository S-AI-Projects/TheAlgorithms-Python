"""
Probe inputs script for Task R23-T024.

Tests decimal_to_negative_base_2 on bad and edge-case inputs:
floats, bools, huge ints, non-numbers, negative numbers, etc.
Compares original vs. new behavior.
"""

import sys
from collections.abc import Callable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from maths.base_neg2_conversion import decimal_to_negative_base_2  # noqa: E402


# Unpatched / Original reference implementation
def original_decimal_to_negative_base_2(num: object) -> object:
    """Original implementation before contract checks."""
    if num == 0:
        return 0
    ans = ""
    while num != 0:
        num, rem = divmod(num, -2)  # type: ignore[operator]
        if rem < 0:
            rem += 2
            num += 1
        ans = str(rem) + ans
    return int(ans)


def run_and_format(fn: Callable[[object], object], val: object) -> str:
    """Execute function and return formatted output or caught exception."""
    try:
        res = fn(val)
        return f"`{res}` (returned value)"
    except Exception as e:  # noqa: BLE001
        return f"`{type(e).__name__}: {e}`"


PROBE_CASES: list[tuple[str, object]] = [
    ("Boolean True", True),
    ("Boolean False", False),
    ("Float (positive fractional)", 3.5),
    ("Float (integral zero)", 0.0),
    ("Float (negative fractional)", -2.5),
    ("String (digits)", "10"),
    ("String (empty)", ""),
    ("String (symbols)", "###"),
    ("NoneType", None),
    ("List collection", [1, 2]),
    ("Complex number", 1 + 2j),
    ("Huge integer", 10**18),
    ("Negative integer", -19),
    ("Zero integer", 0),
]


def main() -> None:
    print(
        "| Input Description | Test Value | Original (Old) Behavior |"
        " New Behavior | Status |"
    )
    print("|---|---|---|---|---|")
    for desc, val in PROBE_CASES:
        old_res = run_and_format(original_decimal_to_negative_base_2, val)
        new_res = run_and_format(decimal_to_negative_base_2, val)
        status = "Handled / Fixed" if old_res != new_res else "Preserved / Valid"
        print(f"| {desc} | `{val!r}` | {old_res} | {new_res} | {status} |")


if __name__ == "__main__":
    main()
