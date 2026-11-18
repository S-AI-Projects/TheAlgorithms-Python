# R23-T045 CI notes

## What CI tests for this file

`.github/workflows/build.yml` installs the test group and runs pytest over the
repository with eight iterations and automatic parallel threads. It enables
coverage for the repository (`--cov=.`) and reports missing lines. The ignored
paths are three computer-vision files, one data-compression file, the
`digital_image_processing/` and `project_euler/` trees, `docs/conf.py`,
`scripts/validate_solutions.py`, and two web-programming files. The
`machine_learning/random_forest_classifier.py` file is not ignored.

The workflow uses `--ignore-gil-enabled` because some scientific packages,
including scikit-learn, do not yet support the free-threaded Python build. The
flag permits those tests to run despite those upstream wheel limitations.

`pyproject.toml` configures pytest with `--doctest-modules`, so pytest looks
for examples in module and function docstrings. Before this change, the target
file had no doctests; its only function was `main()`, whose demo is guarded by
`if __name__ == "__main__"`. Pytest does not call `main()` just by importing
the module. Thus CI collected no test from this file, though importing it
executes its imports. Running the requested focused coverage command before
the change confirmed this: it reported `collected 0 items`, `no tests ran`,
and exit status 5. The module showed 41% coverage from import-time execution
alone.

After adding `random_forest_accuracy()` and its doctest, the focused run
collected and passed one test. Coverage for this module was 57%; the remaining
uncovered lines include the still-manual `main()` demo. The command's
`--cov=machine_learning` option also reports every module in that package, not
only the requested file.

## Directory and filename scripts

`DIRECTORY.md` lists the file in the Machine Learning section as
`Random Forest Classifier` at line 784. `scripts/build_directory_md.py` gets
paths from `good_file_paths()`, which walks Python and notebook files outside
the scripts, hidden, and virtual-environment directories, excluding
`__init__.py`. It formats this snake-case filename into the display title and
links to the Python path. CI regenerates `DIRECTORY.md` after a successful
test run; it should not be hand-edited.

`scripts/validate_filenames.py` uses the same path enumeration and checks for
uppercase characters, spaces, hyphens, and Python files outside a directory.
`machine_learning/random_forest_classifier.py` meets those checks: its name is
lowercase with underscores and it is inside a directory.

## Validation evidence

- Before the change,
  `uv run pytest machine_learning/random_forest_classifier.py --cov=machine_learning --cov-report=term-missing -v`
  collected 0 items and exited 5.
- After the change, the same command passed: 1 doctest passed; the target
  module reported 57% coverage.
- `uv run pytest machine_learning/random_forest_classifier.py -v` passed:
  1 doctest passed.
- `uv run pytest machine_learning -v` ran 193 doctests: 192 passed and 1
  unrelated existing doctest failed in
  `machine_learning/linear_discriminant_analysis.py`. Its expected float was
  `6.4494456086997705`, while this run returned `6.449445608699771`.
- `uvx ruff check machine_learning/random_forest_classifier.py` and
  `uvx ruff format --check machine_learning/random_forest_classifier.py`
  passed. The attempted equivalent `uv run ruff ...` command could not start
  because Ruff is not installed in the project environment; `uvx` supplied
  the tool without changing project dependencies.
