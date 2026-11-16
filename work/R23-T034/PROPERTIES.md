# Edit-distance property checks

`test_edit_distance_properties.py` uses Hypothesis to check each property on
1,000 generated examples. Strings are bounded to length five so the current
recursive implementation can be exercised over thousands of cases efficiently.
The four tests execute 4,000 generated examples total.

The function uses unit-cost insertion, deletion, and substitution. For that
Levenshtein distance:

| Property | Hypothesis check | Why it should hold |
|---|---|---|
| Identity | `d(a, a) == 0` | No edits are needed to transform a string into itself. |
| Symmetry | `d(a, b) == d(b, a)` | Every insertion in one direction corresponds to a deletion in reverse; substitutions are symmetric. |
| Triangle inequality | `d(a, c) <= d(a, b) + d(b, c)` | Transforming `a` to `b`, then `b` to `c`, is a valid route from `a` to `c`; the shortest route cannot cost more. |
| Length bounds | `abs(len(a)-len(b)) <= d(a,b) <= max(len(a),len(b))` | At least the length difference in insertions/deletions is required. Substituting the overlapping positions and inserting or deleting the remaining characters costs at most the longer string's length. |

All properties passed. Hypothesis found no counterexamples in the generated
examples. Non-string inputs are separately rejected with `TypeError` and a
doctest.
