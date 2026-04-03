# __manifest__.py
{
    'name': 'Purchase Approval Extension (Prep)',
    'version': '17.0.1.0.0',
    'category': 'Inventory/Purchase',
    'summary': 'Sample module for interview prep - Multi-level approval',
    'depends': ['purchase'],
    'data': [
        'security/approval_groups.xml',
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
}
