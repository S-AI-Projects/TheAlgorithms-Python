"""Small driver to step through with pdb (run from the repo root).

    python -m pdb work/R23-T055/trace_driver.py

Useful pdb commands:  b maths/chinese_remainder_theorem.py:30   c   p a, b, x, y, k   w   n   s
"""

import sys

sys.path.insert(0, ".")
from maths.chinese_remainder_theorem import chinese_remainder_theorem, extended_euclid

print("extended_euclid(10, 6) =", extended_euclid(10, 6))
print("chinese_remainder_theorem(5, 1, 7, 3) =", chinese_remainder_theorem(5, 1, 7, 3))
