"""Basic tests for the pricing engine."""
import pytest
from pricing import calculate_subtotal, calculate_total


def test_subtotal_single_item():
    items = [{"name": "Widget", "price": 10.00, "quantity": 3}]
    assert calculate_subtotal(items) == 30.00


def test_subtotal_multiple_items():
    items = [
        {"name": "Widget", "price": 10.00, "quantity": 2},
        {"name": "Gadget", "price": 25.50, "quantity": 1},
    ]
    assert calculate_subtotal(items) == 45.50


def test_total_no_discount():
    items = [{"name": "Widget", "price": 100.00, "quantity": 1}]
    result = calculate_total(items)
    assert result["subtotal"] == 100.00
    assert result["after_discount"] == 100.00
    assert result["total"] > 100.00  # tax added