# CI and repository tooling notes: Burkes dithering

## How CI collects and reports tests

`pyproject.toml` configures pytest with:

```toml
[tool.pytest]
ini_options.addopts = [
  "--durations=10",
  "--doctest-modules",
  "--showlocals",
]
```

Thus pytest collects examples from Python docstrings. The build workflow runs
pytest with `--iterations=8 --parallel-threads=auto --ignore-gil-enabled`,
coverage over the repository (`--cov=. .`), and
`--cov-report=term-missing:skip-covered`.

The workflow explicitly skips this tree:

```text
--ignore=digital_image_processing/
```

The adjacent comment explains the reason: `opencv-python` is gated out on
Python 3.15t because there is no `cp315t` wheel yet. Most files in
`digital_image_processing/` import `cv2`, so the workflow skips the tree;
pure-Python algorithms in `computer_vision/` and `data_compression/` remain
eligible. The skip should be removed when OpenCV publishes a compatible
free-threaded wheel.

## Python 3.12 local run

The exact requested `uv run --python 3.12 ...` invocation initially failed
before pytest started: the project declares `requires-python = ">=3.15"`.
Using `uv run --no-project --python 3.12` bypasses that project constraint and
lets uv create an isolated CPython 3.12 environment with NumPy, headless OpenCV,
pytest, and pytest-cov. The baseline run collected the three existing
`get_greyscale` examples and passed. Coverage for `burkes.py` was 23% (43
statements, 33 missed; lines 20-37, 57-78, and 83-98 were missing). The saved
baseline and final command output are in `python312-before.txt` and
`python312-after.txt`.

The added `process` doctest constructs a 2x2 RGB `numpy` array directly, so it
does not need `image_data/lena.jpg`. The module still imports `cv2` at import
time, so OpenCV must be installed even though this doctest does not open a
window or read an image. After the change, all three collected doctest items
passed and `burkes.py` coverage rose to 84%; the remaining missed lines
(106-121) belong to the script's interactive `__main__` path.

## Directory and filename scripts

`DIRECTORY.md` contains the entry
`* [Burkes](digital_image_processing/dithering/burkes.py)`. The directory
generator uses `good_file_paths`, which walks source directories, skips
`scripts`, hidden/underscore directories and virtual environments, and lists
`.py`/`.ipynb` files other than `__init__.py`. It does not filter files by
whether their dependencies can be installed in CI. The generated list is
sorted and rendered as Markdown links.

`scripts/validate_filenames.py` reuses that same file iterator and checks for
uppercase names, spaces, hyphens, and files outside a directory. It does not
check imports or testability. `burkes.py` passes those filename rules, so it
belongs in `DIRECTORY.md` even while its directory is temporarily excluded
from the Python 3.15t test job. `DIRECTORY.md` is generated and was not edited.

## CI proposal

Keep the current Python 3.15t job and its OpenCV-related exclusion. Add a
separate GIL-enabled Python 3.12 job for `digital_image_processing/` that
installs `numpy`, `opencv-python-headless`, `pytest`, and `pytest-cov`, then
runs pytest with doctest collection and coverage. Since the repository's
`requires-python` currently starts at 3.15, the prototype command uses
`uv run --no-project --python 3.12`; alternatively, the dedicated job can use
a Python 3.12 virtual environment directly. Once a `cp315t` OpenCV wheel is
available, the tree can rejoin the primary CI command and its exclusion can be
removed.
