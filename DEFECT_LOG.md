# Defect Log: MockMart POS System

**Project:** MockMart POS System v1.0  
**Logged by:** Carina Kumar  
**Last updated:** November 2024

---

## Defect status definitions

| Status | Meaning |
|---|---|
| Open | Defect logged; not yet assigned |
| In Progress | Developer actively working on fix |
| Fixed | Developer has resolved; pending retest |
| Closed | Retest passed; defect resolved |
| Won't Fix | Accepted risk or out of scope |

## Severity definitions

| Severity | Definition |
|---|---|
| P1 - Critical | Blocks core functionality; testing cannot continue |
| P2 - High | Major feature broken; significant business impact |
| P3 - Medium | Partial functionality; workaround exists |
| P4 - Low | Cosmetic or minor UX issue |

---

## Active defects

---

### BUG-001
**Title:** Split tender transaction does not apply discount correctly  
**Severity:** P2 — High  
**Status:** Fixed — pending retest  
**Found in TC:** TC-013, TC-020  
**Reported:** Nov 13, 2024  
**Assigned to:** Dev Team  

**Steps to reproduce:**
1. Add items totalling $85.00 to cart
2. Apply a 10% manual discount (expected total: $76.50)
3. Apply $40.00 cash payment (expected remaining: $36.50)
4. Apply credit card for remaining balance

**Expected result:** Credit card is charged $36.50; receipt shows discount and both payment methods

**Actual result:** Credit card is charged $45.00 — the discount is not reflected in the remaining balance after the first tender is applied

**Evidence:** Screenshot attached (bug-001-split-tender.png)

**Notes:** Issue appears isolated to split tender flows. Single-tender transactions with discounts work correctly.

---

### BUG-002
**Title:** Return without receipt allows cash refund instead of store credit only  
**Severity:** P2 — High  
**Status:** In Progress  
**Found in TC:** TC-031  
**Reported:** Nov 14, 2024  
**Assigned to:** Dev Team  

**Steps to reproduce:**
1. Navigate to Returns and select "Return without receipt"
2. Scan any eligible item
3. On refund method screen, select Cash

**Expected result:** Cash refund option should be disabled for no-receipt returns; only store credit should be available

**Actual result:** Cash refund option is available and can be selected, allowing a cash refund to be processed without a receipt

**Evidence:** Screen recording attached (bug-002-no-receipt-return.mp4)

**Notes:** This is a policy violation risk. Priority for resolution before UAT.

---

### BUG-003
**Title:** Session timeout warning does not appear before logout  
**Severity:** P3 — Medium  
**Status:** Open  
**Found in TC:** TC-003  
**Reported:** Nov 15, 2024  
**Assigned to:** Unassigned  

**Steps to reproduce:**
1. Log in as any user
2. Leave session idle for 15 minutes

**Expected result:** Warning message appears at 13 minutes alerting the user the session will expire

**Actual result:** No warning is displayed; session expires silently and user is logged out without notice

**Evidence:** Confirmed across Chrome and Edge browsers

**Notes:** Lower priority but should be addressed before go-live for UX reasons. No data loss observed.

---

### BUG-004
**Title:** EOD report does not include voided transactions in cash reconciliation
**Severity:** P2 — High  
**Status:** Open  
**Found in TC:** TC-040  
**Reported:** Nov 18, 2024  
**Assigned to:** Unassigned  

**Steps to reproduce:**
1. Process 3 cash transactions during the shift
2. Void one of the transactions
3. Run EOD reconciliation

**Expected result:** Expected cash total reflects the voided transaction; cash drawer expected total is reduced accordingly

**Actual result:** Voided transaction is still included in the expected cash total, causing a false discrepancy on every shift with a void

**Evidence:** EOD report exported (bug-004-eod-report.csv)

**Notes:** This will create reconciliation problems at scale. Recommend P1 escalation if not fixed before UAT.

---

### BUG-005
**Title:** Receipt shows incorrect date when transaction crosses midnight  
**Severity:** P4 — Low  
**Status:** Open  
**Found in TC:** TC-010  
**Reported:** Nov 19, 2024  
**Assigned to:** Unassigned  

**Steps to reproduce:**
1. Begin a transaction before midnight (e.g. 11:58 PM)
2. Complete the transaction after midnight (e.g. 12:01 AM)

**Expected result:** Receipt date reflects the date the transaction was completed

**Actual result:** Receipt date shows the date the transaction was started, not completed

**Evidence:** Manual test during extended shift simulation

**Notes:** Edge case. Low customer impact but worth flagging for a future fix.

---

## Closed defects

---

### BUG-006
**Title:** Login page does not display error message on invalid credentials  
**Severity:** P2 — High  
**Status:** Closed  
**Found in TC:** TC-002  
**Reported:** Nov 11, 2024  
**Closed:** Nov 13, 2024  

**Summary:** Login form submitted with invalid credentials returned a blank screen instead of an error message. Fixed in build v1.0.2. Retest passed — error message now displays correctly.

---

### BUG-007
**Title:** Barcode scanner input adds duplicate item on fast scan  
**Severity:** P3 — Medium  
**Status:** Closed  
**Found in TC:** TC-010  
**Reported:** Nov 12, 2024  
**Closed:** Nov 16, 2024  

**Summary:** Scanning a barcode quickly twice added the item twice to the cart even when only one scan was intended. Fixed with a 300ms debounce on scanner input in build v1.0.3. Retest passed.

---
