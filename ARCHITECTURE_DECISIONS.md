# ARCHITECTURE DECISIONS LOG

## ADR-001: Primary Inference Runtime Selection

**Status:** Proposed
**Date:** 2026-11-21

**Context:** We need at least two inference runtimes to compare. The hardware has 4GB VRAM and runs Windows 11.

**Decision:** Use llama.cpp (via llama-cpp-python) as the primary runtime and PyTorch/Transformers as the secondary. ONNX Runtime GenAI as optional tertiary if compatible.

**Rationale:**
- llama.cpp has the best VRAM efficiency via GGUF quantized formats
- PyTorch/Transformers is the standard research baseline
- ONNX Runtime adds diversity but compatibility is uncertain
- Both llama.cpp and Transformers have Windows CUDA support

**Consequences:**
- Must verify llama-cpp-python builds with CUDA on Python 3.14
- Must verify PyTorch has 3.14 wheels
- ONNX results may be absent from final report

---

## ADR-002: Model Format Strategy

**Status:** Proposed
**Date:** 2026-11-21

**Context:** Different runtimes require different model formats. We need to manage this systematically.

**Decision:**
- GGUF format for llama.cpp (primary)
- SafeTensors/PyTorch format for Transformers
- ONNX format only if ORT GenAI is viable

**Rationale:**
- GGUF is the most VRAM-efficient format for 4GB constraint
- SafeTensors is the HuggingFace standard
- Format conversion adds complexity — prefer pre-converted models

---

## ADR-003: Database Choice

**Status:** Decided
**Date:** 2026-11-21

**Decision:** SQLite for all results storage.

**Rationale:**
- Zero configuration
- Python stdlib support (sqlite3)
- Single file, portable
- Sufficient for expected data volume (~thousands of rows)
- No server process needed

---

## ADR-004: Quantization Levels to Test

**Status:** Proposed
**Date:** 2026-11-21

**Decision:** Test Q4_K_M and Q8_0 GGUF quantizations, plus FP16 where VRAM allows.

**Rationale:**
- Q4_K_M is the most common "good quality" 4-bit quantization
- Q8_0 provides a quality reference with moderate compression
- FP16 is the uncompressed baseline (may only work on CPU or for very small models)
- More quantization levels add testing time without proportional insight

---

## ADR-005: UI Framework

**Status:** Proposed
**Date:** 2026-11-21

**Decision:** Use Streamlit for the results dashboard. No FastAPI backend unless a REST interface is independently justified.

**Rationale:**
- Streamlit is already installed
- Rapid prototyping for visualization
- FastAPI adds unnecessary complexity for a benchmarking tool
- The primary interface is CLI-based benchmark execution

---

## ADR-006: Measurement Methodology

**Status:** Proposed
**Date:** 2026-11-21

**Decision:**
- Minimum 5 repeated runs per configuration
- 2 warm-up runs (discarded) before measurement runs
- Use `time.perf_counter_ns()` for timing
- Use `psutil` for RAM monitoring
- Use `pynvml` or `nvidia-smi` for VRAM monitoring
- Record all individual measurements, not just aggregates

**Rationale:**
- 5 runs provide enough data for mean, median, std dev
- Warm-up accounts for model loading cache effects
- `perf_counter_ns` offers sub-microsecond precision
- Recording raw data enables post-hoc analysis

---

*Last Updated: 2026-11-21*
