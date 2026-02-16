"""Basic tests for the pricing engine."""
import pytest
from pricing import calculate_subtotal, calculate_total, calculate_shipping, apply_coupon


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


# --- Shipping calculator tests ---


def test_shipping_domestic_free_over_50():
    assert calculate_shipping(75.00, 3.0) == 0.00


def test_shipping_domestic_free_at_exactly_50():
    assert calculate_shipping(50.00, 5.0) == 0.00


def test_shipping_domestic_paid_under_50():
    # base $5 + 2lb * $0.50 = $6.00
    assert calculate_shipping(30.00, 2.0) == 6.00


def test_shipping_domestic_zero_weight():
    # Under $50: base $5 + 0lb * $0.50 = $5.00
    assert calculate_shipping(10.00, 0) == 5.00


def test_shipping_international_basic():
    # base $15 + 3lb * $2.50 = $22.50
    assert calculate_shipping(100.00, 3.0, is_international=True) == 22.50


def test_shipping_international_no_free_shipping():
    # International never gets free shipping even over $50
    # base $15 + 1lb * $2.50 = $17.50
    assert calculate_shipping(200.00, 1.0, is_international=True) == 17.50


def test_shipping_international_zero_weight():
    # base $15 + 0 = $15.00
    assert calculate_shipping(25.00, 0, is_international=True) == 15.00


def test_shipping_negative_subtotal_raises():
    with pytest.raises(ValueError, match="Subtotal cannot be negative"):
        calculate_shipping(-10.00, 2.0)


def test_shipping_negative_weight_raises():
    with pytest.raises(ValueError, match="Weight cannot be negative"):
        calculate_shipping(30.00, -1.0)


# --- Coupon code system tests ---


def test_coupon_save10():
    # 10% off $100 = $90
    assert apply_coupon(100.00, "SAVE10") == 90.00


def test_coupon_flat5():
    # $5 off $100 = $95
    assert apply_coupon(100.00, "FLAT5") == 95.00


def test_coupon_welcome20():
    # 20% off $80 = $64
    assert apply_coupon(80.00, "WELCOME20") == 64.00


def test_coupon_case_insensitive():
    assert apply_coupon(100.00, "save10") == 90.00
    assert apply_coupon(100.00, "Save10") == 90.00


def test_coupon_with_whitespace():
    assert apply_coupon(100.00, "  SAVE10  ") == 90.00


def test_coupon_invalid_code_raises():
    with pytest.raises(ValueError, match="Invalid coupon code"):
        apply_coupon(100.00, "FAKECODE")


def test_coupon_flat5_exceeds_subtotal():
    # $5 off $3 should floor at $0
    assert apply_coupon(3.00, "FLAT5") == 0.00


def test_coupon_zero_subtotal():
    assert apply_coupon(0, "SAVE10") == 0.00
    assert apply_coupon(0, "FLAT5") == 0.00


def test_coupon_rounding():
    # 10% off $33.33 = $29.997 -> $30.00
    assert apply_coupon(33.33, "SAVE10") == 30.00