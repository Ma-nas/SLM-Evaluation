# TEAM TASK ALLOCATION MATRIX

## Three-Member Workstream Distribution

---

## Agent 1 — Research Scientist & Model Evaluation Specialist

**Primary Responsibility:** Research foundations, literature, model selection, quality evaluation

| Week | Tasks | Deliverables | Dependencies |
|------|-------|--------------|--------------|
| W1 | Literature survey; study SLM landscape; survey benchmarking frameworks; identify research gap | `research/literature_review.md`, `research/research_gap.md` | None |
| W2 | Model selection & license verification; dataset identification; evaluation procedure design | `research/model_selection.md`, `research/dataset_analysis.md` | None |
| W3 | Define quality metrics; design model-quality evaluation procedures | `research/quality_evaluation.md` | Agent 2: runtime interface spec |
| W4 | Support experiment execution; validate quality metrics implementation | Quality metric validation results | Agent 3: benchmark engine |
| W5 | Analyze quality vs performance trade-offs; draft report sections | Report Ch 1–2 drafts | Agent 3: raw results |
| W6 | Finalize references; review report; viva prep (research questions) | `research/references.bib`, report sections | All agents |

**Output Files:**
- `research/literature_review.md`
- `research/research_gap.md`
- `research/model_selection.md`
- `research/dataset_analysis.md`
- `research/quality_evaluation.md`
- `research/references.bib`

---

## Agent 2 — System Architect & Runtime Engineer

**Primary Responsibility:** System design, device profiling, runtime adapters, compatibility

| Week | Tasks | Deliverables | Dependencies |
|------|-------|--------------|--------------|
| W1 | Draft system architecture; identify runtime landscape | `architecture/system_architecture.md` (draft) | None |
| W2 | Device-class specification; runtime compatibility investigation; GGUF/ONNX study | `architecture/device_specification.md`, `research/runtime_comparison.md` | None |
| W3 | Implement device profiler; model registry; runtime adapter interface; first adapter (llama.cpp) | `app/profiler/`, `app/models/`, `app/runtimes/`, `tests/test_runtime.py` | Agent 1: model selection |
| W4 | Additional adapters; error handling; compatibility checks; model loading/unloading | Additional adapters, compatibility matrix | None |
| W5 | Platform limitation documentation; architecture finalization | Final `architecture/system_architecture.md` | None |
| W6 | Integration testing; report sections (architecture, implementation) | Report Ch 3 sections | All agents |

**Output Files:**
- `architecture/system_architecture.md`
- `architecture/device_specification.md`
- `app/profiler/` (device profiler module)
- `app/models/` (model registry)
- `app/runtimes/` (runtime adapters)
- `tests/test_runtime.py`
- `research/runtime_comparison.md`

---

## Agent 3 — Benchmarking & Experimental Analysis Specialist

**Primary Responsibility:** Benchmark engine, experiments, statistics, visualization

| Week | Tasks | Deliverables | Dependencies |
|------|-------|--------------|--------------|
| W1 | Study benchmark methodology; design metric collection approach | Benchmark design notes | None |
| W2 | Design benchmark execution protocol; design prompt workloads | Experiment protocol document | Agent 1: evaluation metrics |
| W3 | Implement benchmark engine; metrics collector; warm-up procedures; SQLite storage | `app/benchmark/`, `app/database/`, `tests/test_benchmark.py` | Agent 2: runtime interface |
| W4 | Execute benchmarks; collect raw data; monitor memory; record metadata | `results/` (raw data) | Agent 2: working adapters |
| W5 | Statistical analysis; visualization generation; reproducibility validation | `analysis/`, comparison graphs | W4 data |
| W6 | Final experiments; report sections (results, analysis); presentation graphs | Report Ch 4–5 sections, presentation materials | All agents |

**Output Files:**
- `app/benchmark/` (benchmark engine)
- `app/evaluation/` (quality evaluation)
- `app/database/` (SQLite storage)
- `analysis/statistical_analysis.py`
- `analysis/visualizations.py`
- `results/` (experiment data)
- `tests/test_benchmark.py`

---

## Shared / Integration Files

| File | Owner | Contributors |
|------|-------|--------------|
| `PROJECT_MASTER_PLAN.md` | Coordinator | All |
| `ARCHITECTURE_DECISIONS.md` | Agent 2 | Agent 1, Agent 3 |
| `PROGRESS_TRACKER.md` | Coordinator | All |
| `EXPERIMENT_TRACKER.md` | Agent 3 | Agent 1 |
| `RESEARCH_RISK_REGISTER.md` | Coordinator | All |
| `app/config/` | Agent 2 | All |
| `app/__init__.py` | Agent 2 | — |
| `requirements.txt` | Coordinator | All |
| `README.md` | Coordinator | All |

---

## Dependency Map

```
Agent 1 (Research) ──────────────────────────────────────┐
  │ model_selection.md ──→ Agent 2 (W3: which models)    │
  │ dataset_analysis.md ──→ Agent 3 (W3: which prompts)  │
  │ quality_evaluation.md ──→ Agent 3 (W3: metrics impl) │
  └──────────────────────────────────────────────────────┘

Agent 2 (Architecture) ─────────────────────────────────┐
  │ runtime interface spec ──→ Agent 3 (W3: adapter API) │
  │ working adapters ──→ Agent 3 (W4: run benchmarks)    │
  │ device profiler ──→ Agent 3 (W4: record hardware)    │
  └──────────────────────────────────────────────────────┘

Agent 3 (Benchmarking) ─────────────────────────────────┐
  │ raw results ──→ Agent 1 (W5: quality analysis)       │
  │ statistical summaries ──→ All (W6: report/viva)      │
  └──────────────────────────────────────────────────────┘
```

---

## Critical Path

```
Lit Review (W1) → Model Selection (W2) → Runtime Adapters (W3) → Benchmark Execution (W4) → Analysis (W5) → Report (W6)
```

The critical path runs through the full 6-week period. Any delay in model selection (W2) or runtime adapter implementation (W3) directly delays experiments.

---

*Last Updated: 2026-11-21*
