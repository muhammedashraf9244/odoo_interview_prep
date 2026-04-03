# System design — question bank

> Complements [odoo_system_design.md](../odoo_system_design.md). No answers here — discuss trade-offs aloud.

## Module architecture

1. Split a large client requirement into **multiple installable modules** — what criteria determine boundaries?
2. How do you design **`depends`** so that optional features stay optional?
3. When do you use **`data/`** XML vs **Python post-init hooks** vs **migrations**?

## Data modeling

4. You need a **soft delete** pattern — how would you model it in Odoo vs hard `unlink`?
5. How do you model **polymorphic** relations (`reference` field vs separate models)?
6. When are **`Properties`** fields (v17+) appropriate vs normal relational models?

## Integration

7. Design an integration with an external **REST API** (polling vs webhooks). What runs in Odoo?
8. How do you handle **idempotency** when importing the same external document twice?
9. Where do **API keys** and secrets belong (parameters, `ir.config_parameter`, server env)?

## Scale & reliability

10. A batch import must process **100k rows** — outline a safe architecture (cron chunks, limits, errors).
11. How do you avoid **blocking the UI** for long operations?
12. What **observability** do you add (logging structure, failed queue jobs, alerts)?

## Cross-cutting concerns

13. How do you enforce **audit trails** across custom models (mail.thread, custom log table)?
14. Describe **i18n** and **multi-company** implications for stored computed fields and reports.
