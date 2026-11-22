### Describe your change

* [ ] Add an algorithm?
* [ ] Fix a bug or typo in an existing algorithm?
* [x] Add or change doctests? -- Note: Please avoid changing both code and tests in a single pull request.
* [x] Documentation change?

### Checklist

* [x] I have read [CONTRIBUTING.md](https://github.com/TheAlgorithms/Python/blob/master/CONTRIBUTING.md).
* [x] This pull request is all my own work -- I have not plagiarized.
* [x] I know that pull requests will not be merged if they fail the automated tests.
* [x] This PR only changes one algorithm file. To ease review, please open separate PRs for separate algorithms.
* [x] All new Python files are placed inside an existing directory.
* [x] All filenames are in all lowercase characters with no spaces or dashes.
* [x] All functions and variable names follow Python naming conventions.
* [x] All function parameters and return values are annotated with Python [type hints](https://docs.python.org/3/library/typing.html).
* [x] All functions have [doctests](https://docs.python.org/3/library/doctest.html) that pass the automated testing.
* [x] All new algorithms include at least one URL that points to Wikipedia or another similar explanation.
* [ ] If this pull request resolves one or more open issues, then the description above includes the issue number(s) with a [closing keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue): "Fixes #ISSUE-NUMBER".

---

## Description

This pull request completes **Task R23-T025**: enhancing the documentation and empirical validation of Monte Carlo $\pi$ estimation in `maths/pi_monte_carlo_estimation.py`.

Key contributions include:
1. **Module Documentation**: Added a comprehensive top-level module docstring summarizing the mathematical principles of the Monte Carlo method and linking to authoritative Wikipedia references per repository guidelines.
2. **Seeded Doctest**: Added a deterministic seeded doctest verifying that an estimation with $N = 50,000$ and seed 42 achieves an absolute error $< 0.01$. All 3 existing doctests and the existing `ValueError` check remain intact and passing.
3. **Student Explainer (`work/R23-T025/EXPLAINER.md`)**: Complete walkthrough with mathematical derivation, ASCII & Mermaid diagrams, a hand-worked 10-point simulation table, and recorded classmate feedback re-deriving `estimate_pi(100, 1) == 3.2`.
4. **Convergence Experiment (`work/R23-T025/error_vs_n_plot.png`)**: Empirical demonstration of error convergence across $N \in [10^2, 10^6]$ plotted on a log-log scale against the theoretical $O(1/\sqrt{N})$ line.

## Type of Change

- [ ] Bug Fix
- [ ] New Feature
- [ ] UI/UX Improvement
- [ ] Performance Improvement
- [x] Tests
- [x] Documentation
- [ ] Refactoring / Maintenance
- [ ] CI/CD

## Changes Made

- `maths/pi_monte_carlo_estimation.py`:
  - Added module docstring explaining the ratio of areas and geometric probability.
  - Added reference links:
    - https://en.wikipedia.org/wiki/Monte_Carlo_method
    - https://en.wikipedia.org/wiki/Approximations_of_%CF%80#Monte_Carlo_methods
  - Added seeded doctest: `abs(estimate_pi(50000, 42) - math.pi) < 0.01` -> `True`.
  - Preserved all 3 existing doctests (`100, 1`, `1000, 11`, `1000000, 111`) and the `number_of_simulations < 1` raise path.
- `work/R23-T025/`:
  - `EXPLAINER.md`: Comprehensive student guide covering mathematical foundations, worked example, classmate verification, and empirical findings.
  - `experiment.py`: Simulation runner measuring convergence over 9 sample sizes and generating the log-log plot.
  - `error_vs_n_plot.png`: Dual-curve log-log visualization showing alignment with $1/\sqrt{N}$.
  - `test_output.txt`: Captured test execution logs.

## Empirical Convergence Summary

| Sample Size $N$ | Empirical Mean Error $|\hat{\pi} - \pi|$ | Theoretical $1/\sqrt{N}$ | Ratio |
|---|---|---|---|
| **100** | $0.059363$ | $0.100000$ | $0.59$ |
| **1,000** | $0.047281$ | $0.031623$ | $1.50$ |
| **10,000** | $0.013800$ | $0.010000$ | $1.38$ |
| **100,000** | $0.003951$ | $0.003162$ | $1.25$ |
| **1,000,000** | $0.000945$ | $0.001000$ | $0.95$ |

## Testing & Verification

- `python3 -m doctest -v maths/pi_monte_carlo_estimation.py` -> 4/4 doctests passed.
- `uv run --with pytest pytest --doctest-modules maths/pi_monte_carlo_estimation.py` -> 1 passed in 0.02s.
- `uvx ruff check maths/pi_monte_carlo_estimation.py work/R23-T025/experiment.py` -> All checks passed.
- `uvx ruff format --check maths/pi_monte_carlo_estimation.py work/R23-T025/experiment.py` -> 2 files already formatted.
- `uvx ty check --exit-zero maths/pi_monte_carlo_estimation.py` -> 0 diagnostics.

## Additional Notes

- A second clean branch `student/E26B07F0850/R23-T025-upstream` (and `R23-T025-upstream`) containing only the changes in `maths/pi_monte_carlo_estimation.py` has been created and pushed for a later upstream PR.
