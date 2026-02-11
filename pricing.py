"""
Simple pricing engine for an e-commerce platform.
Handles price calculations, discounts, and tax.
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