.PHONY: ruff
ruff:
	uv run ruff check --fix --select I . && uv run ruff format .