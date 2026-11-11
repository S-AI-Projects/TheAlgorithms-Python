"""Probe ciphers/porta_cipher.py with bad inputs and print a markdown table.

Run from the repo root:  python work/R23-T053/probe_bad_inputs.py
"""

import sys

sys.path.insert(0, ".")
from ciphers.porta_cipher import decrypt, encrypt, generate_table

CASES = [
    ("empty key", encrypt, ("", "hello")),
    ("digits in key", encrypt, ("ab1", "hello")),
    ("space in key", encrypt, ("my key", "hello")),
    ("non-ASCII letter in key", encrypt, ("clé", "hello")),
    ("german sharp s in key", encrypt, ("ß", "hello")),
    ("key is None", encrypt, (None, "hello")),
    ("key is int", encrypt, (123, "hello")),
    ("key is bytes", encrypt, (b"key", "hello")),
    ("text is None", encrypt, ("key", None)),
    ("text has a space", encrypt, ("key", "hello world")),
    ("text has digits", encrypt, ("key", "abc123")),
    ("empty text, valid key", encrypt, ("key", "")),
    ("mixed-case key and text", encrypt, ("MaRvIn", "JeSsIcA")),
    ("generate_table(empty key)", generate_table, ("",)),
    ("generate_table(None)", generate_table, (None,)),
    ("decrypt, empty key", decrypt, ("", "QRACRWU")),
    ("decrypt, text has digit", decrypt, ("marvin", "QRA1")),
    ("very long key (10**6 letters)", encrypt, ("a" * 10**6, "hi")),
]

print("| # | Input | Function | Result |")
print("|---|---|---|---|")
for i, (label, func, args) in enumerate(CASES, 1):
    shown = tuple(a if len(repr(a)) < 25 else "<long>" for a in args)
    try:
        out = func(*args)
        res = f"returns `{out!r}`" if len(repr(out)) < 60 else "returns (long result)"
    except Exception as e:  # noqa: BLE001
        res = f"raises `{type(e).__name__}: {e}`"
    print(f"| {i} | {label} `{shown}` | `{func.__name__}` | {res} |")
