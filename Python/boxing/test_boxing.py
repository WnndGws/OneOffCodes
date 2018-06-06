#!/usr/bin/python3
## Tests boxing.py

import boxing

import hypothesis
import pytest

import datetime


def test_scrape_wikitables():
    result = boxing.scrape_wikitables()
    assert len(result) > 0


@hypothesis.given(
    a=hypothesis.strategies.datetimes(), b=hypothesis.strategies.integers()
)
def test_add_months(a, b):
    if not 1 < b < 12:
        c = abs(b)
        c = c - (c // 12) * 12
        if (c == 0) or (c == 12):
            c = c + 1
    else:
        c = b
    result = boxing.add_months(a, b)
    assert result.month + 12 * (result.year - a.year) == a.month + c
