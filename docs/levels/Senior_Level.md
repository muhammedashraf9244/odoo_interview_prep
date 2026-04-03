# Senior level — questions & answers

> Extends roadmap Q20–Q27.

## ORM & PostgreSQL

### 1. How does the ORM **cache** work at a high level? When must you **`flush`** / **`invalidate`**?

**Answer:** The ORM keeps an **in-memory cache** of field values per record per transaction. **`flush()`** (e.g. `flush_model`, `flush_recordset`) pushes pending writes to PostgreSQL — needed before **raw SQL** that must see ORM changes. **`invalidate_*`** clears cache after **raw SQL writes** or external changes so the next read hits the DB. Missing flush/invalidate causes **stale reads** or inconsistent SQL.

### 2. Describe a safe pattern for mixing **raw SQL** with ORM in the same transaction.

**Answer:** `records.flush_recordset()` → `env.cr.execute(..., params)` with **parameterized** queries → `records.invalidate_recordset()` (or `env.invalidate_all()` if broader). Never interpolate user input into SQL strings. Prefer ORM when possible.

### 3. How do you find **slow queries** in production (Odoo flags, Postgres tooling)?

**Answer:** Odoo: **`--log-sql`**, targeted **`--log-handler`**, slow query logging if enabled. PostgreSQL: **`pg_stat_statements`**, **`EXPLAIN ANALYZE`**, monitoring on **lock waits** and **seq scans**. Correlate with **worker timeouts** and **cron** windows.

### 4. When do you add **`index=True`** vs a custom **SQL index** in `init()`?

**Answer:** **`index=True`** on a field — simple btree on the column; good for **foreign keys** and filtered fields. Use **`init()`** / **`_auto_init`** for **composite**, **partial**, **GIN/GiST** (e.g. JSON, full text, trigram), or **expression** indexes — things the ORM field API does not express.

### 5. Explain **`auto_join`** on relational fields — benefits and risks.

**Answer:** **`auto_join=True`** on Many2one can let the ORM **JOIN** instead of separate queries when the field appears in domains — fewer queries. **Risk:** complex joins, **cartesian products** if misused, harder **query plans**; use only when profiled and domains are selective.

### 6. How does **`read_group()`** differ from `search_read()` for dashboards and pivot-style data?

**Answer:** **`read_group(domain, fields, groupby, ...)`** returns **aggregated** rows (counts, sums with `__count`, aggregated fields) — what **pivot/graph** views use. **`search_read`** returns **flat rows** per record. Use `read_group` for **KPIs** and grouped metrics without pulling every record client-side.

## Multi-company & multi-warehouse

### 7. What does **`_check_company_auto`** do? Give an example failure it prevents.

**Answer:** When `True`, the ORM checks that **Many2one** records linked on the model share a **consistent `company_id`** with the main record (e.g. order lines’ products/warehouses match order company). Prevents **cross-company** documents that break accounting and inventory.

### 8. How do **`company_id`**, **`company_ids`** (user), and **`with_company()`** interact in custom code?

**Answer:** Records carry **`company_id`** (or related). Users have **`company_ids`** (allowed companies); **`env.company`** is the current one from context. **`with_company(company)`** runs code **as if** that company is active (defaults, fiscal rules). Wrong mix causes **invisible records** or **rule** surprises — always set company on create explicitly when multi-company.

### 9. A stock move is validated in the wrong company — what categories of bug do you investigate?

**Answer:** **Context** (`allowed_company_ids`, `with_company`), **default `company_id`** on picking/move, **location** company vs **warehouse** company, **user switching companies** mid-flow, **sudo** without company check, and **record rules** that are too permissive.

## Concurrency & reliability

### 10. How does Odoo handle **concurrent writes** to the same record?

**Answer:** Typically **last write wins** at field level within a transaction; **SerializationFailure** / concurrent update errors can occur with heavy contention. Some flows use **optimistic** checks (`write_date`). Critical sections may need **SQL `SELECT FOR UPDATE`**, **queue jobs**, or **business locking** (state machine) to serialize.

### 11. When would you use **`FOR UPDATE`** (raw SQL) or a **queue job** instead of inline logic?

**Answer:** **`FOR UPDATE`** — short **pessimistic lock** when you must read-then-update atomically (stock reservation, sequence-like counters). **Queue job** — long or **retryable** work, **rate-limited** external API calls, or to **avoid blocking** the HTTP worker — process asynchronously with failure handling.

### 12. What are **savepoints** (`cr.savepoint()`) used for in custom business logic?

**Answer:** **Nested transactions** inside a request: rollback **part** of the work without aborting the whole request. Use for **try/except** around optional sub-steps (e.g. post message fails but main write must commit). Avoid deep nesting; understand **performance** cost.

## Scalability & operations

### 13. How do you size **workers** and memory limits for a multi-worker deployment?

**Answer:** Rule of thumb **~2×CPU + 1** workers (tune to RAM). Set **`limit_memory_soft/hard`** per worker so one bad request cannot kill the node. Separate **cron** / **longpolling** if needed. Monitor **RSS** and **GC** under load.

### 14. What is the role of **longpolling** / bus in deployment topology?

**Answer:** **Bus/longpolling** delivers **notifications** (discuss, live updates) without each worker holding open chatty HTTP. Often a **dedicated** port/process or **gevent** worker so **main workers** are not starved. Reverse proxy must support **long-lived** connections.

### 15. How would you approach **read replicas** for reporting without breaking ORM assumptions?

**Answer:** Replicas have **replication lag** — reporting reads can be **stale**. Route **read-only** cursors only for **known-safe** queries (BI, SQL reports), not for **interactive** ORM flows that immediately write. Odoo does not fully abstract replica routing — often **external** reporting DB or **scheduled** exports.

## Code quality & upgrades

### 16. What strategies reduce **merge pain** when upgrading Odoo major versions?

**Answer:** Minimize **core overrides**; prefer **`_inherit`** and **hooks**; pin **test coverage**; maintain **upgrade scripts** (`migrations/`); read **release notes** and **deprecated** warnings; use **CI** against target version; avoid **private API** (`_` methods) when public hooks exist.

### 17. How do you document **hooks** (`_prepare_*`) so other modules can extend safely?

**Answer:** Document **input/output** dicts, **keys** added, **stability** (which keys are stable across versions), and **call order** with `super()`. Prefer returning **immutable copies** or clear **mutation** contract. Add **tests** for hook extension points.

### 18. When is **OCA `queue_job`** (or similar) preferable to a synchronous `button_*` method?

**Answer:** When work exceeds **HTTP timeout**, needs **retries**, **throttling** to external APIs, or **background** processing so the user gets immediate **feedback** (job id, bus notification). Not for **must-be-atomic** user actions that need instant confirmation without another state.

## Frontend (v17+)

### 19. At a high level, how do **OWL** components relate to the legacy widget registry?

**Answer:** **OWL** is the **component** framework for the web client (form statusbar, many2many widgets, etc.). **Registry** categories (`fields`, `main_components`, …) register **JS modules** that replace or extend UI. Legacy **widgets** are largely superseded by **OWL field components** in modern Odoo.

### 20. When would you add a **custom field widget** vs a **related field** + attrs?

**Answer:** **Custom widget** when you need **rich UI** (charts, maps, complex editing) beyond standard fields. **Related/stored related** + attrs when **data model** is enough and you only need show/hide/format — simpler to maintain and better for **search/export**.
