# R23-T052: conversions/cmyk_to_rgb.py

## What it does
`cmyk_to_rgb(c, m, y, k)` is the inverse of `rgb_cmyk_conversion.rgb_to_cmyk`.
Inputs are percentages of paint (0..100); output is `(r, g, b)` in 0..255:

    R = 255 * (1 - C/100) * (1 - K/100)   (same for G with M, B with Y)

It raises `ValueError` for non-numeric input or values outside 0..100.

## How it differs from rgb_to_cmyk (time / space)
| | rgb_to_cmyk | cmyk_to_rgb |
|---|---|---|
| Time | O(1) | O(1) |
| Space | O(1) | O(1) |
| Measured (20,000 random colours, avg per call) | ~0.70 us | ~1.87 us |

Both are constant time and constant space. `cmyk_to_rgb` is slower per call
only because of its generic validation (`all(isinstance(...))` and
`all(0 <= x <= 100)` over a 4-tuple); the arithmetic itself is just 3 multiplications
and 3 roundings. Timings are from one run on a cloud machine, so treat them as
rough.

## Why the round trip is not exact (rounding)
`rgb_to_cmyk` rounds C, M, Y and K to **whole percentages**. That throws away
information: 256 levels per RGB channel are squeezed into 101 levels per CMYK
channel. Converting back cannot recover the lost detail, so rgb -> cmyk -> rgb
can be off by a few units.

Each CMYK value can be off by up to 0.5 percent, and R depends on two of them
(C and K), so the worst case error is about 2 per channel. Measured over a
grid of every 5th value per channel (140,608 colours):

| max error per channel | colours |
|---|---|
| 0 | 27,214 |
| 1 | 106,608 |
| 2 | 6,786 |

(A larger sample of every 3rd value, 636,056 colours, also had a maximum error
of 2.) So "within +-1 per channel" holds for most colours and for the colours
used in the doctests (red, green, blue, white, black and mid-gray), but not for
every possible colour. The doctest checks the cases that do hold; this file
documents the limit.

## Checks run
- `python3 scripts/validate_filenames.py` -> passed
- `ruff check conversions/cmyk_to_rgb.py` -> all checks passed
- `ruff format --check conversions/cmyk_to_rgb.py` -> already formatted
- `python -m pytest --doctest-modules conversions/cmyk_to_rgb.py conversions/rgb_cmyk_conversion.py` -> passed
