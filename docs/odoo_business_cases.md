# 🏢 Part 3: Real Business Case Studies

> These cases demonstrate how to connect Odoo's core modules (Sales, Purchase, Inventory, Accounting, HR) to solve complex real-world requirements.

---

## 3.1 Case Study: Supply Chain — Multi-step Quality Inspection

**Business Problem:**
A pharmaceutical company needs to ensure all incoming raw materials undergo a "Quality Inspection" before they are available in the main warehouse. If the inspection fails, the goods must be moved to a "Scrap" or "Quarantine" location, and the Purchase team should be notified automatically.

### Technical Design:
1.  **Inventory Routes:** Use a 3-step receipt: `Input` → `Quality Control (QC)` → `Stock`.
2.  **Custom Model:** `quality.check.log` to record individual test results (pH level, purity, etc.).
3.  **Automation:** Automatically create a `quality.check.log` when a transfer enters the `QC` location.

### Implementation Approach:
- **Models:** Inherit `stock.picking` to add a reference to `quality.check.ids`.
- **Workflow:** 
    - Override `button_validate` on `stock.move.line` to prevent movement out of `QC` if a check is pending.
    - Create a server action to "Pass" or "Fail" batches.
- **Notification:** Use `message_post()` to alert the PO manager on failure.

---

## 3.2 Case Study: Accounting — Dynamic Multi-region Tax Engine

**Business Problem:**
A global retailer sells products that have different "Exclusive Tax" structures depending on the delivery region. While Odoo handles standard VAT well, the client requires a custom "Regional Surcharge" that isn't a standard tax but must appear as a separate line in the Journal Entry and Invoice.

### Technical Design:
1.  **Fiscal Positions:** Use Odoo's native Fiscal Positions for standard VAT.
2.  **Compute Engine:** A custom logic on `sale.order` to calculate `surcharge_amount` based on `partner_id.zip_code`.
3.  **Journal Items:** On Invoice confirmation (`action_post`), inject an additional `account.move.line` for the surcharge.

### Implementation Approach:
- **Models:** Inherit `res.partner` with a `region_surcharge_pc` field.
- **Hook:** Use `_prepare_invoice_line` on `sale.order.line` to inject the surcharge logic.
- **ORM:** Ensure the entry balances (`debit == credit`) by adjusting the "Accounts Receivable" line accordingly.

---

## 3.3 Case Study: HR & Payroll — Skill-based Bonus System

**Business Problem:**
A tech firm wants to incentivize employees to complete "Certification Levels" during their first 6 months. Upon completing a specific certification (tracked in HR Skills), the next month's payroll should automatically include a one-time "Knowledge Bonus".

### Technical Design:
1.  **HR Skills:** Use the native `hr.skill` module.
2.  **Payroll Rules:** A custom `hr.salary.rule` with "Python Code" to search for new certifications within the pay period.
3.  **Tracking:** A "Bonus Processed" flag on the skill record to prevent duplicate payments.

### Implementation Approach:
- **Payroll Rule Code:**
    ```python
    # Example logic within a Salary Rule
    new_certs = payslip.employee_id.employee_skill_ids.filtered(
        lambda s: s.skill_type_id.name == 'Certification' and not s.bonus_paid
    )
    result = sum(new_certs.mapped('skill_level_id.bonus_value'))
    ```
- **Lifecycle:** Use a `post_success` hook on the Payslip confirmation to mark `bonus_paid = True` on the employee skills.

---

## 🏗️ Technical Architecture Checklist for Cases
When explaining these in an interview, use this structure:

| Element | Description |
|---------|-------------|
| **Core Dependency** | Which standard modules do we use? (e.g., `stock`, `account`) |
| **Data Integrity** | Are we using `_sql_constraints` to prevent invalid states? |
| **Scalability** | Will this code work if we process 1,000 transfers per hour? |
| **UI/UX** | How does the user know what to do next? (e.g., statusbar colors) |

---

> **Next**: Proceed to [Part 4 — System Design & Architecture](file:///home/administrator/.gemini/antigravity/brain/90687616-e3a0-46f8-8eb3-10f471ccbcf1/odoo_system_design.md)
