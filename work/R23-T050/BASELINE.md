# Laplacian filter baseline

## Input categories for `my_laplacian`

- Valid: a NumPy grayscale or color image and a `ksize` of 1, 3, 5, or 7.
- Boundary: the smallest and largest supported kernel sizes (1 and 7), and a
  3x3 source array smaller than the 5x5 and 7x7 kernels.
- Invalid: a kernel size outside the supported set, such as 0. The existing
  doctest verifies the `ValueError`; the invalid size is checked before the
  source image is passed to OpenCV.

## Coverage before the change

The requested baseline command was attempted:

```bash
uv run --python 3.12 --with numpy --with opencv-python-headless --with pytest --with pytest-cov pytest digital_image_processing/filters/laplacian_filter.py --cov=digital_image_processing/filters --cov-report=term-missing
```

It could not start because this checkout declares `requires-python = ">=3.15"`,
which rejects Python 3.12. The same test was run successfully using uv's
temporary, no-project mode:

```bash
uv run --no-project --python 3.12 --with numpy --with opencv-python-headless --with pytest --with pytest-cov pytest digital_image_processing/filters/laplacian_filter.py --cov=digital_image_processing/filters --cov-report=term-missing
```

Baseline result: 1 test passed; `laplacian_filter.py` had 17 statements, 8
missed, and 53% coverage. The uncovered lines were line 60 (the return path in
`my_laplacian`) and lines 67–81 (the interactive image-display example). The
invalid-`ksize` doctest already covered the error path.

Coverage for the other filters in `digital_image_processing/filters` was not
the target of this task. The baseline command also warned that Python 3.12
coverage could not parse the unrelated `local_binary_pattern.py`.

## Results after the doctests

The Python 3.12 no-project coverage command passed: 1 pytest item passed.
`laplacian_filter.py` reports 59% module coverage because only the interactive
`__main__` example (lines 81–95 after the doctest additions) remains uncovered.
All executable statements inside `my_laplacian` are covered: 6 of 6 (100%),
including each kernel-size lookup, the `ValueError` path, and the valid return
path. The same unrelated `local_binary_pattern.py` parsing warning remains.

The direct doctest command was:

```bash
uv run --no-project --python 3.12 --with numpy --with opencv-python-headless --with pytest python -m doctest -v digital_image_processing/filters/laplacian_filter.py
```

Its summary was:

```text
6 tests in 2 items.
6 passed and 0 failed.
Test passed.
```
