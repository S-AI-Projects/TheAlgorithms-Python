# ruff: noqa: INP001
"""Hypothesis checks for edit-distance metric properties."""

from __future__ import annotations

import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strings.edit_distance import edit_distance

SHORT_STRINGS = st.text(max_size=5)


@settings(max_examples=1000, deadline=None)
@given(SHORT_STRINGS)
def test_identical_strings_have_zero_distance(text: str) -> None:
    """A string needs no edits to become itself."""
    assert edit_distance(text, text) == 0


@settings(max_examples=1000, deadline=None)
@given(SHORT_STRINGS, SHORT_STRINGS)
def test_distance_is_symmetric(source: str, target: str) -> None:
    """Reversing the source and target does not change edit distance."""
    assert edit_distance(source, target) == edit_distance(target, source)


@settings(max_examples=1000, deadline=None)
@given(SHORT_STRINGS, SHORT_STRINGS, SHORT_STRINGS)
def test_triangle_inequality(first: str, second: str, third: str) -> None:
    """A direct transformation cannot cost more than a two-step route."""
    assert edit_distance(first, third) <= edit_distance(first, second) + edit_distance(
        second, third
    )


@settings(max_examples=1000, deadline=None)
@given(SHORT_STRINGS, SHORT_STRINGS)
def test_distance_is_bounded_by_string_lengths(source: str, target: str) -> None:
    """Length difference is a lower bound and the longer length an upper bound."""
    distance = edit_distance(source, target)
    assert abs(len(source) - len(target)) <= distance <= max(len(source), len(target))
