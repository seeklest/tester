# Test Plan: Mock POS System v1.0

**Project:** MockMart POS System  
**Version:** 1.0  
**Prepared by:** Carina Kumar  
**Date:** November 2024  
**Status:** Final

---

## 1. Objective

This test plan outlines the scope, approach, resources, and schedule for testing the MockMart point-of-sale (POS) system. The goal is to validate that core transaction, returns, and end-of-day workflows function correctly and meet business requirements before go-live.

---

## 2. Scope

### In scope
- Transaction processing (cash, credit, debit)
- Item lookup and barcode scanning
- Discount and promotional pricing
- Returns and exchanges
- End-of-day (EOD) reconciliation
- Receipt generation
- User login and role-based access

### Out of scope
- Hardware integration (physical terminals, printers)
- Network/infrastructure testing
- Performance and load testing

---

## 3. Test approach

Manual functional testing will be the primary method for this phase. A subset of high-frequency regression scenarios will also be covered by automated scripts (see `tests/` folder).

| Type | Coverage |
|---|---|
| Functional | Core workflows end-to-end |
| Regression | Transaction and returns flows |
| Negative testing | Invalid inputs, edge cases |
| UAT | Business stakeholder sign-off scenarios |

---

## 4. Entry and exit criteria

### Entry criteria
- Test environment is set up and accessible
- Build has been deployed to QA environment
- Test data (products, users, pricing) is loaded
- Test cases have been reviewed and approved

### Exit criteria
- All high and critical defects are resolved and retested
- 95% of planned test cases executed
- No open P1 or P2 defects
- UAT sign-off received from business stakeholder

---

## 5. Test environment

| Component | Details |
|---|---|
| Application | MockMart POS v1.0 (web-based) |
| Environment | QA environment (qa.mockmart.internal) |
| Browser | Chrome 120+ |
| Test data | Seeded via `test_data_setup.sql` |
| Defect tracking | GitHub Issues |

---

## 6. Roles and responsibilities

| Role | Responsibility |
|---|---|
| QA Tester | Test case execution, defect logging, retesting |
| BA | Requirements clarification, UAT coordination |
| Developer | Defect resolution, build deployment |
| Business Stakeholder | UAT sign-off |

---

## 7. Schedule

| Phase | Start | End |
|---|---|---|
| Test planning | Nov 1 | Nov 5 |
| Test case design | Nov 6 | Nov 10 |
| Environment setup | Nov 6 | Nov 8 |
| Test execution | Nov 11 | Nov 22 |
| Defect retesting | Nov 18 | Nov 25 |
| UAT | Nov 25 | Nov 29 |
| Sign-off | Nov 30 | Nov 30 |

---

## 8. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Test environment unavailable | Medium | High | Escalate to dev lead early; maintain backup access |
| Test data not ready on time | Medium | High | Confirm data setup 2 days before execution starts |
| Defect volume exceeds capacity | Low | Medium | Prioritize P1/P2 fixes; defer P3 to next release |
| Requirement ambiguity | Medium | Medium | BA to review test cases before execution begins |

---

## 9. Defect severity definitions

| Severity | Definition | Example |
|---|---|---|
| P1 - Critical | System crash or data loss; blocks testing | POS freezes on every transaction |
| P2 - High | Major feature broken; no workaround | Returns process fails to refund |
| P3 - Medium | Feature partially working; workaround exists | Discount not applied on split tender |
| P4 - Low | Minor cosmetic or UI issue | Receipt date format inconsistent |

---

## 10. Deliverables

- Test plan (this document)
- Test case library (`TEST_CASES.md`)
- Defect log (`DEFECT_LOG.md`)
- Automated regression scripts (`tests/`)
- Test summary report (post-execution)
