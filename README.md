# MockMart POS Testing Portfolio

A QA testing portfolio project simulating a real-world software testing engagement for a point-of-sale (POS) system. This repo demonstrates test planning, test case design, defect tracking, and automated regression testing for a mock retail POS application.

---

## Repository structure

```
pos-testing-portfolio/
├── TEST_PLAN.md          # Full test plan covering scope, approach, schedule, risks
├── TEST_CASES.md         # Manual test case library (login, transactions, discounts, returns, EOD)
├── DEFECT_LOG.md         # Sample defect log with bug reports in realistic format
├── tests/
│   └── test_pos_transactions.py   # Automated regression tests using Python + pytest
└── README.md
```

---

## What this project covers

### Test plan
A structured QA test plan covering:
- Scope and out-of-scope boundaries
- Test approach (functional, regression, negative, UAT)
- Entry and exit criteria
- Environment and data requirements
- Risk register with mitigations
- Defect severity definitions

### Test case library
42 manual test cases organized by module:
- User login and role-based access
- Transaction processing (cash, credit, split tender)
- Discounts and promotional pricing
- Returns and exchanges
- End-of-day reconciliation

Each test case includes preconditions, step-by-step actions, and expected results.

### Defect log
A realistic defect log with 7 sample bugs including:
- Severity and priority ratings
- Reproduction steps
- Expected vs actual results
- Status tracking (Open, In Progress, Fixed, Closed)

### Automated tests
Regression test suite written in Python using pytest, covering:
- Cart operations and item management
- Payment processing (cash, credit, split tender)
- Discount calculation logic
- Return and refund workflows
- Edge cases and negative scenarios

---

## How to run the automated tests

**Requirements:** Python 3.7+, pytest

```bash
pip install pytest
pytest tests/ -v
```

**Expected output:**
```
tests/test_pos_transactions.py::TestCartOperations::test_add_single_item PASSED
tests/test_pos_transactions.py::TestCartOperations::test_add_multiple_items PASSED
...
14 passed in 0.05s
```

---

## Skills demonstrated

- Test planning and documentation
- Test case design (positive, negative, edge cases)
- Defect lifecycle management
- Python + pytest for automated regression testing
- POS system domain knowledge
- UAT coordination and exit criteria definition
