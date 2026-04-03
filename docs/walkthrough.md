# 🚢 Walkthrough: Odoo Interview Preparation Guide

This comprehensive curriculum was designed to take a developer from junior-level basics to senior-level architectural mastery in Odoo v17–v19.

---

## 🎨 Project Overview

The project is structured into **5 Key Deliverables**, each as a standalone reference document, plus **extra question banks** by level.

### 📂 0. [Question banks by level](levels/README.md)
Additional prompts for Beginner → Senior (with **answers**), System Design, and Business Cases, plus a **[purchase_approval lab](levels/purchase_approval_lab.md)** (prompts only) tied to `custom_addons/purchase_approval/`. Use with the Roadmap and code docs for deeper patterns.

### 📜 1. [Interview Question Roadmap](odoo_interview_roadmap.md)
A categorised list of 27 high-value questions covering:
- **Beginner:** Module structure, basic ORM (CRUD), and XML views.
- **Intermediate:** Advanced ORM (computes, onchanges), security rules, and inheritance.
- **Senior:** Performance (N+1 queries), concurrency, and version differences (v17-v19).

### 💻 2. [Code Examples (Master Guide)](odoo_code_examples.md)
Practical, production-ready code blocks for:
- Full module definition (Approval Workflow).
- Wizards (`TransientModel`) and Scheduled Actions (`ir.cron`).
- Custom REST-style Controllers and Unit Testing (`TransactionCase`).

### ⚡ 2.1 [Advanced Code Examples](odoo_code_examples_advanced.md)
Senior-level technical deep-dives including:
- **OWL Components:** Modern frontend patterns for v17-v19.
- **Mixins:** Adding "Chatter" (logs/activities) to any model.
- **Reporting:** Designing professional QWeb PDF reports.

### 🏢 3. [Real Business Case Studies](odoo_business_cases.md)
Technical solutions for complex integration problems:
- **Supply Chain:** Quality control gates in Warehouse Receipts.
- **Accounting:** Regional tax-exclusive pricing engines.
- **HR:** Dynamic skill-based bonus triggers in Payroll.

### 🏗️ 4. [System Design & Architecture](odoo_system_design.md)
High-level scaling and optimization strategies:
- **Database Tuning:** Common indexing and SQL profiling techniques.
- **Scalability:** Managing workers, memory limits, and load balancing.
- **Maintainability:** Sustainable extension patterns (hooks vs. overrides).

### 🧠 5. [Interview Tips & Tricks](odoo_interview_tips.md)
A "How-To" guide for excelling in the hiring process:
- Applying the **STAR method** to tech interviews.
- Explaining the Odoo lifecycle clearly to stakeholders.
- Avoid common junior pitfalls (like overusing raw SQL).

---

## ✅ Final Project Checklist (Verified)

| Task | Status | Result |
|------|--------|--------|
| **Odoo v17-v19 Diff** | ✅ | Documented new `invisible` attribute and `Properties` fields. |
| **Cross-Module Sync** | ✅ | Balanced cases for Sales, Inventory, and HR. |
| **Logic Verification**| ✅ | All code examples use standard Odoo naming conventions. |
| **Performance Prep** | ✅ | Explicit sections on N+1 and ORM caching. |

---

> [!TIP]
> **Suggested Learning Path**: Start with the [Roadmap](odoo_interview_roadmap.md), drill extra prompts from [levels](levels/README.md), practice the [Code Examples](odoo_code_examples.md), and review [System Design](odoo_system_design.md) for senior-level depth.
