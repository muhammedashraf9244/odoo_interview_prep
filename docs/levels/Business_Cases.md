# Business cases — question bank

> Complements [odoo_business_cases.md](../odoo_business_cases.md). Use STAR-style answers in real interviews. No solutions here.

## Sales

1. **Discount approval:** Orders above X or with margin below Y need sales manager approval before confirmation. What do you extend, and where can users bypass the rule if you are careless?
2. **Delivery blocks:** Block delivery order validation until a **custom checklist** is complete. Which models and entry points?
3. **Multi-step quotation:** Customer accepts quote online — how do you sync to Odoo (portal, API, manual)?

## Purchase

4. **Vendor onboarding:** New vendor requires document upload and approval before first PO. Outline data model and workflow.
5. **Blanket orders:** Link multiple POs to a **framework agreement** with remaining budget. Key fields and validations?
6. **Three-way match:** Receive invoice only when PO + receipt quantities align within tolerance. Where is the logic?

## Inventory

7. **QC gate:** Goods cannot move from **receipt** to **stock** until inspection passes. Route vs custom validation?
8. **Serial traceability:** Recall scenario — find all customers who received a given lot. Which reports/models?
9. **Consignment stock:** Partner-owned inventory at your warehouse — how does ownership reflect in Odoo (high level)?

## Accounting

10. **Inter-company:** Sale in company A, fulfillment in company B — what standard or custom pieces are involved?
11. **Deferred revenue:** SaaS subscription invoiced yearly, recognize monthly. Standard modules vs customization?
12. **Bank reconciliation** at volume: reduce manual matching — rules, imports, or custom matching engine?

## HR

13. **Leave accrual by seniority:** Different rates after N years — payroll rule vs scheduled computation?
14. **Expense policy:** Per-diems by country and job level — configuration vs code?

## Cross-functional

15. **Return merchandise authorization (RMA):** Link sales return, pickings, and credit note — workflow outline.
16. **KPI dashboard:** Real-time sales vs target by team — ORM, SQL view, or reporting engine?
