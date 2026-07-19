# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Graphly is an early-stage CLI tool ("turning data into nice graphs with minimal configuration") for building IR/MS (infrared/mass spectrometry) data graphs from a TOML config file. The project is in its initial scaffolding stage — most functionality does not exist yet.

## Environment and commands

- Python >= 3.13 (see `.python-version`), managed via `uv` (`uv.lock` is present).
- Package uses a `src/` layout (`src/config/...`) installed in editable mode; import the package as `config`, not `src.config`.
- Run tests: `pytest` (or `pytest --cov=src` to match the pre-commit hook).
- Run a single test: `pytest test/config_test/test_parser.py::TestBuildParser::test_filename_only`
- Type check: `mypy` (config lives in `[tool.mypy]` in `pyproject.toml`; `mypy_path = "src"`).
- Lint/format: `ruff check --fix` and `ruff format` (run via pre-commit, using ruff's default rule set — no custom `ruff.toml`/`[tool.ruff]` config exists).
- Pre-commit hooks (`.pre-commit-config.yaml`) run end-of-file-fixer, trailing-whitespace, check-yaml, check-added-large-files, ruff-check, ruff-format, mypy, and pytest --cov=src on every commit.
- Dev tools (pytest, mypy, ruff) are not declared as dependencies in `pyproject.toml`/`uv.lock` — they're expected to be available in the environment (e.g. installed manually or via pre-commit's isolated envs) rather than pulled in via a dependency group.

## Architecture

- `main.py` — placeholder CLI entry point (currently just prints a greeting; not yet wired to `src/config`).
- `src/config/parser.py` — the only real module so far. It has two responsibilities that will likely split apart as the project grows:
  - `parse_args()`: argparse-based CLI parsing (`graphly <filename> [-c/--config <path>]`).
  - `import_config_toml(path)`: loads a `.toml` config file (via `tomllib`) into a Pydantic `Config` model.
- Config schema (Pydantic models in `parser.py`) mirrors `test/test_data/graphly.config.toml`'s structure and uses field aliases to map TOML section names to Python attributes:
  - `Config` has three top-level sections, each keyed by a TOML table alias: `general` (alias `"general.config"`), `ir_data` (alias `"IR.data.config"`), `ms_data` (alias `"MS.data.config"`).
  - All config models use `ConfigDict(populate_by_name=True)`, so fields can be set either by their TOML alias or their Python name.
  - `GeneralConfig` holds global plot dimensions (`width`, `height`) and a `theme` (`"Default"` or `"Seaborn"`).
  - `IRDataConfig`/`MSDataConfig` hold per-dataset overrides (`override_height`/`override_width`, both optional) plus `y_axis` (`"hidden"`/`"visible"`, aliased from `y-axis`) and `spectra_spread`.
- `test/test_data/graphly.config.toml` is a sample/working config file matching this schema — use it as the reference for valid TOML shape when changing the models.
- Tests live under `test/<module>_test/` mirroring `src/` (e.g. `test/config_test/test_parser.py` tests `src/config/parser.py`), and import from the installed `config` package rather than relative paths into `src/`.
