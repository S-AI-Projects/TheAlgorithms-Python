# Strict Ruff review: `geometry/braik_mac_construction.py`

The repository-configured check passed before edits. `uvx ruff check --select
ALL` reported 28 findings across ten rule codes. The choices below were based
on the rule descriptions in Ruff's documentation.

| Code | Count | Decision | Rationale |
| --- | ---: | --- | --- |
| [D205](https://docs.astral.sh/ruff/rules/missing-blank-line-after-summary/) | 3 | Fix | Separate each docstring summary from its description for PEP 257 readability. |
| [D212](https://docs.astral.sh/ruff/rules/multi-line-summary-first-line/) | 3 | Fix | Put each multiline docstring summary on the first physical line. |
| [CPY001](https://docs.astral.sh/ruff/rules/missing-copyright-notice/) | 1 | Leave | The file credits its author but has no verified copyright notice. Adding an invented owner or year would make an unsupported legal claim; the repository does not require this header. |
| [D400](https://docs.astral.sh/ruff/rules/missing-trailing-period/) | 2 | Fix | End docstring summaries with a period. |
| [D415](https://docs.astral.sh/ruff/rules/missing-terminal-punctuation/) | 2 | Fix | The same periods satisfy the broader terminal-punctuation rule. |
| [D105](https://docs.astral.sh/ruff/rules/undocumented-magic-method/) | 2 | Fix | Document the coordinate and point-count validation performed by both `__post_init__` methods. |
| [TRY003](https://docs.astral.sh/ruff/rules/raise-vanilla-args/) | 4 | Fix | Move the validation messages out of the `TypeError` calls; introducing custom exception classes for these simple checks would be unnecessary. |
| [EM101](https://docs.astral.sh/ruff/rules/raw-string-in-exception/) | 4 | Fix | Bind each message to a local variable before raising, avoiding inline string literals while preserving exception type and text. |
| [D102](https://docs.astral.sh/ruff/rules/undocumented-public-method/) | 1 | Fix | Document the public `generate` property. |
| [COM812](https://docs.astral.sh/ruff/rules/missing-trailing-comma/) | 6 | Fix | Add trailing commas to the multiline matrix rows for smaller, clearer future diffs. |

No naming (`N`) rule produced a finding. The determinant coefficients `a` through
`f` are kept as conventional mathematical names. Ruff also reports configured
rule conflicts for D203/D211 and D212/D213; it ignores D203 and D213, so these
configuration warnings are not file findings.

## Baseline

`uvx ruff check geometry/braik_mac_construction.py` passed before changes.
The complete baseline output is saved in `ruff-all-before.txt`.

## Final result

The selected clarity/style findings were fixed. The repo-configured Ruff check
passes, and strict `--select ALL` now reports only CPY001, which is intentionally
left for the reason above. The configured D203/D211 and D212/D213 conflict
warnings remain unchanged. The seven doctests pass, and a focused runtime check
confirmed that all four `TypeError` paths retain their original types and
messages. The final strict and repository-configured outputs are saved in
`ruff-all-after.txt` and `ruff-config-after.txt`; doctest and exception summaries
are recorded in `doctest-summary.txt` and `exception-check.txt`.
