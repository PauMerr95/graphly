---
name: config-schema
description: Conventions for Pydantic config models in src/config/parser.py — TOML section aliases, populate_by_name, and how to add a new config section
---
# Config schema conventions

- `src/config/parser.py` defines `Config` and its nested models (`GeneralConfig`, `IRDataConfig`, `MSDataConfig`) using Pydantic.
- Each top-level section is keyed by its TOML table name via a Python-mismatched `alias` (e.g. `general` ↔ `"general.config"`, `ir_data` ↔ `"IR.data.config"`).
- All config models set `ConfigDict(populate_by_name=True)` so fields work by either the TOML alias or the Python attribute name — keep this on any new model.
- `test/test_data/graphly.config.toml` is the canonical example of valid shape; update it whenever the schema changes so it stays in sync.
- When adding a new data-source section (mirroring `IRDataConfig`/`MSDataConfig`), follow the same pattern: optional `override_height`/`override_width`, a `y_axis` field aliased from `y-axis`, and register it as a new top-level field on `Config` with its own TOML alias.
