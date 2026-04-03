# Intermediate level — questions & answers

> Extends roadmap Q11–Q19.

## ORM: compute, onchange, constraints

### 1. **`store=True` vs `store=False`** on computed fields — trade-offs for search, list views, and recomputation.

**Answer:** **`store=True`** persists the value in the DB: searchable, usable in domains and list views without recomputing every time; recomputed when `@api.depends` fields change. **`store=False`** computes on the fly: lighter DB, but **not searchable** by default and can be expensive if used in list views or heavy logic. Use stored when filtered/ordered often or computation is costly.

### 2. When would you add **`@api.depends`** on a non-stored compute? When is **`inverse`** needed?

**Answer:** **`@api.depends`** is **required** for computed fields so Odoo knows when to recompute (stored or not). For non-stored, it still drives cache invalidation in the UI. **`inverse`** is needed when the compute is **read/write**: user edits the computed field and you must propagate values to dependency fields (e.g. split full name into first/last).

### 3. Compare **`@api.constrains`**, **`@api.onchange`**, and **`_sql_constraints`** — when to use which?

**Answer:** **`@api.constrains`** — server-side validation on create/write; raises **`ValidationError`**; good for cross-field rules. **`@api.onchange`** — UI-only when user changes a field in form; can return warnings; **not** a substitute for DB validation. **`_sql_constraints`** — PostgreSQL-level uniqueness/checks; fast, always enforced, limited to simple SQL expressions.

### 4. How do **`@api.model`**, **`@api.model_create_multi`**, and instance methods differ?

**Answer:** **`@api.model`** — method runs on the **model**, not a specific recordset (`self` is empty recordset); e.g. `create`, schedulers. **`@api.model_create_multi`** — `create` receives a **list of dicts** (batch create in modern Odoo). **Instance methods** — called on a recordset (`self` has ids); business actions like `action_confirm`.

### 5. Explain **`create`**, **`write`**, and **`unlink`** hooks — what can go wrong if you forget `super()`?

**Answer:** Overrides should call **`super()`** so other modules and core logic still run (defaults, mail, followers, constraints). Forgetting **`super()`** can skip **mail tracking**, **stock moves**, **sequence** assignment, or other modules’ extensions — causing subtle production bugs.

### 6. What is **`filtered()`**, **`mapped()`**, **`sorted()`** on recordsets? Give a realistic example.

**Answer:** **`filtered(func)`** — subset matching a condition. **`mapped('field')`** — reads field across records (can return recordset or list of values). **`sorted(key=lambda r: r.date)`** — order recordset in memory.

```python
confirmed = orders.filtered(lambda o: o.state == 'sale')
names = orders.mapped('partner_id.name')
```

### 7. How does **`context`** propagate? Name three common context keys you use in practice.

**Answer:** **`with_context()`** returns a new environment; keys flow to computed fields, defaults, and ORM. Common keys: **`lang`** (translations), **`allowed_company_ids`** / company switching, **`force_company`**, **`mail_create_nosubscribe`**, **`active_id`** / **`active_ids`** for wizards, **`default_*`** for default field values.

## Security

### 8. List the **four security layers** in Odoo (ACL, record rules, field groups, menus).

**Answer:** (1) **Model access** (`ir.model.access`) — CRUD per group. (2) **Record rules** (`ir.rule`) — row-level domain per group. (3) **Field** — `groups=` on fields in views (visibility). (4) **UI** — menu/action `groups` and button `groups`.

### 9. What is the difference between **global** and **group-specific** record rules?

**Answer:** **Global** rules apply to everyone (no `groups` on the rule) — rare, powerful. **Group-specific** rules apply only if the user has that group; users get the **union** of allowed records from all their rules (OR between rules for same model per group semantics — understand your version’s rule combination). Prefer explicit groups for least privilege.

### 10. When is **`sudo()`** justified vs a design smell?

**Answer:** Justified for **clear system tasks** (cron, technical sync) where you’ve already validated inputs, or to read a config record. **Smell** when used to bypass ACLs for normal users — fix **groups**, **record rules**, or **sudo** only around the minimal `env` call with a comment and audit path.

### 11. How do **`groups=`** on buttons and fields interact with ACLs?

**Answer:** **`groups`** hides UI elements; **ACLs** still govern whether the user can **read/write** the model. A user might see a button (wrong group) or miss it — but **RPC** can still call methods unless you check rights in Python. Always enforce **`has_group`** / ACL-sensitive logic in the method for state-changing actions.

### 12. Write (on paper) an **`ir.model.access.csv`** row for a custom model with “user read/write, manager full”.

**Answer:** Two rows, same model, different groups (example names):

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,base.group_user,1,1,1,0
access_my_model_manager,my.model.manager,model_my_model,my_module.group_manager,1,1,1,1
```

## Inheritance & extension

### 13. **Classical extension** (`_inherit` without `_name`) vs **prototype** — when do you create a new `_name`?

**Answer:** **Extension** — you extend `sale.order` in place (same table, more fields/methods). **Prototype** (`_name` + `_inherit`) — you need a **new model** that reuses another’s definition but separate data (new table). Use new `_name` when business entities differ (e.g. `sale.order` vs `rental.order` with extra workflow).

### 14. What is **delegation inheritance** (`_inherits`)? One example use case.

**Answer:** **`_inherits = {'res.partner': 'partner_id'}`** — your model has a delegate Many2one; field access can proxy to the related record. Use case: **`res.users`** extending **`res.partner`** without duplicating partner columns.

### 15. How do you override a standard method **safely** for upgrades?

**Answer:** Call **`super()`** first or last depending on whether you need pre/post behavior; keep **signature** compatible; avoid copying huge core bodies — add **hooks** if upstream provides `_prepare_*`; add **tests**; document **Odoo version** constraints.

## Controllers & integration

### 16. Compare **`type='json'`** vs **`type='http'`** routes; **`auth='user'`** vs **`'public'`**.

**Answer:** **`type='json'`** — JSON-RPC style, returns JSON (legacy json route behavior). **`type='http'`** — full Request/Response, HTML or custom content. **`auth='user'`** — must be logged in. **`auth='public'`** — guest allowed (website); still has `request.env` with public user unless overridden.

### 17. Why is **`csrf`** relevant for HTTP routes? When might you disable it?

**Answer:** **CSRF** tokens prevent cross-site request forgery on state-changing requests. **Disable** only for **token-based API** clients (OAuth, API keys) or machine-to-machine endpoints where you document alternate protection — never blindly for browser forms.

### 18. How would you expose a read-only list of records to an external system — ORM vs raw SQL?

**Answer:** Prefer **`search_read(domain, fields, limit)`** or **`read()`** with minimal fields — respects **ACLs** and **record rules** under `request.env`. Raw SQL bypasses security and cache — only for **aggregates** or **reporting** with explicit filtering and `sudo` awareness.

## Performance (basics)

### 19. What is the **N+1 query** problem in Odoo? How do you reduce it without raw SQL?

**Answer:** Accessing a relational field **per record in a Python loop** triggers repeated queries. Fix: **`mapped()`**, **`prefetch_fields`**, batch **`read()`**, **`with_prefetch()`**, avoid per-row `browse`, and design **stored fields** for list columns.

### 20. Why is **`search([])`** without **`limit`** dangerous in cron or server actions?

**Answer:** Loads **all matching rows** into memory / long transaction — can **OOM** or lock tables. Always use **`limit`**, **`order`**, batching, or **`_auto = False`** models for huge tables; process in chunks in cron.

## Testing

### 21. What is **`TransactionCase`** vs **`HttpCase`**? When do you use **`@tagged('post_install')`**?

**Answer:** **`TransactionCase`** — each test in a transaction rolled back (default for fast model tests). **`HttpCase`** — HTTP client / browser for controller and tour tests. **`@tagged('post_install')`** — run after all modules installed so dependencies and full data exist; use for integration tests that need `sale`, `stock`, etc.
