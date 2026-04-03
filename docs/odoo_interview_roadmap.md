# 🎯 Odoo Developer Interview Preparation Roadmap

> **From Junior to Senior — A Structured Learning Path**
> Covers Odoo v17, v18, and v19 | References: [v17 Docs](https://www.odoo.com/documentation/17.0/developer/reference.html) · [v18 Docs](https://www.odoo.com/documentation/18.0/developer/reference.html) · [v19 Docs](https://www.odoo.com/documentation/19.0/developer/reference.html)

**Extra question banks:** [levels/README.md](levels/README.md) — Beginner / Intermediate / Senior include answers; [purchase_approval lab](levels/purchase_approval_lab.md) is prompts-only.

---

## 📋 Table of Contents

| Part | Document | Topics |
|------|----------|--------|
| 0 | [Question banks](levels/README.md) | Extra prompts: Beginner → Senior, system design, business cases |
| 1 | **This file** | Interview Question Roadmap (Beginner → Senior) |
| 2 | [Code Examples](odoo_code_examples.md) | Practical code aligned with Odoo v17–v19 |
| 3 | [Business Case Studies](odoo_business_cases.md) | Sales, Purchase, Inventory, Accounting, HR |
| 4 | [System Design & Architecture](odoo_system_design.md) | Scalability, Performance, ORM Best Practices |
| 5 | [Interview Tips & Tricks](odoo_interview_tips.md) | Pitfalls, Communication, Live Coding |

---

# Part 1: Interview Question Roadmap

## 🟢 Level 1 — Beginner (0–1 Year Experience)

### 1.1 Odoo Architecture & Basics

**Q1: What is the Odoo framework architecture?**
> Odoo follows a **3-tier architecture**: Database (PostgreSQL), Application Server (Python/ORM), and Web Client (JavaScript/OWL). The server uses **WSGI** with Werkzeug and can run behind a reverse proxy (Nginx). Modules are self-contained packages with models, views, security, and data files.

**Q2: What is the difference between `odoo.sh`, Community, and Enterprise?**
> - **Community**: Open-source (LGPL), core modules only
> - **Enterprise**: Proprietary license, adds accounting, studio, marketing, etc.
> - **Odoo.sh**: PaaS hosting platform with CI/CD, staging, and production environments

**Q3: Explain the Odoo module structure.**
> ```
> my_module/
> ├── __init__.py          # Python package init
> ├── __manifest__.py      # Module metadata (name, depends, data)
> ├── models/              # Python model definitions
> │   ├── __init__.py
> │   └── my_model.py
> ├── views/               # XML view definitions
> │   └── my_model_views.xml
> ├── security/            # Access control
> │   ├── ir.model.access.csv
> │   └── security.xml     # Record rules
> ├── data/                # Default/demo data
> ├── static/              # Web assets (JS, CSS, images)
> ├── controllers/         # HTTP endpoints
> ├── wizard/              # Transient models
> └── reports/             # QWeb report templates
> ```

**Q4: What is `__manifest__.py` and what are its key fields?**
> The manifest declares module metadata:
> ```python
> {
>     'name': 'My Module',
>     'version': '17.0.1.0.0',
>     'category': 'Sales',
>     'depends': ['sale', 'stock'],
>     'data': [
>         'security/ir.model.access.csv',
>         'views/my_model_views.xml',
>     ],
>     'installable': True,
>     'application': True,
>     'license': 'LGPL-3',
> }
> ```
> Key fields: `name`, `version`, `depends`, `data`, `demo`, `installable`, `auto_install`, `license`.

**Q5: What are the main field types in Odoo?**
> | Category | Fields |
> |----------|--------|
> | Basic | `Char`, `Text`, `Html`, `Integer`, `Float`, `Boolean`, `Date`, `Datetime` |
> | Relational | `Many2one`, `One2many`, `Many2many` |
> | Computed | Any field with `compute=` parameter |
> | Special | `Selection`, `Binary`, `Monetary`, `Reference`, `Properties` (v17+) |

### 1.2 ORM Fundamentals

**Q6: What is the Odoo ORM and why use it over raw SQL?**
> The ORM maps Python classes to PostgreSQL tables. Benefits:
> - Automatic CRUD with access control enforcement
> - Record rules and security applied transparently
> - Cache management and invalidation
> - Computed field recomputation
> - **Never use raw SQL** unless absolutely necessary (reporting, bulk ops) — it bypasses security.

**Q7: Explain `create()`, `write()`, `unlink()`, and `search()`.**
> ```python
> # Create — returns new recordset
> record = self.env['res.partner'].create({'name': 'John'})
> 
> # Write — updates existing records
> record.write({'phone': '123456'})
> 
> # Search — returns recordset matching domain
> partners = self.env['res.partner'].search([('is_company', '=', True)])
> 
> # Unlink — deletes records
> record.unlink()
> ```

**Q8: What is a domain in Odoo? Give examples.**
> A domain is a list of criteria tuples `(field, operator, value)`:
> ```python
> # Simple
> [('state', '=', 'sale')]
> 
> # AND (implicit)
> [('amount', '>', 1000), ('state', '=', 'draft')]
> 
> # OR
> ['|', ('state', '=', 'draft'), ('state', '=', 'sent')]
> 
> # NOT
> ['!', ('active', '=', False)]
> 
> # Nested — (A OR B) AND C
> ['|', ('state', '=', 'draft'), ('state', '=', 'sent'), ('amount', '>', 500)]
> ```

### 1.3 Views & UI

**Q9: What are the main view types in Odoo?**
> `form`, `tree` (list), `kanban`, `calendar`, `pivot`, `graph`, `search`, `gantt` (Enterprise), `map` (Enterprise), `cohort` (Enterprise), `activity`.

**Q10: What is the difference between `<field>`, `<attribute>`, and `xpath` in view inheritance?**
> ```xml
> <!-- xpath: locate and modify elements -->
> <xpath expr="//field[@name='partner_id']" position="after">
>     <field name="custom_field"/>
> </xpath>
> 
> <!-- field + position: shortcut for simple cases -->
> <field name="partner_id" position="after">
>     <field name="custom_field"/>
> </field>
> 
> <!-- attribute: modify properties -->
> <xpath expr="//field[@name='name']" position="attributes">
>     <attribute name="required">1</attribute>
> </xpath>
> ```

---

## 🟡 Level 2 — Intermediate (1–3 Years Experience)

### 2.1 Advanced ORM

**Q11: Explain computed fields with `store=True` vs `store=False`.**
> ```python
> # Stored: written to DB, searchable, auto-recomputed on dependency changes
> total = fields.Float(compute='_compute_total', store=True)
> 
> @api.depends('line_ids.price')
> def _compute_total(self):
>     for rec in self:
>         rec.total = sum(rec.line_ids.mapped('price'))
> 
> # Not stored (default): computed on-the-fly, NOT searchable unless you add search method
> display_name = fields.Char(compute='_compute_display_name')
> ```
> **Key difference**: Stored fields add DB columns, trigger recomputation via `@api.depends`, and are filterable. Non-stored fields are ephemeral.

**Q12: What is `@api.constrains` vs `@api.onchange`?**
> | Feature | `@api.constrains` | `@api.onchange` |
> |---------|-------------------|-----------------|
> | When | Server-side, on `create`/`write` | Client-side, in form view |
> | Purpose | Validate data integrity | UI reactivity / field defaults |
> | Raises | `ValidationError` | No exception, returns warning dict |
> | DB state | Data already in draft transaction | Data NOT yet saved |

**Q13: Explain `sudo()`, `with_user()`, `with_context()`, and `with_company()`.**
> ```python
> # sudo() — bypass access rights (runs as superuser)
> self.sudo().write({'state': 'done'})
> 
> # with_user() — execute as specific user
> self.with_user(user_id).check_access('read')
> 
> # with_context() — add/override context keys
> self.with_context(lang='fr_FR').name_get()
> 
> # with_company() — switch company context (multi-company)
> self.with_company(company_id).create({...})
> ```

**Q14: How does model inheritance work? Explain the 3 types.**
> | Type | `_inherit` | `_name` | Effect |
> |------|-----------|---------|--------|
> | **Extension** | `'sale.order'` | *(omitted)* | Adds fields/methods to existing model |
> | **Prototype** | `'sale.order'` | `'custom.order'` | New model, copies all fields from parent |
> | **Delegation** | — | `'custom.model'` | Uses `_inherits = {'res.partner': 'partner_id'}`, auto-delegates field access |

**Q15: What are server actions, automated actions, and scheduled actions?**
> - **Server Actions** (`ir.actions.server`): Execute code/email on button click or from action menu
> - **Automated Actions** (`base.automation`): Triggered by record events (create, write, delete, time-based)
> - **Scheduled Actions** (`ir.cron`): Run periodically via cron (e.g., every hour, daily)

### 2.2 Security

**Q16: Explain the Odoo security model (4 layers).**
> 1. **Access Rights** (`ir.model.access.csv`): Model-level CRUD permissions per group
> 2. **Record Rules** (`ir.rule`): Row-level filtering with domains per group
> 3. **Field Groups** (`groups=` attribute): Hide fields from specific groups
> 4. **Menu Access** (`groups=` on menuitems): Restrict menu visibility

**Q17: Write an `ir.model.access.csv` example.**
> ```csv
> id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
> access_my_model_user,my.model.user,model_my_model,base.group_user,1,1,1,0
> access_my_model_manager,my.model.manager,model_my_model,my_module.group_manager,1,1,1,1
> ```

**Q18: What is `@api.model` vs `@api.depends` vs `api.ondelete`?**
> - `@api.model`: Method operates on model class, not a recordset (e.g., `create()`)
> - `@api.depends('field1', 'field2')`: Declares compute field dependencies for recomputation
> - `@api.ondelete(at_uninstall=False)`: v15+, defines behavior when records are deleted

### 2.3 Web Controllers & API

**Q19: How do you create a custom HTTP controller?**
> ```python
> from odoo import http
> from odoo.http import request
> 
> class MyController(http.Controller):
>     @http.route('/api/partners', auth='user', type='json', methods=['POST'])
>     def get_partners(self, **kwargs):
>         partners = request.env['res.partner'].search_read(
>             [('is_company', '=', True)],
>             ['name', 'email', 'phone']
>         )
>         return partners
> ```
> - `type='json'`: Expects/returns JSON (RPC-style)
> - `type='http'`: Standard HTTP request/response
> - `auth='public'|'user'|'none'`: Authentication level

---

## 🔴 Level 3 — Senior (3+ Years Experience)

### 3.1 Performance & Optimization

**Q20: What are the top ORM performance anti-patterns?**
> 1. **Browsing in loops** — `for id in ids: self.browse(id)` → Use `self.browse(ids)` once
> 2. **N+1 queries** — Accessing relational fields in a loop without prefetching
> 3. **`search()` + `browse()`** — Use `search()` directly (it returns recordsets)
> 4. **Non-stored computed field with heavy logic** — Store it if used in search/filter
> 5. **Missing indexes** — Add `index=True` on frequently filtered fields
> 6. **Calling `write()` in loops** — Batch: `records.write({...})`

**Q21: How do you optimize a slow list view with 100k+ records?**
> 1. Add `index=True` to filtered fields
> 2. Use stored computed fields instead of on-the-fly
> 3. Add PostgreSQL indexes via `_sql_constraints` or `init()` method
> 4. Use `read_group()` for aggregation views
> 5. Profile with `--log-sql` and `EXPLAIN ANALYZE`
> 6. Consider `auto_join=True` on Many2one fields used in domains

**Q22: Explain `flush()`, `invalidate_cache()`, and ORM caching.**
> ```python
> # flush(): write pending ORM changes to DB (needed before raw SQL)
> self.env['sale.order'].flush_model()       # v16+
> self.env['sale.order'].flush_recordset()   # flush specific records
> 
> # invalidate_cache(): clear ORM cache (needed after raw SQL writes)
> self.env.invalidate_all()  # v16+: replaces invalidate_cache()
> 
> # Raw SQL pattern:
> self.flush_recordset()
> self.env.cr.execute("UPDATE sale_order SET state='done' WHERE id=%s", [self.id])
> self.invalidate_recordset()
> ```

### 3.2 Multi-Company & Multi-Currency

**Q23: How does multi-company work in Odoo?**
> - Models with `_check_company_auto = True` auto-validate company consistency
> - Use `company_id` field with `default=lambda self: self.env.company`
> - Record rules filter by `['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]`
> - Access other company data with `with_company()`
> - `@api.model` methods use `self.env.company`, NOT `self.company_id`

**Q24: How do you handle concurrency in Odoo?**
> - Odoo uses **optimistic locking** via `write_date` / `__last_update`
> - `FOR UPDATE` in raw SQL for pessimistic locking
> - Worker processes share nothing; each request has its own cursor
> - Use `self.env.cr.savepoint()` for atomic sub-transactions
> - Queue jobs via `queue_job` OCA module for async processing

### 3.3 Testing & QA

**Q25: How do you write tests in Odoo?**
> ```python
> from odoo.tests.common import TransactionCase, tagged
> 
> @tagged('post_install', '-at_install')
> class TestSaleOrder(TransactionCase):
>     @classmethod
>     def setUpClass(cls):
>         super().setUpClass()
>         cls.partner = cls.env['res.partner'].create({'name': 'Test'})
>     
>     def test_create_sale_order(self):
>         order = self.env['sale.order'].create({
>             'partner_id': self.partner.id,
>         })
>         self.assertEqual(order.state, 'draft')
>         order.action_confirm()
>         self.assertEqual(order.state, 'sale')
> ```
> Test types: `TransactionCase` (rolled back), `SingleTransactionCase` (persistent), `HttpCase` (with browser tours).

**Q26: How do you debug a production Odoo instance?**
> 1. **Logs** — `--log-level=debug` or `--log-handler=odoo.addons.my_module:DEBUG`
> 2. **SQL** — `--log-sql` to see all queries
> 3. **Shell** — `odoo shell -d mydb` for interactive debugging
> 4. **pdb** — `import pdb; pdb.set_trace()` (dev only)
> 5. **Profiling** — `--dev=all` enables auto-reload + debugger
> 6. **PostgreSQL** — `pg_stat_statements`, `EXPLAIN ANALYZE`

### 3.4 Version Differences (v17 → v18 → v19)

**Q27: What are the key differences between Odoo v17, v18, and v19?**

> | Feature | v17 | v18 | v19 |
> |---------|-----|-----|-----|
> | **Frontend** | OWL 2.x | OWL 2.x refined | OWL 2.x + improvements |
> | **Properties Field** | Introduced | Stabilized | Enhanced |
> | **Asset Bundling** | New asset system | Refined | Further optimized |
> | **Product Type** | `type` field (consumable/storable/service) | Simplified product types | Continued refinement |
> | **POS** | Rewritten in OWL | Polished | New features (DPO, QR) |
> | **Expense Module** | Standard | Restructured (categories, cards) | Enhanced analysis |
> | **Inventory Valuation** | Under product mgmt | Under product mgmt | Separate section |
> | **eCommerce** | Flat structure | Restructured | Config+Design separation |
> | **New Modules** | — | ESG, Stages API | Shopee/Lazada connectors |

> [!IMPORTANT]
> Always check the **upgrade scripts** when migrating between versions. Field renames, model
> splits, and API changes can break custom modules silently.

---

## 📊 Topic Coverage Matrix

| Topic | Beginner | Intermediate | Senior |
|-------|----------|-------------|--------|
| Module Structure | ✅ Q3, Q4 | | |
| ORM CRUD | ✅ Q6, Q7 | ✅ Q11, Q13 | ✅ Q20, Q22 |
| Fields & Types | ✅ Q5 | ✅ Q11 | |
| Domains | ✅ Q8 | | |
| Views | ✅ Q9, Q10 | | |
| Inheritance | | ✅ Q14 | |
| Security | | ✅ Q16, Q17 | ✅ Q23 |
| API Decorators | | ✅ Q12, Q18 | |
| Controllers | | ✅ Q19 | |
| Performance | | | ✅ Q20, Q21 |
| Concurrency | | | ✅ Q24 |
| Testing | | | ✅ Q25, Q26 |
| Version Diffs | | | ✅ Q27 |

---

> **Next**: See [Part 2 — Code Examples](file:///home/administrator/.gemini/antigravity/brain/90687616-e3a0-46f8-8eb3-10f471ccbcf1/odoo_code_examples.md) for practical implementations.
