# R23-T046 input probe evidence

The probes below were run against the original `strings/string_switch_case.py`
before the change. The input text was passed to all seven functions;
`to_complex_case` used `(input, False, "_")`, and `to_snake_case` and
`to_kebab_case` used `(input, False)`.

| Input | `split_input` | `to_simple_case` | `to_complex_case` | `to_pascal_case` | `to_camel_case` | `to_snake_case` | `to_kebab_case` |
|---|---|---|---|---|---|---|---|
| `None` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` |
| `123` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` |
| `["a", "b"]` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` | `TypeError` from `re.split` |
| `""` | `[[]]` | `""` | `""` | `""` | `"not valid string"` | `""` | `""` |
| `"   "` | `[[]]` | `""` | `""` | `""` | `"not valid string"` | `""` | `""` |
| `"---___!!!"` | ten empty groups (`[[], ...]`) | `""` | `""` | `""` | `"not valid string"` | `""` | `""` |
| `"12345"` | `[['12345']]` | `"12345"` | `"12345"` | `"12345"` | `"12345"` | `"12345"` | `"12345"` |
| `"café"` | `[['caf'], []]` | `"Caf"` | `"caf"` | `"Caf"` | `"caf"` | `"caf"` | `"caf"` |
| `"漢字"` | three empty groups (`[[], [], []]`) | `""` | `""` | `""` | `"not valid string"` | `""` | `""` |
| `"A" * 1_000_000` | returned one group | returned length 1,000,000 | returned length 1,000,000 | returned length 1,000,000 | returned length 1,000,000 | returned length 1,000,000 | returned length 1,000,000 |

## Decisions and resulting contract

- Require actual strings. `split_input` now raises `TypeError("input must be a
  string")` before calling the regex. All six conversion functions delegate
  through it, and each has a doctest for this error.
- Treat empty, whitespace-only, and separator-only text as valid input. The
  case converters return `""`; camel case no longer returns the misleading
  `"not valid string"` sentinel. `split_input` retains its grouped-list shape,
  including empty groups.
- Preserve digits, and preserve Unicode letters/digits rather than silently
  deleting them. Punctuation and underscore remain separators.
- Do not impose an arbitrary length limit: the one-million-character string
  probe completed for each function and returned the expected-length result.

After the change, focused probes confirmed the same `TypeError` contract for
all three non-string values, empty results for empty/separator-only inputs,
digit preservation, and Unicode outputs such as `CaféAuLait`,
`café_au_lait`, and `café-au-lait`.
