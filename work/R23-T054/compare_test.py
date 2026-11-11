"""Compare ELU with SELU and Leaky ReLU (R23-T054).

Run from the repo root:  python -m pytest work/R23-T054/compare_test.py -v
"""

import numpy as np
import pytest

from neural_network.activation_functions.exponential_linear_unit import (
    exponential_linear_unit,
)
from neural_network.activation_functions.leaky_rectified_linear_unit import (
    leaky_rectified_linear_unit,
)
from neural_network.activation_functions.scaled_exponential_linear_unit import (
    scaled_exponential_linear_unit,
)

# 14 shared inputs: negatives, zero, positives, tiny and large values.
SHARED = np.array(
    [-1000.0, -50.0, -5.0, -2.0, -1.0, -0.1, 0.0, 0.1, 0.5, 1.0, 2.0, 5.0, 50.0, 700.0]
)
POSITIVE = SHARED[SHARED > 0]
ALPHAS = [0.0, 0.067, 0.3, 1.0, 1.6732]


@pytest.mark.parametrize("alpha", ALPHAS)
def test_elu_equals_selu_with_scale_one(alpha):
    # SELU(x, alpha, lambda_=1) is exactly ELU(x, alpha).
    assert np.array_equal(
        exponential_linear_unit(SHARED, alpha),
        scaled_exponential_linear_unit(SHARED, alpha, 1.0),
    )


def test_selu_defaults_are_scaled_elu():
    # SELU's documented constants: SELU(x) = 1.0507 * ELU(x, alpha=1.6732).
    assert np.allclose(
        scaled_exponential_linear_unit(SHARED),
        1.0507 * exponential_linear_unit(SHARED, 1.6732),
    )


@pytest.mark.parametrize("alpha", ALPHAS)
def test_elu_equals_leaky_relu_for_positive_inputs(alpha):
    assert np.array_equal(
        exponential_linear_unit(POSITIVE, alpha),
        leaky_rectified_linear_unit(POSITIVE, alpha),
    )
    assert np.array_equal(exponential_linear_unit(POSITIVE, alpha), POSITIVE)


@pytest.mark.parametrize("alpha", ALPHAS)
def test_zero_maps_to_zero_in_all_three(alpha):
    zero = np.array([0.0])
    assert exponential_linear_unit(zero, alpha)[0] == 0
    assert leaky_rectified_linear_unit(zero, alpha)[0] == 0
    assert scaled_exponential_linear_unit(zero, alpha, 1.0)[0] == 0


def test_large_negative_saturates_for_elu_but_not_leaky_relu():
    x = np.array([-1000.0])
    assert exponential_linear_unit(x, 0.3)[0] == pytest.approx(-0.3)
    assert leaky_rectified_linear_unit(x, 0.3)[0] == pytest.approx(-300.0)


def test_they_disagree_on_negative_inputs():
    # Why the three cannot agree everywhere: different negative branches.
    x = np.array([-1.0])
    elu = exponential_linear_unit(x, 0.3)[0]
    leaky = leaky_rectified_linear_unit(x, 0.3)[0]
    assert elu != pytest.approx(leaky)


def test_large_positive_gives_right_answer_but_warns():
    # np.where evaluates both branches, so exp(1000) overflows (inf) and warns,
    # even though the positive branch is the one returned.
    with pytest.warns(RuntimeWarning, match="overflow"):
        result = exponential_linear_unit(np.array([1000.0]), 0.3)
    assert result[0] == 1000.0
