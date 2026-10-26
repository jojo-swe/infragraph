# AGENTS.md

## Layout

- `src/infragraph/core.py`: the graph, `blast_radius`, `single_points_of_failure`, `dependency_chain`, `to_mermaid`.
- `src/infragraph/cli.py`: argparse front end and exit codes.
- `tests/test_core.py`: graph analysis tests. `tests/test_cli.py`: CLI tests that call `main([...])`.
- `examples/campus.json`: the canonical fixture. README output must match it.

## Setup, test, lint

```bash
pip install -e ".[dev]"   # required; tests import the installed package
pytest
ruff check .
```

CI runs exactly these commands on Python 3.11, 3.12 and 3.13.

## Conventions

- Model types are frozen dataclasses with `slots=True`.
- Every public method sorts its output so results are deterministic.
- CLI errors go to stderr prefixed `infragraph:` and exit `2`.
- New CLI behaviour gets a test in `tests/`.
- README example blocks are copied from real command output; `tests/test_cli.py` checks the impact example.

## Edge direction

`source` depends on `target`. `_dependents` is the reverse index (target -> sources) used by blast
radius and only holds required edges. `_requirements` is the forward index (source -> targets) used
by `chain` and holds every edge, including optional ones.
