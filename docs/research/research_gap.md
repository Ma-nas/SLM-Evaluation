# Research Gap Analysis

## Identifying the Need for a Cross-Platform SLM Evaluation Harness

---

## 1. Overview

Despite the rapid proliferation of Small Language Models and the maturing ecosystem of inference runtimes and quantization techniques, a systematic gap exists in how these models are evaluated for real-world deployment. This document identifies four specific gaps in the current research and practice, and explains how our project addresses each.

---

## 2. Gap 1: Separation of Quality and Performance Evaluation

**Current State:** The dominant evaluation frameworks (lm-evaluation-harness, Open LLM Leaderboard) measure model quality—accuracy on benchmarks like MMLU, HellaSwag, ARC, WinoGrande—but report zero information about inference performance. Conversely, throughput benchmarks (e.g., llama.cpp's built-in `--benchmark` mode) measure tokens/sec but not task quality.

**The Problem:** A practitioner choosing an SLM for deployment needs to answer: "Which model gives me acceptable quality AND fits within my latency and memory budget?" Today, this requires consulting multiple disconnected tools and manually correlating results, with no guarantee that measurements were taken under comparable conditions.

**Our Contribution:** Our evaluation harness measures both performance metrics (TTFT, tokens/sec, peak RAM/VRAM, model loading time) and task quality in the same framework, on the same hardware, with the same prompts. This enables direct quality-vs-performance trade-off analysis.

---

## 3. Gap 2: No Systematic Cross-Runtime Comparison

**Current State:** When researchers report SLM inference performance, they typically use a single runtime (e.g., only llama.cpp, or only Transformers). There is no published framework that systematically runs the same model across multiple runtimes on the same hardware using a controlled protocol.

**The Problem:** Different runtimes have fundamentally different characteristics:
- llama.cpp is optimized for quantized GGUF models with CPU+GPU hybrid offloading.
- Transformers/PyTorch provides the broadest model support but higher memory overhead.
- ONNX Runtime offers graph-level optimizations but limited model coverage.

Without controlled comparison, practitioners cannot determine whether observed performance differences are due to the model, the runtime, the quantization method, or the hardware.

**Our Contribution:** We define a `RuntimeAdapter` abstract interface and implement adapters for multiple runtimes. The benchmark engine runs identical prompts with identical generation parameters through each adapter, isolating the runtime variable. The compatibility matrix records which model×runtime combinations work and which don't.

---

## 4. Gap 3: Landscape Lock-In is Not Formally Studied

**Current State:** The SLM ecosystem exhibits significant format and runtime dependencies:
- GGUF models work with llama.cpp but not Transformers (without conversion).
- SafeTensors models work with Transformers but not llama.cpp.
- ONNX models require specific conversion and may not support all architectures.
- Quantization methods are runtime-specific (K-quants for GGUF, bitsandbytes for Transformers, QDQ for ONNX).
- GPU acceleration requires specific drivers, CUDA versions, and compute capabilities.

**The Problem:** These dependencies create "landscape lock-in"—once a practitioner selects a runtime, they are constrained to specific model formats and quantization methods, limiting portability and reproducibility. This phenomenon is widely experienced but not systematically documented or analyzed.

**Our Contribution:** We create a formal **compatibility matrix** mapping Model × Format × Runtime × Device-Class, recording for each combination whether it is: supported, unsupported, tested successfully, tested with failure, not tested, or requires conversion. This provides the first systematic documentation of SLM landscape lock-in.

---

## 5. Gap 4: No Standardized Device-Class Specification

**Current State:** When SLM benchmarks are reported in papers and blog posts, hardware descriptions range from detailed ("NVIDIA A100 80GB, CUDA 12.1, 128GB RAM") to vague ("tested on a laptop") to absent. There is no standardized schema for describing the device running the benchmark.

**The Problem:** Without standardized device descriptions, benchmark results cannot be meaningfully compared across papers, reproduced on different hardware, or extrapolated to deployment targets. A model that runs at 50 tok/s on one "laptop" might achieve 15 tok/s on another, depending on undisclosed CPU, GPU, and memory specifications.

**Our Contribution:** We define a formal **Device-Class Specification** schema that captures: CPU (model, architecture, cores, threads, clock speed), GPU (model, VRAM, compute capability, driver version), RAM, OS, Python version, available accelerators, and known measurement limitations. This schema is extensible to future device categories (mobile, edge, server) and enables reproducible hardware characterization.

---

## 6. Summary of Gaps and Contributions

| Gap | Current State | Our Contribution |
|-----|---------------|------------------|
| Quality vs. Performance | Evaluated separately in different tools | Unified harness measuring both |
| Cross-Runtime Comparison | Single-runtime benchmarks, no controlled protocol | Multi-runtime adapter interface with identical workloads |
| Landscape Lock-In | Experienced but undocumented | Formal compatibility matrix |
| Device Specification | Ad-hoc, inconsistent hardware descriptions | Standardized device-class schema |

---

## 7. Research Questions Derived from Gaps

Each research question directly maps to an identified gap:

- **RQ1** (device-class variation) ← Gap 4 (no standardized device specification)
- **RQ2** (runtime effects) ← Gap 2 (no cross-runtime comparison) + Gap 3 (lock-in)
- **RQ3** (quantization trade-offs) ← Gap 1 (quality-performance separation)
- **RQ4** (harness reproducibility) ← Gap 4 (device specification) + Gap 2 (cross-runtime protocol)

---

*Last Updated: 2026-11-21*
