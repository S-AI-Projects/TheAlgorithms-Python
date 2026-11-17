# Octal-to-hexadecimal properties

`test_octal_to_hexadecimal_properties.py` uses Hypothesis with 2,000 examples
for each property.

- **Minimal counterexample found:** the valid-string property shrank a failure
  to `"0"`: the converter returned `"0x"` while `hex(int("0", 8))` is `"0x0"`.
  The converter now returns `"0x0"` for zero; doctests cover both `"0"` and
  leading-zero input `"000"`.
- **Valid octal strings match Python's reference:** generated nonempty strings
  contain only octal digits, with or without the accepted `0o` prefix. The
  expected value is `hex(int(s, 8))` normalized to the function's documented
  uppercase hexadecimal digits and `0x` prefix. Generated strings also cover
  leading zeros and zero itself.
- **Invalid octal digits raise:** generated strings contain an `8` or `9`,
  optionally following the accepted `0o` prefix. The function must raise
  `ValueError` rather than return a conversion.

## Results

- Both property tests pass with 2,000 examples each using
  `uv run --with hypothesis --with pytest python -m pytest work/R23-T042/`.
- The converter's 10 doctests pass, and `pytest conversions` passes all 82
  tests.
- The exact suggested command `uv run --with hypothesis pytest work/R23-T042/`
  does not expose Hypothesis to this environment's `pytest` launcher. Running
  pytest as a module with both dependencies explicitly supplied succeeds.
- A repository-wide pytest run hits `scripts/validate_filenames.py`, which
  rejects the required uppercase/hyphenated `work/R23-T042/` path. Per task
  guidance, the filename validator was left unchanged.
