# Electrical conductivity

## Idea

This function uses the relationship

```text
σ = n · q · μ
```

where `σ` is electrical conductivity, `n` is electron concentration, `q` is
the magnitude of the electron charge, and `μ` is electron mobility. The code
uses `q = 1.6021 × 10⁻¹⁹ C`. Pass the known values as `conductivity`,
`electron_conc`, and `mobility`; use exactly one `0` to mark the quantity to
calculate. The function returns a pair containing the name of the calculated
quantity and its value.

The implementation first checks that exactly one argument is zero, then
rejects negative values. It calculates conductivity when `conductivity` is
zero, electron concentration when `electron_conc` is zero, and mobility
otherwise (the earlier check ensures `mobility` must be zero in that case).
The equations are the original relationship rearranged for the unknown:

```text
σ = n · q · μ       n = σ / (q · μ)       μ = σ / (n · q)
```

## Worked example by hand

Re-derive the existing electron-concentration doctest with
`conductivity = 1000 S/m` and `mobility = 1200 m²/(V·s)`:

```text
n = σ / (q · μ)
  = 1000 / (1.6021 × 10⁻¹⁹ × 1200)
  = 5.201506356240767 × 10¹⁸ m⁻³
```

Thus `electric_conductivity(conductivity=1000, electron_conc=0, mobility=1200)`
returns `("electron_conc", 5.201506356240767e+18)`.

## Units experiment

The dimensions below use `C = A·s` and `S = A/V`. Each rearrangement returns
the expected unit for its unknown.

| Quantity solved for | Rearranged expression | Unit calculation | Resulting unit |
| --- | --- | --- | --- |
| Conductivity `σ` | `n · q · μ` | `m⁻³ · C · m²/(V·s) = C/(m·V·s) = A/(m·V)` | `S/m` |
| Electron concentration `n` | `σ/(q · μ)` | `(S/m) / (C·m²/(V·s)) = (A/(V·m)) / (A·s·m²/(V·s))` | `m⁻³` |
| Mobility `μ` | `σ/(n · q)` | `(S/m) / (m⁻³·C) = (A/(V·m)) / (m⁻³·A·s)` | `m²/(V·s)` |

## Decision diagram

```text
                  conductivity, electron_conc, mobility
                                  |
                      exactly one value is 0?
                         /               \
                       no                 yes
                       |                   |
                 raise ValueError    any value negative?
                                        /          \
                                      yes           no
                                       |             |
                                 raise ValueError  conductivity == 0?
                                                   /          \
                                                 yes           no
                                                  |             |
                                        σ = n · q · μ      electron_conc == 0?
                                                            /          \
                                                          yes           no
                                                           |             |
                                                   n = σ / (q · μ)  μ = σ / (n · q)
```

The eight existing doctest examples (three calculations and five error
examples) and the four existing `ValueError` paths are unchanged by this
documentation update.

## Peer re-derivation feedback

Pending: a classmate should independently re-derive the doctest result above
from this explainer. Feedback has not yet been collected; it is intentionally
not represented as completed.

Reference: [Electrical resistivity and conductivity](https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity).
