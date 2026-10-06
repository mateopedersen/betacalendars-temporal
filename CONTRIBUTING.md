# Contributing

Bug reports and focused changes are welcome. Please include a short example that reproduces the issue and the Python version used.

For local development, install the project with `python -m pip install -e '.[dev]'`, then run `pytest`, `ruff check .`, `ruff format --check .`, and `mypy src`.

Keep calendar calculations deterministic, bounded, offline, and based on Python's standard date types. Do not add a holiday database or network behavior without a separate design discussion.
