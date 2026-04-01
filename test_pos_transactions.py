"""
Automated regression tests for MockMart POS transaction workflows.
Covers: cart operations, payment processing, discounts, and returns.

Run with: pytest tests/ -v
"""

import pytest


# ---------------------------------------------------------------------------
# Mock data and helpers
# ---------------------------------------------------------------------------

def make_cart():
    """Return a fresh empty cart."""
    return {"items": [], "discount": 0.0, "payments": []}


def add_item(cart, name, sku, price, qty=1):
    cart["items"].append({"name": name, "sku": sku, "price": price, "qty": qty})
    return cart


def cart_subtotal(cart):
    return round(sum(i["price"] * i["qty"] for i in cart["items"]), 2)


def apply_discount(cart, percent):
    if not 0 < percent <= 100:
        raise ValueError("Discount must be between 1 and 100 percent.")
    cart["discount"] = percent
    return cart


def cart_total(cart):
    subtotal = cart_subtotal(cart)
    discount_amount = round(subtotal * cart["discount"] / 100, 2)
    return round(subtotal - discount_amount, 2)


def apply_payment(cart, method, amount):
    if method not in ("cash", "credit", "debit", "store_credit"):
        raise ValueError(f"Unknown payment method: {method}")
    if amount <= 0:
        raise ValueError("Payment amount must be greater than zero.")
    cart["payments"].append({"method": method, "amount": round(amount, 2)})
    return cart


def amount_paid(cart):
    return round(sum(p["amount"] for p in cart["payments"]), 2)


def change_due(cart, tendered):
    total = cart_total(cart)
    if tendered < total:
        raise ValueError("Tendered amount is less than total.")
    return round(tendered - total, 2)


def checkout(cart):
    if not cart["items"]:
        raise ValueError("Cart is empty.")
    total = cart_total(cart)
    paid = amount_paid(cart)
    if round(paid, 2) < round(total, 2):
        raise ValueError(f"Insufficient payment. Total: ${total:.2f}, Paid: ${paid:.2f}")
    return {"status": "success", "total": total, "paid": paid}


def process_return(transaction_id, items_to_return, original_payment_method, within_policy=True):
    if not transaction_id:
        raise ValueError("Transaction ID is required.")
    if not items_to_return:
        raise ValueError("No items selected for return.")
    if not within_policy:
        raise PermissionError("Transaction is outside the return policy window.")
    refund = round(sum(i["price"] * i["qty"] for i in items_to_return), 2)
    return {"status": "refunded", "amount": refund, "method": original_payment_method}


# ---------------------------------------------------------------------------
# Tests: cart operations
# ---------------------------------------------------------------------------

class TestCartOperations:

    def test_add_single_item(self):
        cart = make_cart()
        add_item(cart, "Wireless Mouse", "SKU-001", 29.99)
        assert len(cart["items"]) == 1
        assert cart_subtotal(cart) == 29.99

    def test_add_multiple_items(self):
        cart = make_cart()
        add_item(cart, "Wireless Mouse", "SKU-001", 29.99)
        add_item(cart, "USB Hub", "SKU-002", 44.99)
        assert len(cart["items"]) == 2
        assert cart_subtotal(cart) == 74.98

    def test_add_item_with_quantity(self):
        cart = make_cart()
        add_item(cart, "AA Batteries", "SKU-010", 5.99, qty=4)
        assert cart_subtotal(cart) == round(5.99 * 4, 2)

    def test_empty_cart_checkout_raises(self):
        cart = make_cart()
        with pytest.raises(ValueError, match="Cart is empty"):
            checkout(cart)


# ---------------------------------------------------------------------------
# Tests: payment processing
# ---------------------------------------------------------------------------

class TestPaymentProcessing:

    def test_exact_cash_payment(self):
        cart = make_cart()
        add_item(cart, "Keyboard", "SKU-020", 75.00)
        apply_payment(cart, "cash", 75.00)
        result = checkout(cart)
        assert result["status"] == "success"
        assert result["total"] == 75.00

    def test_cash_payment_with_change(self):
        cart = make_cart()
        add_item(cart, "Notebook", "SKU-030", 12.50)
        assert change_due(cart, 20.00) == 7.50

    def test_insufficient_payment_raises(self):
        cart = make_cart()
        add_item(cart, "Monitor", "SKU-040", 299.99)
        apply_payment(cart, "credit", 100.00)
        with pytest.raises(ValueError, match="Insufficient payment"):
            checkout(cart)

    def test_credit_card_payment(self):
        cart = make_cart()
        add_item(cart, "Headphones", "SKU-050", 89.99)
        apply_payment(cart, "credit", 89.99)
        result = checkout(cart)
        assert result["status"] == "success"

    def test_invalid_payment_method_raises(self):
        cart = make_cart()
        add_item(cart, "Pen", "SKU-060", 1.99)
        with pytest.raises(ValueError, match="Unknown payment method"):
            apply_payment(cart, "bitcoin", 1.99)

    def test_split_tender(self):
        cart = make_cart()
        add_item(cart, "Tablet", "SKU-070", 350.00)
        apply_payment(cart, "cash", 100.00)
        apply_payment(cart, "credit", 250.00)
        result = checkout(cart)
        assert result["status"] == "success"
        assert amount_paid(cart) == 350.00


# ---------------------------------------------------------------------------
# Tests: discounts
# ---------------------------------------------------------------------------

class TestDiscounts:

    def test_percentage_discount(self):
        cart = make_cart()
        add_item(cart, "Jacket", "SKU-080", 100.00)
        apply_discount(cart, 10)
        assert cart_total(cart) == 90.00

    def test_discount_reflected_in_total(self):
        cart = make_cart()
        add_item(cart, "Boots", "SKU-090", 80.00)
        add_item(cart, "Belt", "SKU-091", 20.00)
        apply_discount(cart, 20)
        assert cart_subtotal(cart) == 100.00
        assert cart_total(cart) == 80.00

    def test_invalid_discount_raises(self):
        cart = make_cart()
        add_item(cart, "Scarf", "SKU-092", 25.00)
        with pytest.raises(ValueError):
            apply_discount(cart, 0)

    def test_discount_over_100_raises(self):
        cart = make_cart()
        add_item(cart, "Hat", "SKU-093", 30.00)
        with pytest.raises(ValueError):
            apply_discount(cart, 110)

    def test_split_tender_with_discount(self):
        cart = make_cart()
        add_item(cart, "Coat", "SKU-094", 200.00)
        apply_discount(cart, 10)
        total = cart_total(cart)
        assert total == 180.00
        apply_payment(cart, "cash", 100.00)
        apply_payment(cart, "credit", 80.00)
        result = checkout(cart)
        assert result["status"] == "success"
        assert result["total"] == 180.00


# ---------------------------------------------------------------------------
# Tests: returns
# ---------------------------------------------------------------------------

class TestReturns:

    def test_standard_return_with_receipt(self):
        items = [{"name": "Jeans", "sku": "SKU-100", "price": 59.99, "qty": 1}]
        result = process_return("TXN-20241115-001", items, "credit")
        assert result["status"] == "refunded"
        assert result["amount"] == 59.99
        assert result["method"] == "credit"

    def test_return_outside_policy_raises(self):
        items = [{"name": "Shirt", "sku": "SKU-101", "price": 29.99, "qty": 1}]
        with pytest.raises(PermissionError, match="outside the return policy"):
            process_return("TXN-20241001-002", items, "cash", within_policy=False)

    def test_return_no_transaction_id_raises(self):
        items = [{"name": "Socks", "sku": "SKU-102", "price": 9.99, "qty": 1}]
        with pytest.raises(ValueError, match="Transaction ID is required"):
            process_return("", items, "cash")

    def test_return_no_items_raises(self):
        with pytest.raises(ValueError, match="No items selected"):
            process_return("TXN-20241115-003", [], "credit")

    def test_partial_return(self):
        items_to_return = [{"name": "Gloves", "sku": "SKU-103", "price": 19.99, "qty": 1}]
        result = process_return("TXN-20241115-004", items_to_return, "debit")
        assert result["amount"] == 19.99
