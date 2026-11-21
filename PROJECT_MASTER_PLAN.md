# PROJECT MASTER PLAN

## Landscape Lock-In, Device-Class Specification, and Cross-Platform Evaluation Harness for Small Language Models (SLMs)

**Domain:** AI/ML · NLP · Edge AI · Model Deployment · Systems Benchmarking
**Team Size:** 3 members
**Duration:** 6 weeks
**University:** JAIN (Deemed-to-be University) — School of Computer Science & Engineering (CSE-AIML)
**Degree:** B.Tech in Computer Science & Engineering — AIML

---

## A. Document Inventory

| # | Document | Status | Notes |
|---|----------|--------|-------|
| 1 | `Report_Template[1].docx` | ✅ Inspected | University-prescribed report format. Contains structure from a previous project ("FIREGUIDE"). We extract the **format only**: title page, certificate, declaration, acknowledgement, nomenclature, list of figures, abstract, Ch 1–3 structure, references, plagiarism report page. |
| 2 | Project title | ✅ Provided | "Landscape Lock-In, Device-Class Specification, and Cross-Platform Evaluation Harness for Small Language Models (SLMs)" |
| 3 | Student names / registration numbers | ❌ NOT PROVIDED | Must be supplied by user before final report generation |
| 4 | Supervisor name | ❌ NOT PROVIDED | Template shows Dr. K.S. Arvind — user must confirm |
| 5 | Evaluation rubric | ❌ NOT PROVIDED | Will design defensible deliverables regardless |

---

## B. Hardware Environment Profile

| Component | Specification |
|-----------|---------------|
| **CPU** | 12th Gen Intel Core i5-12450H (8 cores, 12 threads, 2.0 GHz base) |
| **Architecture** | x86_64 (Alder Lake — hybrid P-core/E-core) |
| **RAM** | 16 GB DDR4/DDR5 |
| **GPU** | NVIDIA GeForce RTX 3050 Laptop GPU |
| **VRAM** | 4 GB GDDR6 |
| **CUDA Compute** | 8.6 (Ampere) |
| **Driver** | 617.42 |
| **CUDA UMD** | 13.4 |
| **OS** | Windows 11 Home (Build 26300) |
| **Python** | 3.14.3 |

**Hardware Constraints:**
- 4 GB VRAM severely limits model sizes — most >3B parameter models in FP16 won't fit
- Q4 quantized models up to ~3B–4B parameters are feasible on GPU
- CPU inference has no VRAM constraint but is significantly slower
- Hybrid architecture (P-core/E-core) may affect CPU benchmark consistency

---

## C. Installed Dependencies

| Package | Version | Status |
|---------|---------|--------|
| fastapi | 0.141.1 | ✅ Installed |
| matplotlib | 3.10.8 | ✅ Installed |
| numpy | 2.4.3 | ✅ Installed |
| pandas | 3.0.1 | ✅ Installed |
| pytest | 9.0.2 | ✅ Installed |
| streamlit | 1.65.0 | ✅ Installed |
| torch | — | ❌ Not installed |
| transformers | — | ❌ Not installed |
| llama-cpp-python | — | ❌ Not installed |
| onnxruntime | — | ❌ Not installed |
| psutil | — | ❌ Not installed |
| plotly | — | ❌ Not installed |

---

## D. University Report Format (Extracted from Template)

The prescribed structure is:

1. **Title Page** — University header, project title, student names, guide name, year
2. **Certificate** — Bonafide certificate signed by guide and examiners
3. **Declaration** — Student declaration of original work
4. **Acknowledgement** — Standard acknowledgement format
5. **Table of Contents**
6. **Nomenclature / Abbreviations**
7. **List of Figures**
8. **Abstract** — ~1 page project summary
9. **Chapter 1: Introduction** — 1.1 Introduction, 1.2 Objectives, 1.3 Background & Motivation, 1.4 Benefits
10. **Chapter 2: Literature Survey** — Table format with columns for reference details and summary
11. **Chapter 3 (Problem Formulation):** Problem Statement, System Architecture, Proposed Algorithms, Proposed Work (phased), Hardware/Software Design
12. **Chapter 4 (System Design):** Use Case Diagram, System Architecture Diagram, Activity Diagram
13. **References** — Numbered list format
14. **Plagiarism Report** — Attached separately

> **NOTE:** The template appears to cover up to Chapter 3 (System Design). We will follow this structure and extend with Results, Analysis, Conclusion chapters as standard practice, unless the user provides additional template pages.

---

## E. Research Problem Formulation

### Research Questions

| ID | Research Question |
|----|-------------------|
| **RQ1** | How does SLM performance vary across different device classes (CPU-only vs GPU-assisted inference on consumer hardware)? |
| **RQ2** | How do inference runtimes (llama.cpp, ONNX Runtime, Transformers/PyTorch) affect model performance, compatibility, and portability? |
| **RQ3** | What trade-offs exist between quantization level (FP16, Q8, Q5, Q4), model quality, inference speed, and resource consumption? |
| **RQ4** | How can a standardized evaluation harness improve benchmark reproducibility across heterogeneous hardware? |

### Hypotheses (Testable)

| ID | Hypothesis |
|----|------------|
| **H1** | GPU-accelerated inference on the RTX 3050 will achieve ≥2× token throughput compared to CPU-only inference for Q4-quantized SLMs ≤3B parameters. |
| **H2** | llama.cpp with GGUF models will demonstrate lower memory overhead and higher throughput than PyTorch/Transformers for the same model at comparable quantization levels. |
| **H3** | Aggressive quantization (Q4) will reduce model quality by ≤10% on standard NLP benchmarks compared to FP16, while reducing memory consumption by ≥60%. |
| **H4** | A standardized evaluation harness with fixed prompts, warm-up procedures, and controlled generation parameters will produce benchmark results with coefficient of variation <15% across repeated runs. |

### Proposed Research Contribution

1. **Landscape Lock-In Taxonomy:** A systematic compatibility matrix mapping Model × Format × Runtime × Device-Class combinations, documenting which paths are supported, tested, and blocked.
2. **Device-Class Specification Schema:** A formal, extensible schema for describing inference hardware capabilities relevant to SLM deployment.
3. **Cross-Platform Evaluation Harness:** An open, modular Python framework that standardizes SLM benchmarking across runtimes and hardware, with reproducible measurement protocols.
4. **Empirical Evidence:** Actual benchmark data comparing SLMs across runtimes and device configurations on real consumer hardware.

---

## F. Six-Week Execution Schedule

### Week 1: Research Foundation (Days 1–7)
- [ ] Literature review on SLM benchmarking, edge inference, model compression
- [ ] Survey existing benchmarking frameworks (lm-evaluation-harness, llm-benchmark, etc.)
- [ ] Identify research gap
- [ ] Formalize research questions and hypotheses
- [ ] Define evaluation metrics
- [ ] Begin model candidate identification

### Week 2: Experimental Design (Days 8–14)
- [ ] Finalize model selection with compatibility verification
- [ ] Design device-class specification schema
- [ ] Investigate runtime compatibility (llama.cpp, ONNX, Transformers)
- [ ] Design experimental protocol (prompts, parameters, warm-up, repetitions)
- [ ] Select evaluation datasets
- [ ] Install and validate required dependencies
- [ ] Document landscape lock-in findings

### Week 3: Framework Architecture & Core Implementation (Days 15–21)
- [ ] Implement device profiler module
- [ ] Implement model registry
- [ ] Design and implement runtime adapter interface
- [ ] Implement llama.cpp runtime adapter
- [ ] Implement ONNX Runtime adapter (if compatible)
- [ ] Implement Transformers/PyTorch adapter
- [ ] Write unit tests for core modules
- [ ] Implement configuration management

### Week 4: Benchmark Engine & Experiments (Days 22–28)
- [ ] Implement benchmark execution engine
- [ ] Implement metrics collection (TTFT, TPS, latency, memory)
- [ ] Implement warm-up procedures
- [ ] Implement results storage (SQLite)
- [ ] Download selected models
- [ ] Execute first benchmark runs
- [ ] Collect raw experimental data
- [ ] Debug and fix measurement issues

### Week 5: Quality Evaluation & Analysis (Days 29–35)
- [ ] Implement task-quality evaluation metrics
- [ ] Execute complete benchmark suite
- [ ] Perform statistical analysis
- [ ] Generate visualizations
- [ ] Analyze quantization trade-offs
- [ ] Analyze CPU vs GPU performance
- [ ] Analyze runtime comparison
- [ ] Draft research report

### Week 6: Documentation & Validation (Days 36–42)
- [ ] Complete research report in university format
- [ ] Final integration testing
- [ ] Validate reproducibility
- [ ] Prepare presentation
- [ ] Prepare viva Q&A (40+ questions)
- [ ] Final review and quality gates
- [ ] Package deliverables

---

## G. Quality Gates

| Gate | Criteria | Status |
|------|----------|--------|
| **G1 — Research** | RQs, lit survey, gap, methodology documented | ⬜ Pending |
| **G2 — Architecture** | Device spec, runtime interface, modular design documented | ⬜ Pending |
| **G3 — Implementation** | Core framework executes real models, records valid measurements | ⬜ Pending |
| **G4 — Experiments** | Actual benchmark runs performed, raw data available | ⬜ Pending |
| **G5 — Analysis** | Results statistically summarized and interpreted | ⬜ Pending |
| **G6 — Documentation** | University format followed, citations verified | ⬜ Pending |
| **G7 — Validation** | Tests pass, limitations disclosed, presentation ready | ⬜ Pending |

---

## H. Risk Register Summary

See `RESEARCH_RISK_REGISTER.md` for full details.

**Top 5 Risks:**
1. **VRAM Limitation (4GB)** — Severely constrains model sizes; mitigated by targeting Q4-quantized ≤3B models
2. **Runtime Compatibility** — ONNX Runtime GenAI may not support all target models on Windows; mitigated by treating as optional
3. **Python 3.14 Compatibility** — Very new Python version; some ML packages may lack wheels; mitigated by fallback to CPU-only or building from source
4. **Measurement Noise** — Laptop thermal throttling and background processes affect benchmarks; mitigated by warm-up runs and repeated measurements
5. **Model Download Time/Size** — Large model files require significant bandwidth; mitigated by selecting small, quantized variants

---

*Last Updated: 2026-11-21*
*Status: INITIALIZED — Week 1 begins*
