# 🏗️ Part 4: System Design & Architecture

> For Senior Odoo Developers: How to build systems that don't break at 10 million records.

---

## 4.1 Modularity & Extension Patterns

**Rule of Thumb:** "Inherit, don't Overwrite."

### Designing for Reusability
- **Base Modules:** Create a `my_module_base` for shared models/fields and separate `my_module_ux` or `my_module_reporting` for the UI and logic.
- **Hook Patterns:** Use methods like `_prepare_X` in your base code so that other modules can override just a dictionary instead of the entire logic.
  ```python
  # Good Pattern:
  def _prepare_invoice_vals(self):
      return {'amount': self.total, 'partner_id': self.partner_id.id}
  
  def action_invoice(self):
      vals = self._prepare_invoice_vals()
      return self.env['account.move'].create(vals)
  ```

---

## 4.2 Performance Optimization (The "N+1" Killer)

**Performance is 90% DB access management.**

### 1. Identifying N+1 Queries
- **The Problem:** Accessing a Many2one field in a loop triggers a new SQL query for every iteration.
- **The Solution:** Use `prefetched` recordsets or `mapped()`.
  ```python
  # BAD (triggers N queries):
  for order in orders:
      print(order.partner_id.name) 

  # GOOD (triggers 1-2 queries):
  partners = orders.mapped('partner_id')
  for partner in partners:
      print(partner.name)
  ```

### 2. Database Indexing
- **Essential:** Any field used in a `domain`, `search()`, or `_order` should have `index=True`.
- **Advanced:** Use `_sql_constraints` to create partial or composite indexes for high-frequency filters.

### 3. PostgreSQL Tuning for Odoo
- **Parallel Workers:** Ensure Postgres has enough workers for Odoo's multi-process model.
- **`pg_stat_statements`:** Use this extension to identify the "top 10" slowest queries in production.

---

## 4.3 ORM Best Practices & Anti-patterns

| Topic | Best Practice | Anti-pattern |
|-------|---------------|--------------|
| **`compute`** | Use `store=True` for searchable/frequent fields. | Heavy non-stored computes in list views. |
| **`sudo()`** | Use `sudo()` only for specific security bypasses. | Using `sudo()` as a "lazy fix" for access rights. |
| **`write()`** | Batch updates: `records.write({'state': 'done'})`. | `for r in records: r.write(...)`. |
| **`search()`**| Use `limit` and `order` for large datasets. | `self.env['model'].search([])` without limits. |

---

## 4.4 Scaling Odoo

### Worker Management
Odoo's performance depends on the number of workers:
- **Calculation:** `(2 * CPU cores) + 1`.
- **Soft Limit:** `limit_memory_soft` (~2GB) prevents memory leaks from growing unchecked.
- **Hard Limit:** `limit_memory_hard` (~2.5GB) ensures individual workers don't crash the server.

### Load Balancing (Odoo.sh or On-prem)
1.  **Nginx:** Use for SSL termination and static file caching.
2.  **Longpolling:** Always use a specific port for Chat/Bus notifications to prevent worker starvation.
3.  **Read-Only Replicas:** For very high traffic (reporting), point Read-Only cursors to a Postgres replica.

---

## 4.5 Dealing with Technical Debt

When inheriting from core Odoo modules (e.g., `account`), keep changes minimal. 
> [!WARNING]
> Overriding core methods like `action_post` on invoices can break future migrations. Always call `super()` first and wrap your custom logic in `try/except` if it's non-critical.

---

> **Next**: Finalize with [Part 5 — Interview Tips & Tricks](file:///home/administrator/.gemini/antigravity/brain/90687616-e3a0-46f8-8eb3-10f471ccbcf1/odoo_interview_tips.md)
