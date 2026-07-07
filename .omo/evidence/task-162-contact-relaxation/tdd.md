# Task 162 TDD Evidence

## RED

Focused local RED command:

```text
uv run pytest tests/test_geometry.py::test_relax_contact_constrained_node_when_contact_crosses_direct_path -q
```

Observed failure before implementation:

```text
ImportError: cannot import name 'relax_contact_constrained_node'
```

This was the intended failure: the test named a new generalized geometry helper
that did not exist yet.

## GREEN

Focused local GREEN:

```text
uv run pytest tests/test_geometry.py::test_relax_contact_constrained_node_when_contact_crosses_direct_path -q
.                                                                        [100%]
1 passed in 0.01s
```

Local geometry suite:

```text
uv run pytest tests/test_geometry.py -q
.............                                                            [100%]
13 passed in 0.02s
```

Static checks:

```text
uv run ruff check src/pyz1/contact_relaxation.py src/pyz1/geometry.py tests/test_geometry.py
All checks passed!

uv run basedpyright src/pyz1/contact_relaxation.py src/pyz1/geometry.py tests/test_geometry.py
0 errors, 0 warnings, 0 notes
```
