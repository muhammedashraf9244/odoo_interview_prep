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
