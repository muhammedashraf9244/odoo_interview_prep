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
