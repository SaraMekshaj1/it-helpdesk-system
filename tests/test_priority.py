"""
test_priority.py
Unit tests for the impact/urgency priority matrix.
Run with: python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.priority import calculate_priority


def test_high_high_is_critical():
    assert calculate_priority("High", "High") == "Critical"


def test_high_medium_is_high():
    assert calculate_priority("High", "Medium") == "High"


def test_medium_high_is_high():
    assert calculate_priority("Medium", "High") == "High"


def test_medium_medium_is_medium():
    assert calculate_priority("Medium", "Medium") == "Medium"


def test_low_low_is_low():
    assert calculate_priority("Low", "Low") == "Low"


def test_high_low_is_medium():
    assert calculate_priority("High", "Low") == "Medium"


def test_low_high_is_medium():
    assert calculate_priority("Low", "High") == "Medium"


def test_invalid_impact_raises():
    with pytest.raises(ValueError):
        calculate_priority("Extreme", "High")


def test_invalid_urgency_raises():
    with pytest.raises(ValueError):
        calculate_priority("High", "Extreme")
