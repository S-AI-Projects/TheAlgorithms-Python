"""Check that the refactored electronics/resistor_color_code.py behaves exactly like
the original (saved as original_resistor_color_code.py): same results, same exception
types and messages, over the doctests, every raise path, and random inputs.

Run from the repo root:  python -m pytest work/R23-T058/equivalence_test.py -v
"""

import importlib.util
import itertools
import random
from pathlib import Path

import pytest

from electronics import resistor_color_code as new


def _load_original():
    path = Path(__file__).parent / "original_resistor_color_code.py"
    spec = importlib.util.spec_from_file_location("original_resistor_color_code", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old = _load_original()
COLORS = [*old.valid_colors, "Aqua", "Lime", "", "black", None, 5]


def outcome(func, *args):
    """Return ('ok', value) or ('raises', type name, message)."""
    try:
        return ("ok", func(*args))
    except Exception as e:  # noqa: BLE001
        return ("raises", type(e).__name__, str(e))


def same(name, *args):
    assert outcome(getattr(new, name), *args) == outcome(getattr(old, name), *args), (
        name,
        args,
    )


@pytest.mark.parametrize("color", COLORS)
@pytest.mark.parametrize(
    "name", ["get_multiplier", "get_tolerance", "get_temperature_coeffecient"]
)
def test_single_color_getters(name, color):
    same(name, color)


def test_get_significant_digits():
    for n in range(0, 4):
        for combo in itertools.product(COLORS, repeat=n):
            same("get_significant_digits", list(combo))


def test_get_band_type_count():
    for bands in [0, 2, 3, 4, 5, 6, 7, "3", None]:
        for kind in ["significant", "multiplier", "tolerance", "temp_coeffecient", "x"]:
            same("get_band_type_count", bands, kind)


def test_check_validity_random():
    rng = random.Random(0)
    for _ in range(5000):
        bands = rng.choice([0, 1, 2, 3, 4, 5, 6, 7, 3.0, 4.5])
        colors = [rng.choice(COLORS) for _ in range(rng.randint(0, 8))]
        same("check_validity", bands, colors)


def test_calculate_resistance_random():
    rng = random.Random(1)
    good = old.valid_colors
    for _ in range(20000):
        bands = rng.choice([0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7])
        pool = good if rng.random() < 0.8 else COLORS
        count = bands if rng.random() < 0.85 else rng.randint(0, 8)
        colors = [rng.choice(pool) for _ in range(count)]
        same("calculate_resistance", bands, colors)


def test_all_valid_combinations_of_three_and_four_bands():
    for combo in itertools.product(old.valid_colors, repeat=3):
        same("calculate_resistance", 3, list(combo))
    for combo in itertools.product(old.valid_colors, repeat=4):
        same("calculate_resistance", 4, list(combo))


def test_the_ten_raise_paths_are_kept():
    # one input per `raise` statement in the original file
    cases = [
        ("get_significant_digits", (["Aqua", "Blue"],)),
        ("get_multiplier", ("Ivory",)),
        ("get_tolerance", ("Indigo",)),
        ("get_temperature_coeffecient", ("Cyan",)),
        ("get_band_type_count", (2, "significant")),
        ("get_band_type_count", (3, "sign")),
        ("check_validity", (0, [])),
        ("check_validity", (4, ["Black"])),
        ("check_validity", (3, ["Cyan", "Red", "Yellow"])),
    ]
    for name, args in cases:
        same(name, *args)
        assert outcome(getattr(new, name), *args)[0] == "raises"
    # 10th raise ("Input is invalid") is unreachable: check_validity raises first
    assert outcome(new.calculate_resistance, 7, ["Red"])[0] == "raises"
