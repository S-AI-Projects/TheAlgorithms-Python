"""
Comparison test suite for:
- data_structures/arrays/kth_largest_element.py (kth_largest_element)
- searches/quick_select.py (quick_select)
- searches/median_of_medians.py (quick_select)

Validates that all three implementations agree across >= 10 diverse shared inputs
and verifies k-th largest vs k-th smallest index/rank conversions.
"""

from __future__ import annotations

import pytest

from data_structures.arrays.kth_largest_element import kth_largest_element
from searches.median_of_medians import quick_select as qs_median_of_medians
from searches.quick_select import quick_select as qs_random

# 12 diverse test cases covering distinct values, extremes (ends), duplicates,
# negatives, single-element, and sorted/reverse-sorted inputs.
SHARED_TEST_CASES = [
    # 1. Distinct elements, k at maximum end (k=1)
    ([3, 7, 2, 9, 1, 8, 4, 6, 5], 1),
    # 2. Distinct elements, k at minimum end (k=n)
    ([3, 7, 2, 9, 1, 8, 4, 6, 5], 9),
    # 3. Distinct elements, median position
    ([3, 7, 2, 9, 1, 8, 4, 6, 5], 5),
    # 4. Array with multiple duplicate values
    ([5, 2, 8, 2, 5, 8, 2, 5, 1], 4),
    # 5. All identical elements
    ([7, 7, 7, 7, 7, 7], 3),
    # 6. Single element boundary
    ([42], 1),
    # 7. Strictly ascending (already sorted) array
    ([10, 20, 30, 40, 50, 60], 2),
    # 8. Strictly descending (reverse sorted) array
    ([90, 80, 70, 60, 50, 40], 5),
    # 9. Array containing negative integers and zero
    ([-15, -3, 0, -8, 2, -1, 4], 3),
    # 10. Large values with duplicates
    ([1000, 250, 5000, 750, 10000, 5000], 2),
    # 11. Even-length array with k near lower quartile
    ([12, 3, 5, 7, 4, 19, 26, 31], 6),
    # 12. Two elements list testing both positions
    ([100, -100], 1),
]


@pytest.mark.parametrize(("arr", "k_largest"), SHARED_TEST_CASES)
def test_implementations_agreement(arr: list[int], k_largest: int) -> None:
    """
    Test that kth_largest_element, searches/quick_select.py, and
    searches/median_of_medians.py all return identical elements.

    Conversions:
    - kth_largest_element(arr, k_largest): 1-based k-th largest (1 <= k <= n).
    - searches/quick_select(arr, index): 0-based k-th smallest index = n - k_largest.
    - searches/median_of_medians(arr, target): 1-based rank = n - k_largest + 1.
    """
    n = len(arr)
    expected = sorted(arr)[-k_largest]

    # kth_largest_element mutates arr in place, so pass a shallow copy
    res_kth = kth_largest_element(arr.copy(), k_largest)

    # searches/quick_select index conversion: index in sorted ascending array
    qs_index = n - k_largest
    res_qs = qs_random(arr.copy(), qs_index)

    # searches/median_of_medians rank conversion: 1-based rank in ascending order
    mom_rank = n - k_largest + 1
    res_mom = qs_median_of_medians(arr.copy(), mom_rank)

    assert res_kth == expected, f"kth_largest_element failed for {arr}, k={k_largest}"
    assert res_qs == expected, f"quick_select failed for {arr}, index={qs_index}"
    assert res_mom == expected, f"median_of_medians failed for {arr}, rank={mom_rank}"


def test_edge_cases_out_of_range() -> None:
    """
    Document and verify out-of-range behavior across implementations:
    - kth_largest_element raises ValueError for position <= 0 or position > len.
    - searches/quick_select returns None for index < 0 or index >= len.
    - searches/median_of_medians returns -1 for target > len.
    """
    sample = [1, 2, 3, 4, 5]

    # k_largest <= 0
    with pytest.raises(ValueError, match="Invalid value of 'position'"):
        kth_largest_element(sample.copy(), 0)

    with pytest.raises(ValueError, match="Invalid value of 'position'"):
        kth_largest_element(sample.copy(), -1)

    # k_largest > len
    with pytest.raises(ValueError, match="Invalid value of 'position'"):
        kth_largest_element(sample.copy(), 6)

    # quick_select returns None out of bounds
    assert qs_random(sample.copy(), -1) is None
    assert qs_random(sample.copy(), 5) is None

    # median_of_medians returns -1 for rank > len
    assert qs_median_of_medians(sample.copy(), 10) == -1


def test_empty_list_handling() -> None:
    """
    Verify empty list handling:
    - kth_largest_element returns -1 on empty list.
    - quick_select returns None on empty list.
    """
    assert kth_largest_element([], 1) == -1
    assert qs_random([], 0) is None
