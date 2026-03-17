# AAE-ENGINE Baseline Checkpoint

## Branch: `runtime-unification`

This document captures the baseline state before architectural restructuring to prevent silent regression.

---

## Test Results

**Command:** `pytest -q`

### Summary
- **Status:** FAILED (Collection Errors)
- **Errors:** 24 collection errors
- **Warnings:** 18 pytest warnings

### Error Details

All test collections failed due to **Python version incompatibility**:

```
TypeError: Unable to evaluate type annotation 'datetime | None'. 
If you are making use of the new typing syntax (unions using `|` since Python 3.10 
or builtins subscripting since Python 3.9), you should either replace the use of 
new syntax with the existing `typing` constructs or install the `eval_type_backport` package.
```

**Root Cause:** The codebase uses Python 3.10+ union syntax (`datetime | None`) but the runtime is Python 3.9.6.

**Affected Test Files (24):**
- `tests/integration/test_graph_runtime_integration.py`
- `tests/integration/test_workflows.py`
- `tests/patching/test_diff_constructor.py`
- `tests/test_deep_integration.py`
- `tests/unit/test_action_graph.py`
- `tests/unit/test_adapters.py`
- `tests/unit/test_agent_roles.py`
- `tests/unit/test_artifact_store.py`
- `tests/unit/test_behavior_localization.py`
- `tests/unit/test_dashboard_api.py`
- `tests/unit/test_events.py`
- `tests/unit/test_experiment_evaluator.py`
- `tests/unit/test_graph_pipeline.py`
- `tests/unit/test_knowledge_graph.py`
- `tests/unit/test_launcher.py`
- `tests/unit/test_learning_memory_sandbox.py`
- `tests/unit/test_patching_evaluation.py`
- `tests/unit/test_planner_modules.py`
- `tests/unit/test_registry_memory.py`
- `tests/unit/test_repo_model.py`
- `tests/unit/test_retry_policy.py`
- `tests/unit/test_swarm_planner.py`
- `tests/unit/test_swe_preparation.py`
- `tests/unit/test_task_graph.py`

---

## Python Version

**Version:** Python 3.9.6

---

## Key Dependencies

From `requirements.txt`:

| Category | Package | Version |
|----------|---------|---------|
| Core | fastapi | >=0.115 |
| Core | uvicorn | >=0.30 |
| Core | httpx | >=0.27 |
| Core | pydantic | >=2.0 |
| Core | PyYAML | >=6.0 |
| Database | psycopg | >=3.1 |
| Database | redis | >=5.0 |
| Graph/Vector | neo4j | >=5.0 |
| Graph/Vector | qdrant-client | >=1.7 |
| Graph/Vector | networkx | >=3.0 |
| ML/Embeddings | numpy | >=1.26 |
| ML/Embeddings | scikit-learn | >=1.4 |
| ML/Embeddings | sentence-transformers | >=2.6 |
| Code Parsing | tree-sitter | >=0.21 |
| Code Parsing | tree-sitter-python | >=0.21 |
| Security | bandit | >=1.7 |
| Security | safety | >=3.0 |
| Monitoring | prometheus-client | >=0.20 |
| Monitoring | opentelemetry-api | >=1.23 |
| Process | docker | >=7.0 |
| Process | psutil | >=5.9 |
| Utilities | tenacity | >=8.2 |
| Utilities | rich | >=13.0 |
| Utilities | typer | >=0.12 |
| Utilities | structlog | >=24.0 |

---

## Pre-Restructuring Notes

### Critical Issue
The test suite is **non-functional** due to Python version mismatch. Before proceeding with architectural changes:

1. **Either:** Upgrade Python to 3.10+ to support modern union syntax
2. **Or:** Backport all type annotations to use `Optional[]` and `Union[]` from `typing` module

### Recommendation
This baseline confirms that the primary regression risk is **not** from the planned structural changes, but from the existing Python version incompatibility. The `runtime-unification` branch should address this dependency issue first.

---

*Generated: 2026-03-17*
*Branch: runtime-unification*
