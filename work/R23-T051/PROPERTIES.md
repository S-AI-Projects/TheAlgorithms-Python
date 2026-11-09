# Properties tested: maths/points_are_collinear_3d.py

Run with: `python -m pytest work/R23-T051/ -v` (Hypothesis, 2000 examples per test).

## Properties

1. **Exact collinearity (integers).** For integer A, v, t, s, the points A, B = A + t*v and C = A + s*v lie on one line, so the cross product of AB and AC is exactly zero and `are_collinear` must return True. Integer arithmetic is exact, so no rounding is involved.
2. **Float collinearity.** The same property with float inputs (coordinates in [-100, 100], scalars in [-10, 10]). Floating-point error makes the cross product only approximately zero, so this test uses `accuracy=6`.
3. **Perturbation.** Moving C off the line by a vector w that is not parallel to v (cross(v, w) != 0, t != 0) gives a non-zero cross product, so `are_collinear` must return False. Integer inputs are used so the cross product is an exact non-zero integer vector.

## Findings

- All three properties passed over 2000 random examples each; Hypothesis found no failing input.
- The result depends on `accuracy`, because `is_zero_vector` rounds each cross-product component to that many decimals before comparing with zero. A deviation that is real but smaller than 10**-accuracy is treated as collinear. For example, with A=(0,0,0), B=(1,0,0), C=(2,1e-6,0) the cross product is (0, 0, 1e-6): `are_collinear` returns False at the default accuracy=10 but True at accuracy=5. Likewise a 1e-9 deviation is True at accuracy=8 and False at accuracy=10.
- These boundary cases are now documented as doctests in `are_collinear` (18 doctests pass: the original 14 plus 4 new).
- Limitation: the check uses an absolute tolerance, not a relative one, so for very large coordinates floating-point error can exceed the tolerance, and for very small coordinates real deviations can be rounded away.
