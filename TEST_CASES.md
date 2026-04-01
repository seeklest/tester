# Test Case Library: MockMart POS System

**Module coverage:** Transactions | Returns | Discounts | EOD | Login  
**Prepared by:** Carina Kumar  
**Last updated:** November 2024

---

## How to use this document

Each test case follows this format:

| Field | Description |
|---|---|
| TC-ID | Unique test case identifier |
| Description | What is being tested |
| Preconditions | What must be true before executing |
| Steps | Actions to perform in order |
| Expected result | What should happen if the system works correctly |
| Priority | P1 Critical / P2 High / P3 Medium / P4 Low |

---

## Module 1: User login and access

### TC-001 — Valid cashier login
**Priority:** P1  
**Preconditions:** User account exists with cashier role

| Step | Action | Expected Result |
|---|---|---|
| 1 | Navigate to POS login screen | Login form displays with username and password fields |
| 2 | Enter valid cashier credentials | Fields accept input |
| 3 | Click Login | User is authenticated and redirected to the POS home screen |
| 4 | Verify role | Only cashier-level menu options are visible; admin options are hidden |

---

### TC-002 — Invalid password
**Priority:** P2  
**Preconditions:** User account exists

| Step | Action | Expected Result |
|---|---|---|
| 1 | Enter valid username and incorrect password | Fields accept input |
| 2 | Click Login | Error message displayed: "Invalid username or password" |
| 3 | Verify lockout | After 3 failed attempts, account is locked and user is notified |

---

### TC-003 — Session timeout
**Priority:** P2  
**Preconditions:** User is logged in

| Step | Action | Expected Result |
|---|---|---|
| 1 | Leave the session idle for 15 minutes | System displays a session expiry warning at 13 minutes |
| 2 | Allow session to fully expire | User is logged out and redirected to login screen |
| 3 | Attempt to navigate back | Session data is cleared; user cannot access previous screen without logging in again |

---

## Module 2: Transaction processing

### TC-010 — Successful cash sale
**Priority:** P1  
**Preconditions:** Cashier is logged in; product exists in system

| Step | Action | Expected Result |
|---|---|---|
| 1 | Scan or search for item by barcode | Item name, SKU, and price appear in the cart |
| 2 | Add a second item | Both items display in cart with correct subtotal |
| 3 | Select Cash as payment method | Cash tender screen opens |
| 4 | Enter cash amount equal to total | Change due displays as $0.00 |
| 5 | Confirm sale | Transaction completes; receipt is generated; inventory decrements |

---

### TC-011 — Cash sale with change
**Priority:** P1  
**Preconditions:** Cashier is logged in; product exists in system

| Step | Action | Expected Result |
|---|---|---|
| 1 | Add item worth $12.50 to cart | Cart shows $12.50 |
| 2 | Select Cash; enter $20.00 | Change due displays as $7.50 |
| 3 | Confirm sale | Transaction completes; receipt shows amount tendered and change |

---

### TC-012 — Credit card payment
**Priority:** P1  
**Preconditions:** Cashier is logged in; payment terminal connected

| Step | Action | Expected Result |
|---|---|---|
| 1 | Add items to cart | Cart total is correct |
| 2 | Select Credit as payment method | Payment terminal prompt appears |
| 3 | Simulate approved card response | Transaction completes with "Approved" status |
| 4 | Simulate declined card response | Error displayed: "Payment declined — please try another method" |

---

### TC-013 — Split tender (cash + credit)
**Priority:** P2  
**Preconditions:** Cashier is logged in

| Step | Action | Expected Result |
|---|---|---|
| 1 | Add items totalling $85.00 | Cart shows $85.00 |
| 2 | Apply $40.00 cash payment | Remaining balance updates to $45.00 |
| 3 | Apply credit card for remaining $45.00 | Transaction completes; receipt shows both payment methods |

---

### TC-014 — Empty cart checkout attempt
**Priority:** P3  
**Preconditions:** Cashier is logged in; cart is empty

| Step | Action | Expected Result |
|---|---|---|
| 1 | Click Checkout with no items in cart | System displays validation message: "Cart is empty" |
| 2 | Verify no transaction is created | No transaction ID is generated |

---

## Module 3: Discounts and promotions

### TC-020 — Manual percentage discount
**Priority:** P2  
**Preconditions:** Cashier has discount permission; item is in cart

| Step | Action | Expected Result |
|---|---|---|
| 1 | Add item at $50.00 to cart | Cart shows $50.00 |
| 2 | Apply 10% manual discount | Discount of $5.00 is applied; new total is $45.00 |
| 3 | Confirm sale | Receipt shows original price, discount amount, and final total |

---

### TC-021 — Promotional coupon code
**Priority:** P2  
**Preconditions:** Valid coupon code exists in system

| Step | Action | Expected Result |
|---|---|---|
| 1 | Add items to cart | Cart shows subtotal |
| 2 | Enter valid coupon code | Discount is applied and displayed in cart |
| 3 | Enter expired coupon code | Error message: "This coupon has expired" |
| 4 | Enter invalid coupon code | Error message: "Invalid coupon code" |

---

### TC-022 — Discount without permission
**Priority:** P2  
**Preconditions:** User logged in with cashier role (no discount permission)

| Step | Action | Expected Result |
|---|---|---|
| 1 | Attempt to apply manual discount | System prompts for manager override code |
| 2 | Enter incorrect override code | Access denied; discount is not applied |
| 3 | Enter correct override code | Discount is applied and override is logged |

---

## Module 4: Returns and exchanges

### TC-030 — Standard return with receipt
**Priority:** P1  
**Preconditions:** Original transaction exists; item is returnable

| Step | Action | Expected Result |
|---|---|---|
| 1 | Navigate to Returns module | Returns screen displays |
| 2 | Enter original transaction ID | Transaction details load with eligible items |
| 3 | Select item to return | Item is added to return cart |
| 4 | Select refund method (original payment) | Refund amount is calculated correctly |
| 5 | Confirm return | Refund is processed; receipt generated; inventory increments |

---

### TC-031 — Return without receipt
**Priority:** P2  
**Preconditions:** No transaction ID available

| Step | Action | Expected Result |
|---|---|---|
| 1 | Select "Return without receipt" option | System prompts for item lookup by SKU or barcode |
| 2 | Scan item | Item details load; system flags as no-receipt return |
| 3 | Process return | Refund issued as store credit only; transaction is flagged for review |

---

### TC-032 — Return outside return window
**Priority:** P2  
**Preconditions:** Transaction is older than the 30-day return policy

| Step | Action | Expected Result |
|---|---|---|
| 1 | Enter transaction ID for a 35-day-old purchase | System identifies transaction as outside return window |
| 2 | Attempt to process return | Warning displayed: "This transaction is outside the return policy window" |
| 3 | Verify override option | Manager override is required to proceed |

---

## Module 5: End-of-day reconciliation

### TC-040 — EOD with balanced drawer
**Priority:** P1  
**Preconditions:** Transactions have been processed during the shift

| Step | Action | Expected Result |
|---|---|---|
| 1 | Navigate to End of Day | EOD summary screen opens showing expected cash total |
| 2 | Enter actual cash count | System compares expected vs actual |
| 3 | Submit with matching amounts | EOD closes with status "Balanced"; shift report is generated |

---

### TC-041 — EOD with cash discrepancy
**Priority:** P1  
**Preconditions:** Cash count does not match system expected total

| Step | Action | Expected Result |
|---|---|---|
| 1 | Enter cash count that differs from expected | System highlights discrepancy amount |
| 2 | Submit EOD | System accepts submission but flags discrepancy for manager review |
| 3 | Verify report | Shift report shows over/short amount and requires manager acknowledgment |

---
