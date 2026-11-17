# Property-Based Testing for `ciphers/base32.py` (Task R23-T014)

## Overview
Using `hypothesis`, we tested `ciphers/base32.py` against Python's built-in `base64` reference module over 1,000 random inputs per property.

## Properties Tested
1. **Reference Agreement**:
   $$\forall b \in \text{bytes},\quad \text{base32\_encode}(b) = \text{base64.b32encode}(b)$$
   Tested by `test_encode_matches_standard_base64_reference`.
2. **Round-Trip Invertibility**:
   $$\forall b \in \text{bytes},\quad \text{base32\_decode}(\text{base32\_encode}(b)) = b$$
   Tested by `test_decode_roundtrip_property`.

## Bugs Uncovered by Property Tests
1. **Empty input (`b""`) padding flaw**:
   - `base32_encode(b"")` erroneously returned `b"A======="` instead of `b""` due to unhandled 0-length calculation in `5 * ((len // 5) + 1)`.
2. **Multiple-of-5 byte length padding flaw** (`len % 5 == 0`, e.g., length 5 `b"AAAAA"`):
   - `base32_encode(b"AAAAA")` erroneously appended an extra 8 characters `A=======` (`b'IFAUCQKBA======='` vs expected `b'IFAUCQKB'`).
3. **Arbitrary byte values (non-UTF8 bytes, e.g. `b"\xff"`)**:
   - The original code called `.decode("utf-8")` on raw input bytes, crashing with `UnicodeDecodeError` on non-UTF-8 bytes.
   - The decode function used `chr()` and `.encode("utf-8")`, which corrupts bytes with values $\ge 128$.
4. **Invalid decode characters**:
   - Decoding inputs with non-base32 symbols (e.g. `b"INVALID!"`) now raises a clear `ValueError`.

## Fixes & Test Vectors Added
- Added RFC 4648 test vectors covering all padding lengths 0 to 5 (`b""`, `b"f"`, `b"fo"`, `b"foo"`, `b"foob"`, `b"fooba"`).
- Added test vectors for arbitrary byte values (`b"\xff"`).
- Added invalid character decode doctest (`b"INVALID!"`).
- All 6 existing doctests pass unchanged.
