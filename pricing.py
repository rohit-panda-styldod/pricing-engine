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


def calculate_shipping(subtotal, weight, domestic=True):
    """Calculate shipping cost based on order subtotal and weight.

    Args:
        subtotal: Order subtotal in dollars.
        weight: Package weight in pounds.
        domestic: True for domestic, False for international.

    Returns:
        Shipping cost rounded to 2 decimal places.

    Raises:
        ValueError: If subtotal is negative or weight is not positive.
    """
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative")
    if weight <= 0:
        raise ValueError("Weight must be positive")

    if domestic and subtotal > 50:
        return 0.00

    base_rate = 5.00 if domestic else 15.00
    per_pound = 0.50 if domestic else 1.50
    shipping = base_rate + (weight * per_pound)
    return round(shipping, 2)


COUPON_CODES = {
    "SAVE10": {"type": "percent", "value": 10},
    "FLAT5": {"type": "fixed", "value": 5},
    "WELCOME20": {"type": "percent", "value": 20},
}


def apply_coupon(subtotal, code):
    """Apply a coupon code to the subtotal.

    Args:
        subtotal: Order subtotal in dollars.
        code: Coupon code string (e.g., 'SAVE10', 'FLAT5', 'WELCOME20').

    Returns:
        Discounted subtotal rounded to 2 decimal places.

    Raises:
        ValueError: If coupon code is invalid or subtotal is negative.
    """
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative")

    code = code.upper().strip()
    if code not in COUPON_CODES:
        raise ValueError(f"Invalid coupon code: {code}")

    coupon = COUPON_CODES[code]
    if coupon["type"] == "percent":
        discounted = subtotal * (1 - coupon["value"] / 100)
    else:
        discounted = subtotal - coupon["value"]

    return round(max(discounted, 0), 2)


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