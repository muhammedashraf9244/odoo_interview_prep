# Beginner level — questions & answers

> Aligns with roadmap Q1–Q10; extends with extra prompts.

## Python (Odoo-relevant)

### 1. What is the difference between a **list** and a **tuple**? When might you return a tuple from an Odoo method?

**Answer:** A **list** is mutable (you can append, assign by index). A **tuple** is immutable. In Odoo, many APIs return tuples for **fixed small structures**, e.g. `name_get()` returns `[(id, display_name), ...]`, ORM commands use tuples like `(0, 0, vals)` for O2M lines, and domains are lists of tuples. Returning a tuple signals “this sequence should not be mutated by callers.”

### 2. Explain **mutable vs immutable** types. Why does that matter when you pass default values (e.g. `[]` in function defaults)?

**Answer:** **Mutable** objects (list, dict, set) can change in place; **immutable** (int, str, tuple, frozenset) cannot. Using a mutable default like `def f(x=[])` is wrong: the same list is reused across calls, so state leaks between invocations. Use `def f(x=None): x = x or []` instead. Odoo model defaults usually use `default=lambda self: ...` or immutable literals.

### 3. What is a **dictionary**? How does Odoo use dict-like structures in `create()` / `write()`?

**Answer:** A **dict** maps keys to values (`{'field_name': value}`). `create(vals)` and `write(vals)` take a dict of field names to values for scalar fields; for One2many/Many2many they use **command tuples** in lists. `read()` / `search_read()` return list of dicts per record.

### 4. What are `*args` and `**kwargs`? Where do you see `kwargs` in controllers or `create` overrides?

**Answer:** `*args` collects positional arguments into a tuple; `**kwargs` collects keyword arguments into a dict. HTTP controllers often use `**kwargs` for query/body parameters. When overriding `create`, you may see `def create(self, vals_list)` (v13+) or unpacking; `super().create(vals)` passes the dict through. Always forward `**kwargs` if the parent signature accepts optional keys.

### 5. What is a **list comprehension**? Rewrite a simple `for` loop that builds a list of IDs as a comprehension.

**Answer:** A compact syntax `[expr for x in iterable if cond]`.

```python
# loop
ids = []
for r in orders:
    ids.append(r.id)

# comprehension
ids = [r.id for r in orders]
# or recordset: orders.ids (preferred on recordsets)
```

## Odoo fundamentals

### 6. What are the roles of **`__manifest__.py`**, **`__init__.py`** (root and packages), and **`depends`**?

**Answer:** **`__manifest__.py`** declares module metadata: name, version, `depends`, `data` files to load, assets, license, etc. **`__init__.py`** makes Python treat directories as packages and imports subpackages (e.g. `from . import models`). **`depends`** lists modules that must be loaded before this one so models, XML IDs, and security exist when your code runs.

### 7. What is **`_name`** vs **`_inherit`** vs **`_inherits`** (high level only)?

**Answer:** **`_name`** defines the **technical name** of a new model (new table). **`_inherit`** **extends** an existing model (same table or Python mixin pattern); no new `_name` means you add behavior to e.g. `sale.order`. **`_inherits`** is **delegation**: one model embeds another via a Many2one “delegate” field (e.g. `res.partner` fields exposed on `res.users`).

### 8. Name five common **field types** and one use case for each.

**Answer:** Examples: **`Char`** — name, reference; **`Many2one`** — link to parent record; **`One2many`** — order lines from header; **`Float`** — quantity with `digits`; **`Boolean`** — flags; **`Selection`** — workflow states; **`Datetime`** — when something happened; **`Monetary`** — amounts with currency. Any five with sensible uses is fine.

### 9. What is **`required=True`**, **`readonly=True`**, **`copy=False`** on a field?

**Answer:** **`required=True`** — value must be set (DB NOT NULL where applicable). **`readonly=True`** — cannot edit in UI (ORM can still write if business code allows). **`copy=False`** — field is omitted when duplicating a record (`copy()`), useful for computed state or sequences.

### 10. What is a **domain**? Write a domain for “partners that are companies and active”.

**Answer:** A **domain** is a list of criteria (prefix operators `|`, `!`, `&`) used by `search()` and record rules.

```python
[('is_company', '=', True), ('active', '=', True)]
```

### 11. What do **`search()`**, **`browse()`**, **`exists()`**, and **`ensure_one()`** do?

**Answer:** **`search(domain)`** queries the DB and returns a recordset. **`browse(ids)`** wraps ids into a recordset without checking existence (lazy). **`exists()`** returns only records that still exist in DB. **`ensure_one()`** raises if the recordset is not exactly one record — use when logic assumes singleton.

### 12. What is **`default_get`** and when is it used?

**Answer:** **`default_get(fields_list)`** is called when opening a new record form to compute default values for fields (from context, other defaults, or onchange-like logic). Override it on models or wizards to prefill fields from `active_id`, session, etc.

### 13. What is the difference between **`UserError`** and **`ValidationError`**?

**Answer:** **`UserError`** — business rule or usability message (often shown for “cannot confirm”, access denied messaging). **`ValidationError`** — **data integrity** / constraint failure, typically from `@api.constrains`. Both are user-facing; use ValidationError for validation semantics, UserError for workflow blocks.

## Views & UI

### 14. Name at least six **view types** in Odoo.

**Answer:** e.g. `form`, `tree` (list), `kanban`, `search`, `calendar`, `pivot`, `graph`, `activity` (and optionally `gantt`, `map` in Enterprise).

### 15. What is **view inheritance**? What is the purpose of **`inherit_id`** and **`xpath`**?

**Answer:** **View inheritance** extends or alters an existing view without copying it. **`inherit_id`** points to the base view XML ID. **`xpath`** locates nodes in the base arch (`expr`, `position`) to insert/replace attributes — needed when no direct `field` anchor exists.

### 16. In v17+, how do **`invisible`**, **`readonly`**, **`required`** differ from legacy **`attrs`**?

**Answer:** In v17+, these are **Python-like expressions** on the node (e.g. `invisible="state != 'draft'"`) instead of `attrs="{'invisible': [('state', '!=', 'draft')]}"`. Same semantics, cleaner XML; still evaluated server-side for consistency.

### 17. What is a **search view**? What are **filters** and **group by**?

**Answer:** The **search view** defines search fields, **filters** (preset domains, often with `separator`), and **group by** options (`context` with `group_by`). It drives the search panel above list/kanban.

## Debugging & workflow

### 18. You upgrade a module and the UI shows old fields — what do you check first (caching, assets, module version)?

**Answer:** Confirm the **module is upgraded** (`Apps` → Upgrade), **restart** the server if needed, hard-refresh or clear **browser cache**, and in dev use **regenerate assets** / disable asset bundling. Also verify the **view XML** is in `data` and loaded without error in the log.

### 19. Where do you look when a traceback points to your custom Python file?

**Answer:** Read the traceback bottom-up: your line number, exception type, then check recent **`write`/`create`** calls, **`super()`** order, and whether **access rights** or **constraints** apply. Reproduce with **developer mode** logging or `--log-level=debug` for that addon.

### 20. What is **developer mode** used for (technical menu, field names, view XML IDs)?

**Answer:** **Developer mode** exposes the **Technical** menu, **Edit View** / **View metadata**, **field names** on hover (depending on version), and tools to see **external IDs** and domains — essential for debugging views and security.

## Quick scenarios (short answers)

### 21. A user cannot see a menu entry they expect — what layers of security do you verify?

**Answer:** **Menu** `groups`, **user groups** membership, **model ACL** (read on underlying action’s model), **record rules** hiding records, and **company** context if multi-company. Also check **action/domain** on the menu action.

### 22. You add a field in Python but it does not appear on the form — what are two common causes?

**Answer:** (1) The field is not in the **form view** (add `<field>` or inherit view). (2) **Module not upgraded** or view **inherit** not loaded / wrong `inherit_id`. Bonus: **`groups`** on the field hiding it, or **`invisible`** logic always true.
