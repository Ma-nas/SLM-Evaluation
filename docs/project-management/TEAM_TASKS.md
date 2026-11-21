# TEAM TASKS

## Three-Member Task Allocation and Status Tracker

**Last Updated:** 2026-11-21

---

## Member 1 — Research Scientist & Model Evaluation Specialist

**Focus:** Research, literature review, SLM selection, quality evaluation

| # | Task | Week | Status | Deliverable | Dependencies |
|---|------|------|--------|-------------|--------------|
| 1.1 | Literature survey on SLMs, quantization, edge inference | W1 | 🔄 In Progress | `docs/research/literature_review.md` | None |
| 1.2 | Survey existing benchmarking frameworks | W1 | ⬜ Pending | Part of literature review | None |
| 1.3 | Identify and document research gap | W1 | ⬜ Pending | `docs/research/research_gap.md` | 1.1 |
| 1.4 | Preliminary model selection & license check | W2 | ⬜ Pending | `docs/research/model_selection.md` | 1.1 |
| 1.5 | Dataset identification for quality evaluation | W2 | ⬜ Pending | `docs/research/dataset_analysis.md` | 1.4 |
| 1.6 | Design quality evaluation procedures | W3 | ⬜ Pending | `docs/research/quality_evaluation.md` | 1.5 |
| 1.7 | Implement quality metrics module | W3–4 | ⬜ Pending | `src/evaluation/` | 2.6 (runtime interface) |
| 1.8 | Analyze quality vs. performance trade-offs | W5 | ⬜ Pending | Analysis document | 3.5 (raw results) |
| 1.9 | Draft report: Introduction, Literature Survey, Methodology | W5 | ⬜ Pending | `docs/report/` sections | 1.1–1.6 |
| 1.10 | Compile verified references (BibTeX) | W5–6 | ⬜ Pending | `docs/research/references.bib` | 1.1 |
| 1.11 | Viva preparation: research questions | W6 | ⬜ Pending | `presentation/viva_qa.md` | All |

---

## Member 2 — System Architect & Runtime Engineer

**Focus:** Device profiling, runtime integration, compatibility, resource monitoring

| # | Task | Week | Status | Deliverable | Dependencies |
|---|------|------|--------|-------------|--------------|
| 2.1 | Draft system architecture document | W1 | 🔄 In Progress | `docs/architecture/system_architecture.md` | None |
| 2.2 | Runtime landscape investigation | W1–2 | ⬜ Pending | `docs/architecture/runtime_comparison.md` | None |
| 2.3 | Design device-class specification schema | W2 | ⬜ Pending | `docs/architecture/device_specification.md` | None |
| 2.4 | Implement device profiler module | W3 | ⬜ Pending | `src/devices/` | None |
| 2.5 | Implement model registry | W3 | ⬜ Pending | `src/models/` | 1.4 (selected models) |
| 2.6 | Design & implement runtime adapter interface | W3 | ⬜ Pending | `src/runtimes/base.py` | 2.1 |
| 2.7 | Implement llama.cpp runtime adapter | W3 | ⬜ Pending | `src/runtimes/llamacpp_adapter.py` | 2.6 |
| 2.8 | Implement Transformers runtime adapter | W3–4 | ⬜ Pending | `src/runtimes/transformers_adapter.py` | 2.6 |
| 2.9 | Investigate ONNX Runtime compatibility | W2–4 | ⬜ Pending | Compatibility report | None |
| 2.10 | Implement resource monitoring | W3 | ⬜ Pending | `src/monitoring/` | None |
| 2.11 | Landscape lock-in compatibility matrix | W4 | ⬜ Pending | `docs/research/compatibility_matrix.md` | 2.7, 2.8 |
| 2.12 | Write runtime unit tests | W3–4 | ⬜ Pending | `tests/test_runtimes.py` | 2.7, 2.8 |
| 2.13 | Report sections: Architecture, Implementation | W5–6 | ⬜ Pending | `docs/report/` sections | 2.1–2.11 |

---

## Member 3 — Benchmarking & Experimental Analysis Specialist

**Focus:** Benchmark execution, data collection, analysis, visualization, reporting

| # | Task | Week | Status | Deliverable | Dependencies |
|---|------|------|--------|-------------|--------------|
| 3.1 | Design benchmark methodology | W1–2 | 🔄 In Progress | `docs/experimental-design/benchmark_methodology.md` | None |
| 3.2 | Design standardized prompt workloads | W2 | ⬜ Pending | `configs/prompts.yaml` | None |
| 3.3 | Design SQLite database schema | W2–3 | ⬜ Pending | `src/benchmarks/schema.sql` | None |
| 3.4 | Implement benchmark execution engine | W3 | ⬜ Pending | `src/benchmarks/` | 2.6 (runtime interface) |
| 3.5 | Implement metrics collector | W3 | ⬜ Pending | `src/monitoring/metrics.py` | 2.10 |
| 3.6 | Implement results database manager | W3 | ⬜ Pending | `src/benchmarks/database.py` | 3.3 |
| 3.7 | Execute benchmark experiments | W4 | ⬜ Pending | `results/raw/` | 2.7, 2.8, 3.4 |
| 3.8 | Implement statistical analysis | W4–5 | ⬜ Pending | `scripts/analyze_results.py` | 3.7 |
| 3.9 | Generate comparison visualizations | W5 | ⬜ Pending | `results/figures/` | 3.8 |
| 3.10 | Validate reproducibility | W5 | ⬜ Pending | Reproducibility report | 3.7 |
| 3.11 | Write benchmark unit tests | W3–4 | ⬜ Pending | `tests/test_benchmarks.py` | 3.4, 3.6 |
| 3.12 | Report sections: Results, Analysis | W5–6 | ⬜ Pending | `docs/report/` sections | 3.7–3.9 |
| 3.13 | Presentation materials | W6 | ⬜ Pending | `presentation/` | All |

---

## Cross-Team Dependencies

```
Member 1 ──(1.4 model_selection)──→ Member 2 (2.5 model registry)
Member 2 ──(2.6 runtime interface)──→ Member 1 (1.7 quality metrics)
Member 2 ──(2.6 runtime interface)──→ Member 3 (3.4 benchmark engine)
Member 2 ──(2.7, 2.8 adapters)──→ Member 3 (3.7 experiments)
Member 3 ──(3.7 raw results)──→ Member 1 (1.8 quality analysis)
```

## Shared Interface Contracts

| Interface | Defined By | Used By | Specification |
|-----------|-----------|---------|---------------|
| `RuntimeAdapter` ABC | Member 2 | Member 3 | `src/runtimes/base.py` |
| `DeviceProfile` schema | Member 2 | Member 3 | `src/devices/schema.py` |
| `ModelConfig` dataclass | Member 2 | Member 1, 3 | `src/models/registry.py` |
| `BenchmarkResult` schema | Member 3 | Member 1 | `src/benchmarks/schema.sql` |
| Prompt format | Member 3 | All | `configs/prompts.yaml` |

---

## Current Blockers

| Blocker | Affects | Resolution |
|---------|---------|------------|
| Python 3.14 compatibility for torch/llama-cpp-python | Member 2 (W3) | Test pip install in W2 |
| Student names needed for report | All (W6) | User to provide |

---

*Next update: After Week 1 deliverables complete*
