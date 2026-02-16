"""
Simple pricing engine for an e-commerce platform.
Handles price calculations, discounts, tax, shipping, and coupons.
"""


def calculate_subtotal(items):
    """Calculate subtotal from a list of items.
    Each item is a dict with 'name', 'price', and 'quantity'.
    """
    total = 0
    for item in items:
        total += item["price"] * item["quantity"]
    return round(total, 2)


def apply_discount(subtotal, discount_percent):
    """Apply a percentage discount to the subtotal."""
    discounted = subtotal * (1 - discount_percent / 100)
    return round(discounted, 2)


def calculate_tax(amount, tax_rate=8.5):
    """Calculate tax on an amount.
    Default tax rate is 8.5%.
    """
    tax = amount * (tax_rate / 100)
    return round(tax, 2)


def calculate_shipping(subtotal, weight_lb, is_international=False):
    """Calculate shipping cost based on order subtotal and weight.

    Domestic orders over $50 get free shipping.
    International orders have a higher base rate.

    Args:
        subtotal: Order subtotal in dollars.
        weight_lb: Package weight in pounds.
        is_international: Whether the order ships internationally.

    Returns:
        Shipping cost rounded to 2 decimal places.

    Raises:
        ValueError: If subtotal or weight_lb is negative.
    """
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative")
    if weight_lb < 0:
        raise ValueError("Weight cannot be negative")

    if not is_international and subtotal >= 50:
        return 0.00

    if is_international:
        base_rate = 15.00
        per_lb_rate = 2.50
    else:
        base_rate = 5.00
        per_lb_rate = 0.50

    shipping = base_rate + (weight_lb * per_lb_rate)
    return round(shipping, 2)


COUPON_CODES = {
    "SAVE10": {"type": "percent", "value": 10},
    "FLAT5": {"type": "fixed", "value": 5},
    "WELCOME20": {"type": "percent", "value": 20},
}


def apply_coupon(subtotal, coupon_code):
    """Apply a coupon code to the subtotal.

    Supports percentage-based and fixed-dollar discounts.
    Valid codes: SAVE10 (10% off), FLAT5 ($5 off), WELCOME20 (20% off).

    Args:
        subtotal: Order subtotal in dollars.
        coupon_code: Coupon code string (case-insensitive).

    Returns:
        Discounted subtotal rounded to 2 decimal places (minimum $0).

    Raises:
        ValueError: If the coupon code is invalid.
    """
    code = coupon_code.strip().upper()
    if code not in COUPON_CODES:
        raise ValueError(f"Invalid coupon code: {coupon_code}")

    coupon = COUPON_CODES[code]
    if coupon["type"] == "percent":
        result = subtotal * (1 - coupon["value"] / 100)
    else:
        result = subtotal - coupon["value"]

    return round(max(result, 0), 2)


def calculate_total(items, discount_percent=0, tax_rate=8.5):
    """Calculate the final total: subtotal - discount + tax."""
    subtotal = calculate_subtotal(items)
    after_discount = apply_discount(subtotal, discount_percent)
    tax = calculate_tax(after_discount, tax_rate)
    total = after_discount + tax
    return {
        "subtotal": subtotal,
        "discount": discount_percent,
        "after_discount": after_discount,
        "tax": tax,
        "total": round(total, 2),
    }