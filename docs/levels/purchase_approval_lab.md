# Lab: `purchase_approval` sample module

Sample path: `odoo_interview_prep/custom_addons/purchase_approval/`.

## Module bootstrap

1. What does the **root** `__init__.py` import, and why must the `models/` package expose submodules?
2. Trace loading order: **`__manifest__.py`** → **`depends`** → Python imports. What happens if `depends` is wrong?
3. Is the **`license`** field important for Community vs Enterprise distribution?

## This module’s code

4. **`_inherit = 'purchase.order'`** — what does this mean for the database and for upgrades?
5. **`requires_approval`** is computed with **`store=True`** — why store it? What depends on **`company_id`** and **`amount_total`**?
6. The compute uses **`hasattr(order.company_id, 'po_approval_threshold')`** — is this a good pattern? What would you prefer in production?
7. **`action_approve`** checks **`has_group`** then **`write`**. Could a user bypass approval via RPC? What else would you enforce?
8. **`button_confirm`** is overridden — why call **`super()`** last? What breaks if you forget?
9. **`approved_by`** uses **`self.env.uid`** in `write` — alternative APIs for “current user”?

## Views & UX

10. The **Approve** button uses **`invisible=`** with **`requires_approval`** — what happens if `requires_approval` is recomputed after lines change?
11. **`statusbar`** with **`statusbar_visible`** — what is the user experience trade-off vs showing all states?

## Security

12. **`ir.model.access.csv`** references **`purchase_approval.group_purchase_approver`** — why include the module prefix in `group_id:id`?
13. Does this module need **record rules** for `purchase.order`, or are standard purchase rules enough? When would you add one?

## Stretch

14. Add **reject** flow and **chatter** messages — which mixins and methods?
15. Write **tests** (names only) you would add for approval threshold edge cases.
