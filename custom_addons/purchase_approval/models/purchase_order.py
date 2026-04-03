# models/purchase_order.py
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
            threshold = order.company_id.po_approval_threshold if hasattr(order.company_id, 'po_approval_threshold') else 5000.0
            order.requires_approval = order.amount_total > threshold

    def action_approve(self):
        self.ensure_one()
        if not self.env.user.has_group('purchase_approval.group_purchase_approver'):
            raise UserError(_("You don't have approval rights."))
        self.write({
            'approval_state': 'approved',
            'approved_by': self.env.uid,
            'approval_date': fields.Datetime.now(),
        })

    def button_confirm(self):
        for order in self:
            if order.requires_approval and order.approval_state != 'approved':
                raise UserError(_("Order %s requires approval before confirmation.", order.name))
        return super().button_confirm()
