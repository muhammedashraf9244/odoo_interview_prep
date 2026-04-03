# 🎯 Odoo Developer Interview Preparation Roadmap

> **From Junior to Senior — A Structured Learning Path**
> Covers Odoo v17, v18, and v19 | References: [v17 Docs](https://www.odoo.com/documentation/17.0/developer/reference.html) · [v18 Docs](https://www.odoo.com/documentation/18.0/developer/reference.html) · [v19 Docs](https://www.odoo.com/documentation/19.0/developer/reference.html)

---

## Developer levels

Use these tiers to pick what to study first and what interviewers usually expect. Experience ranges are indicative (project complexity matters more than years).

| Level | Typical experience | What you are expected to do | Question & answer practice |
|-------|-------------------|-----------------------------|------------------------------|
| **Junior / Beginner** | 0–1 year Odoo | Module layout, manifest, basic models and fields, domains, form/list views, view inheritance, ORM `create` / `write` / `search`, debugging with logs and developer mode | [docs/levels/Beginner_Level.md](docs/levels/Beginner_Level.md) |
| **Intermediate** | 1–3 years | Stored computes, `constrains` vs `onchange`, security (ACL + record rules), `sudo` / context / multi-company basics, controllers, inheritance patterns, tests, performance awareness (N+1, batching) | [docs/levels/Intermediate_Level.md](docs/levels/Intermediate_Level.md) |
| **Senior** | 3+ years | ORM cache / flush / raw SQL safety, indexing and profiling, concurrency and jobs, scaling workers and deployment concerns, upgrade-safe overrides, OWL at a high level | [docs/levels/Senior_Level.md](docs/levels/Senior_Level.md) |
| **System / architecture** | Often overlaps Senior | Splitting modules, integrations, data modeling trade-offs, batch imports, observability | [docs/levels/System_Design.md](docs/levels/System_Design.md) + [docs/odoo_system_design.md](docs/odoo_system_design.md) |
| **Business / functional depth** | Any level with domain focus | End-to-end flows (Sales, Purchase, Stock, Accounting, HR), scoping and trade-offs | [docs/levels/Business_Cases.md](docs/levels/Business_Cases.md) + [docs/odoo_business_cases.md](docs/odoo_business_cases.md) |

**Sample module in this repo:** [custom_addons/purchase_approval/](custom_addons/purchase_approval/) — practice questions in [docs/levels/purchase_approval_lab.md](docs/levels/purchase_approval_lab.md).

**Index of all level files:** [docs/levels/README.md](docs/levels/README.md).

---

## 📋 Table of Contents

| Part | Document | Topics |
|------|----------|--------|
| 0 | [Developer levels](#developer-levels) | Junior → Senior, system design, business cases |
| 1 | **This file** | Interview Question Roadmap (Beginner → Senior) |
| 2 | [Code Examples](file:///home/administrator/.gemini/antigravity/brain/90687616-e3a0-46f8-8eb3-10f471ccbcf1/odoo_code_examples.md) | Practical code aligned with Odoo v17–v19 |
| 3 | [Business Case Studies](file:///home/administrator/.gemini/antigravity/brain/90687616-e3a0-46f8-8eb3-10f471ccbcf1/odoo_business_cases.md) | Sales, Purchase, Inventory, Accounting, HR |
| 4 | [System Design & Architecture](file:///home/administrator/.gemini/antigravity/brain/90687616-e3a0-46f8-8eb3-10f471ccbcf1/odoo_system_design.md) | Scalability, Performance, ORM Best Practices |
| 5 | [Interview Tips & Tricks](file:///home/administrator/.gemini/antigravity/brain/90687616-e3a0-46f8-8eb3-10f471ccbcf1/odoo_interview_tips.md) | Pitfalls, Communication, Live Coding |

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
# 🧑‍💻 Part 2: Code Examples (Odoo v17–v19)

> Practical, production-ready patterns inspired by the official Odoo documentation.

---

## 2.1 Complete Module: Custom Approval Workflow

### `__manifest__.py`
```python
{
    'name': 'Purchase Approval Extension',
    'version': '17.0.1.0.0',
    'category': 'Inventory/Purchase',
    'summary': 'Adds multi-level approval to purchase orders',
    'depends': ['purchase'],
    'data': [
        'security/approval_groups.xml',
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'data/mail_template_data.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
}
```

### `models/purchase_order.py` — Extending an Existing Model
```python
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    approval_state = fields.Selection([
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Approval Status', default='pending', tracking=True)

    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approval_date = fields.Datetime(string='Approval Date', readonly=True)
    requires_approval = fields.Boolean(
        compute='_compute_requires_approval', store=True,
        help='Orders above threshold require manager approval'
    )

    @api.depends('amount_total', 'company_id')
    def _compute_requires_approval(self):
        for order in self:
            threshold = order.company_id.po_approval_threshold or 5000.0
            order.requires_approval = order.amount_total > threshold

    def action_approve(self):
        """Manager approves the purchase order."""
        self.ensure_one()
        if not self.env.user.has_group('purchase_approval.group_purchase_approver'):
            raise UserError(_("You don't have approval rights."))
        self.write({
            'approval_state': 'approved',
            'approved_by': self.env.uid,
            'approval_date': fields.Datetime.now(),
        })
        # Send notification
        self._send_approval_notification()

    def action_reject(self):
        self.ensure_one()
        self.approval_state = 'rejected'

    def button_confirm(self):
        """Override to enforce approval before confirmation."""
        for order in self:
            if order.requires_approval and order.approval_state != 'approved':
                raise UserError(_(
                    "Order %s requires approval before confirmation (Amount: %s).",
                    order.name, order.amount_total
                ))
        return super().button_confirm()

    def _send_approval_notification(self):
        template = self.env.ref('purchase_approval.mail_template_po_approved')
        template.send_mail(self.id, force_send=True)
```

### `security/approval_groups.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="group_purchase_approver" model="res.groups">
        <field name="name">Purchase Approver</field>
        <field name="category_id" ref="base.module_category_inventory_purchase"/>
        <field name="implied_ids" eval="[(4, ref('purchase.group_purchase_manager'))]"/>
    </record>
</odoo>
```

### `security/ir.model.access.csv`
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_purchase_order_approver,purchase.order.approver,purchase.model_purchase_order,group_purchase_approver,1,1,1,0
```

### `views/purchase_order_views.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="purchase_order_form_inherit_approval" model="ir.ui.view">
        <field name="name">purchase.order.form.approval</field>
        <field name="model">purchase.order</field>
        <field name="inherit_id" ref="purchase.purchase_order_form"/>
        <field name="arch" type="xml">
            <!-- Add approval buttons in the header -->
            <xpath expr="//header" position="inside">
                <button name="action_approve" string="Approve"
                        type="object" class="btn-primary"
                        invisible="approval_state != 'pending' or not requires_approval"
                        groups="purchase_approval.group_purchase_approver"/>
                <button name="action_reject" string="Reject"
                        type="object" class="btn-danger"
                        invisible="approval_state != 'pending' or not requires_approval"
                        groups="purchase_approval.group_purchase_approver"/>
                <field name="approval_state" widget="statusbar"
                       statusbar_visible="pending,approved"
                       invisible="not requires_approval"/>
            </xpath>

            <!-- Add approval info after partner field -->
            <xpath expr="//field[@name='partner_id']" position="after">
                <field name="requires_approval" invisible="1"/>
                <field name="approved_by" invisible="approval_state != 'approved'"/>
                <field name="approval_date" invisible="approval_state != 'approved'"/>
            </xpath>
        </field>
    </record>
</odoo>
```

> [!NOTE]
> **v17+ Change**: The `attrs` attribute (used in v16 and below) is replaced by direct `invisible`, `required`, `readonly` attributes on elements. No more `attrs="{'invisible': [('field', '=', value)]}"`.

---

## 2.2 Wizard (Transient Model)

```python
from odoo import models, fields, api

class PurchaseMassApproval(models.TransientModel):
    _name = 'purchase.mass.approval'
    _description = 'Mass Approve Purchase Orders'

    order_ids = fields.Many2many('purchase.order', string='Orders to Approve')
    note = fields.Text('Approval Note')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids', [])
        orders = self.env['purchase.order'].browse(active_ids).filtered(
            lambda o: o.requires_approval and o.approval_state == 'pending'
        )
        res['order_ids'] = [(6, 0, orders.ids)]
        return res

    def action_mass_approve(self):
        for order in self.order_ids:
            order.action_approve()
        return {'type': 'ir.actions.act_window_close'}
```

---

## 2.3 Scheduled Action (Cron Job)

```python
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _cron_auto_cancel_expired_rfq(self):
        """Cancel RFQs not confirmed after 30 days."""
        deadline = fields.Datetime.subtract(fields.Datetime.now(), days=30)
        expired_orders = self.search([
            ('state', '=', 'draft'),
            ('create_date', '<', deadline),
        ])
        expired_orders.button_cancel()
        _logger.info("Auto-cancelled %d expired RFQs", len(expired_orders))
```

```xml
<record id="ir_cron_auto_cancel_rfq" model="ir.cron">
    <field name="name">Auto-cancel Expired RFQs</field>
    <field name="model_id" ref="purchase.model_purchase_order"/>
    <field name="state">code</field>
    <field name="code">model._cron_auto_cancel_expired_rfq()</field>
    <field name="interval_number">1</field>
    <field name="interval_type">days</field>
    <field name="numbercall">-1</field>
</record>
```

---

## 2.4 Custom Controller (REST-style API)

```python
import json
from odoo import http
from odoo.http import request, Response

class PurchaseAPI(http.Controller):

    @http.route('/api/v1/purchase-orders', auth='user', type='json',
                methods=['GET'], csrf=False)
    def list_orders(self, **kwargs):
        """List purchase orders for the authenticated user."""
        domain = [('state', 'in', ['draft', 'sent', 'purchase'])]
        limit = kwargs.get('limit', 20)
        offset = kwargs.get('offset', 0)

        orders = request.env['purchase.order'].search_read(
            domain,
            fields=['name', 'partner_id', 'amount_total', 'state', 'date_order'],
            limit=limit,
            offset=offset,
            order='date_order desc'
        )
        total = request.env['purchase.order'].search_count(domain)
        return {'data': orders, 'total': total}

    @http.route('/api/v1/purchase-orders/<int:order_id>/approve',
                auth='user', type='json', methods=['POST'], csrf=False)
    def approve_order(self, order_id, **kwargs):
        order = request.env['purchase.order'].browse(order_id)
        if not order.exists():
            return {'error': 'Order not found', 'status': 404}
        order.action_approve()
        return {'success': True, 'order': order.name}
```

---

## 2.5 Unit Test

```python
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import UserError

@tagged('post_install', '-at_install')
class TestPurchaseApproval(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Vendor Test'})
        cls.product = cls.env['product.product'].create({
            'name': 'Test Product', 'list_price': 10000.0,
        })
        # Create user with approver rights
        cls.approver = cls.env['res.users'].create({
            'name': 'Approver', 'login': 'approver@test.com',
            'groups_id': [(4, cls.env.ref('purchase_approval.group_purchase_approver').id)],
        })

    def _create_order(self, amount=6000):
        order = self.env['purchase.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_qty': 1,
                'price_unit': amount,
            })],
        })
        return order

    def test_order_requires_approval_above_threshold(self):
        order = self._create_order(amount=6000)
        self.assertTrue(order.requires_approval)

    def test_order_no_approval_below_threshold(self):
        order = self._create_order(amount=1000)
        self.assertFalse(order.requires_approval)

    def test_cannot_confirm_without_approval(self):
        order = self._create_order(amount=6000)
        with self.assertRaises(UserError):
            order.button_confirm()

    def test_approve_then_confirm(self):
        order = self._create_order(amount=6000)
        order.with_user(self.approver).action_approve()
        self.assertEqual(order.approval_state, 'approved')
        order.button_confirm()
        self.assertEqual(order.state, 'purchase')
```

---

## 2.6 Version-Specific Patterns

### v17: `invisible` attribute (replaces `attrs`)
```xml
<!-- v16 and below (DEPRECATED) -->
<field name="field_a" attrs="{'invisible': [('state', '!=', 'draft')]}"/>

<!-- v17+ (NEW) -->
<field name="field_a" invisible="state != 'draft'"/>
```

### v17+: Properties Fields (Dynamic Fields)
```python
class ProjectTask(models.Model):
    _inherit = 'project.task'

    # Properties are dynamic fields defined per parent record
    task_properties = fields.Properties(
        string='Properties',
        definition='project_id.task_properties_definition',
    )
```

### v19: Enhanced Expense Module
```python
# v19 introduces expense categories and expense cards
class HrExpenseCategory(models.Model):
    _name = 'hr.expense.category'  # New in v19
    _description = 'Expense Category'
```

---

> **Next**: See [Part 3 — Business Case Studies](file:///home/administrator/.gemini/antigravity/brain/90687616-e3a0-46f8-8eb3-10f471ccbcf1/odoo_business_cases.md)
# 🚀 Part 2.1: Advanced Code Examples (Odoo v17–v19)

> This section covers advanced ORM patterns, UI components, and reporting.

---

## 2.7 Multi-record Handling & Constraints

### Advanced Relational Fields (O2M/M2M)
```python
class Project(models.Model):
    _name = 'custom.project'
    _description = 'Sophisticated Project Model'

    name = fields.Char(required=True)
    # One2many: requires inverse_name in child model
    task_ids = fields.One2many('custom.project.task', 'project_id', string='Tasks')
    
    # Many2many: Odoo creates a middle table automatically
    tag_ids = fields.Many2many('res.partner.category', string='Tags')

    @api.constrains('task_ids')
    def _check_task_limit(self):
        for project in self:
            if len(project.task_ids) > 100:
                raise ValidationError("A project cannot have more than 100 tasks.")

class ProjectTask(models.Model):
    _name = 'custom.project.task'
    _description = 'Project Task'

    project_id = fields.Many2one('custom.project', ondelete='cascade')
    name = fields.Char(required=True)
    priority = fields.Selection([('0', 'Low'), ('1', 'High')], default='0')
```

### SQL Constraints vs Python Constraints
```python
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # SQL Constraints: Handled by PostgreSQL (Fastest, strictly enforced)
    _sql_constraints = [
        ('unique_barcode', 'unique(barcode)', 'The barcode must be unique!'),
        ('check_price', 'check(list_price >= 0)', 'Price must be positive.'),
    ]

    # Python Constraints: For complex logic involving multiple fields/models
    @api.constrains('list_price', 'standard_price')
    def _check_margins(self):
        for product in self:
            if product.list_price < product.standard_price:
                raise ValidationError("Selling price cannot be lower than cost price.")
```

---

## 2.8 Mixins & Chatter Integration (Essential for Business Apps)

To add the **Log Note**, **Schedule Activity**, and **Followers** features to your custom model:

```python
class CustomContract(models.Model):
    _name = 'custom.contract'
    # Inherit from mail mixins
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Contract with Chatter'

    name = fields.Char(tracking=True) # tracking=True logs changes in Chatter
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed')
    ], default='draft', tracking=True)
```

### Corresponding XML View
```xml
<record id="custom_contract_view_form" model="ir.ui.view">
    <field name="model">custom.contract</field>
    <field name="arch" type="xml">
        <form>
            <sheet>
                <field name="name"/>
                <field name="state"/>
            </sheet>
            <!-- Chatter section -->
            <div class="oe_chatter">
                <field name="message_follower_ids"/>
                <field name="activity_ids"/>
                <field name="message_ids"/>
            </div>
        </form>
    </field>
</record>
```

---

## 2.9 QWeb PDF Reports

Reports are defined in two parts: the Action and the Template.

### Report Action (`reports/contract_report.xml`)
```xml
<record id="action_report_custom_contract" model="ir.actions.report">
    <field name="name">Contract Report</field>
    <field name="model">custom.contract</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">my_module.report_contract_template</field>
    <field name="report_file">my_module.report_contract_template</field>
    <field name="binding_model_id" ref="model_custom_contract"/>
    <field name="binding_type">report</field>
</record>
```

### Report Template
```xml
<template id="report_contract_template">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="o">
            <t t-call="web.external_layout">
                <div class="page">
                    <h2>Contract: <span t-field="o.name"/></h2>
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Description</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><span t-field="o.name"/></td>
                                <td><span t-field="o.state"/></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </t>
        </t>
    </t>
</template>
```

---

## 2.10 OWL Component Fundementals (The "Modern" Way)

In v17-v19, Odoo's UI is built with **OWL (Odoo Website Library)**. Senior candidates should know how to create a basic component.

### `static/src/components/my_widget/my_widget.js`
```javascript
/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class MyCounter extends Component {
    static template = "my_module.CounterTemplate";

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
    }
}

// Register as a field widget or a global component
registry.category("views").add("my_counter", MyCounter);
```

### `static/src/components/my_widget/my_widget.xml`
```xml
<templates xml:space="preserve">
    <t t-name="my_module.CounterTemplate">
        <div class="p-4 border rounded shadow-sm bg-white">
            <h4 class="text-primary">Counter: <t t-esc="state.value"/></h4>
            <button class="btn btn-secondary" t-on-click="increment">
                Click Me!
            </button>
        </div>
    </t>
</templates>
```

---

## 2.11 Multi-Company Design Pattern

When designing for multi-company environments, compliance is key.

```python
class CompanySpecificData(models.Model):
    _name = 'custom.data'
    _check_company_auto = True # Enforces company consistency on relational fields

    name = fields.Char()
    company_id = fields.Many2one(
        'res.company', 
        required=True, 
        default=lambda self: self.env.company
    )
    
    # Use 'company_dependent=True' for values that vary per company
    # (e.g., an account number for the same product in different companies)
    value = fields.Float(company_dependent=True)

    # When searching in code, Odoo auto-applies current company to domain.
    # To bypass:
    def get_all_companies_data(self):
        return self.sudo().search([])
```

---

> [!TIP]
> **Performance Trick**: Use `mapped()` and `filtered()` on recordsets to avoid nested loops and unnecessary database hits.
> `names = self.order_line.mapped('product_id.name')` is much faster and cleaner than a manual for-loop.

---

> **Next**: Proceed to [Part 3 — Business Case Studies](file:///home/administrator/.gemini/antigravity/brain/90687616-e3a0-46f8-8eb3-10f471ccbcf1/odoo_business_cases.md) to see how these patterns apply to real-world problems.
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
# 🏁 Part 5: Interview Tips & Tricks

> Practical advice for landing the job — from soft skills to whiteboarding.

---

## 5.1 Common Pitfalls in Odoo Interviews

Avoid these "red flag" answers:
1.  **Over-using Raw SQL:** If you say "I'll use `cr.execute()`" for a simple record update, you fail. The interviewers want to see that you understand and trust the ORM's security and cache management.
2.  **Modifying Core Modules In-Place:** Never suggest editing Odoo's original source code. Always emphasize **inheritance (`_inherit`)**.
3.  **Ignoring Security:** Don't forget that a module is incomplete without an `ir.model.access.csv` file. 
4.  **Misunderstanding the Registry:** If asked how Odoo "knows" about your model, be sure to explain the `_name` and the `__init__.py` registration lifecycle.

---

## 5.2 How to Explain Odoo Concepts Clearly

When asked "How does X work?", follow this **Layered Explanation** method:
1.  **What it is:** (The definition) e.g., "A many2one field is a database relation..."
2.  **Why we use it:** (The business value) "...that allows us to link one record to another, like a sale order to a customer."
3.  **How it's handled:** (Technical internal) "Under the hood, it's a foreign key with an index for efficiency."

---

## 5.3 Approaching Live Coding & Debugging

If given a 15-minute challenge:
- **Think Aloud:** State your assumptions. "I'm assuming we're on Odoo v17, so I'll use the `invisible` attribute instead of `attrs`."
- **Check the Logs First:** If the code crashes, go straight to the Python console/log. Show that you can interpret Tracebacks.
- **Start with the Simple Case:** Get the basic logic working, then optimize for performance or edge cases.
- **The "Safety First" Rule:** If you're doing something risky, say: "In production, I would wrap this in a `try-except` and use `_logger.error`."

---

## 5.4 Using the STAR Method for Business Cases

Interviewers love the **STAR** method for the "Technical Case Study" round:
- **(S) Situation:** "The client had 50,000 monthly invoices that were reconciled manually."
- **(T) Task:** "My goal was to automate 90% of the bank statement imports."
- **(A) Action:** "I built a custom reconciliation model in the `account` module using the `mapped()` field pattern for speed."
- **(R) Result:** "Monthly reconciliation time dropped from 3 days to 2 hours."

---

## 5.5 Senior Perspective: The "Big Picture"

For senior roles, interviewers look for more than just code:
- **Upgrades:** Mention that you design code with **migrations** in mind (minimizing overrides).
- **Security Audit:** Discuss how you sanitize inputs in controllers using `werkzeug` and Odoo's native CSRF protection.
- **Team Growth:** Mention that you use **unit tests** (`TransactionCase`) and **docstrings** to help junior developers understand your modules.

---

> [!TIP]
> **Closing the Interview**: Always ask one high-level technical question back.
> *Example*: "How does your team handle database migrations between Odoo Enterprise versions for large-scale databases?" This shows you understand the lifecycle of Odoo, not just the code.

---

> **Final Step**: [Walkthrough of the Entire Prep Guide](file:///home/administrator/.gemini/antigravity/brain/90687616-e3a0-46f8-8eb3-10f471ccbcf1/walkthrough.md)
