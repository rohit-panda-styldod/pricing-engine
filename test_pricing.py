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


class TestCalculateShipping:
    """Tests for the shipping cost calculator."""

    def test_domestic_free_shipping_over_50(self):
        """Domestic orders over $50 get free shipping."""
        assert calculate_shipping(51.00, 5.0, domestic=True) == 0.00

    def test_domestic_free_shipping_at_boundary(self):
        """Domestic orders at exactly $50 do NOT get free shipping."""
        assert calculate_shipping(50.00, 2.0, domestic=True) > 0

    def test_domestic_paid_shipping(self):
        """Domestic orders under $50 pay base + weight rate."""
        # base_rate=5.00 + weight*0.50 = 5.00 + 2*0.50 = 6.00
        assert calculate_shipping(30.00, 2.0, domestic=True) == 6.00

    def test_domestic_heavy_package(self):
        """Weight affects domestic shipping cost."""
        # 5.00 + 10*0.50 = 10.00
        assert calculate_shipping(20.00, 10.0, domestic=True) == 10.00

    def test_international_no_free_shipping(self):
        """International orders never get free shipping regardless of subtotal."""
        result = calculate_shipping(100.00, 2.0, domestic=False)
        # base_rate=15.00 + 2*1.50 = 18.00
        assert result == 18.00

    def test_international_base_rate(self):
        """International has higher base rate than domestic."""
        intl = calculate_shipping(30.00, 1.0, domestic=False)
        dom = calculate_shipping(30.00, 1.0, domestic=True)
        assert intl > dom

    def test_international_heavy_package(self):
        """International weight rate is higher."""
        # 15.00 + 5*1.50 = 22.50
        assert calculate_shipping(10.00, 5.0, domestic=False) == 22.50

    def test_negative_subtotal_raises(self):
        """Negative subtotal should raise ValueError."""
        with pytest.raises(ValueError, match="Subtotal cannot be negative"):
            calculate_shipping(-1.00, 2.0)

    def test_zero_weight_raises(self):
        """Zero weight should raise ValueError."""
        with pytest.raises(ValueError, match="Weight must be positive"):
            calculate_shipping(30.00, 0)

    def test_negative_weight_raises(self):
        """Negative weight should raise ValueError."""
        with pytest.raises(ValueError, match="Weight must be positive"):
            calculate_shipping(30.00, -1.0)

    def test_zero_subtotal_domestic(self):
        """Zero subtotal domestic still charges shipping."""
        assert calculate_shipping(0, 1.0, domestic=True) == 5.50

    def test_rounding(self):
        """Shipping cost should be rounded to 2 decimal places."""
        result = calculate_shipping(10.00, 3.0, domestic=False)
        assert result == round(result, 2)


# --- Coupon code tests ---


class TestApplyCoupon:
    """Tests for the coupon code system."""

    def test_save10_percentage(self):
        """SAVE10 applies 10% discount."""
        assert apply_coupon(100.00, "SAVE10") == 90.00

    def test_flat5_fixed_dollar(self):
        """FLAT5 subtracts $5."""
        assert apply_coupon(100.00, "FLAT5") == 95.00

    def test_welcome20_percentage(self):
        """WELCOME20 applies 20% discount."""
        assert apply_coupon(100.00, "WELCOME20") == 80.00

    def test_case_insensitive(self):
        """Coupon codes should be case-insensitive."""
        assert apply_coupon(100.00, "save10") == 90.00

    def test_whitespace_trimmed(self):
        """Coupon codes should have whitespace trimmed."""
        assert apply_coupon(100.00, " FLAT5 ") == 95.00

    def test_invalid_code_raises(self):
        """Invalid coupon code should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid coupon code"):
            apply_coupon(100.00, "BOGUS")

    def test_empty_code_raises(self):
        """Empty coupon code should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid coupon code"):
            apply_coupon(100.00, "")

    def test_negative_subtotal_raises(self):
        """Negative subtotal should raise ValueError."""
        with pytest.raises(ValueError, match="Subtotal cannot be negative"):
            apply_coupon(-10.00, "SAVE10")

    def test_zero_subtotal(self):
        """Zero subtotal returns zero after any coupon."""
        assert apply_coupon(0, "SAVE10") == 0.00

    def test_fixed_discount_exceeds_subtotal(self):
        """Fixed discount larger than subtotal floors at $0."""
        assert apply_coupon(3.00, "FLAT5") == 0.00

    def test_percentage_on_small_amount(self):
        """Percentage discount on small amounts rounds correctly."""
        assert apply_coupon(9.99, "SAVE10") == 8.99

    def test_rounding(self):
        """Coupon result should be rounded to 2 decimal places."""
        result = apply_coupon(33.33, "WELCOME20")
        assert result == round(result, 2)