# RESEARCH RISK REGISTER

## Risk Assessment Matrix

| ID | Risk | Probability | Impact | Severity | Mitigation | Contingency |
|----|------|-------------|--------|----------|------------|-------------|
| R1 | **VRAM limitation (4GB)** prevents loading target models on GPU | High | High | **Critical** | Select Q4-quantized models ≤3B params; verify VRAM requirements before download | Fall back to CPU-only benchmarking for larger models |
| R2 | **ONNX Runtime GenAI** incompatible with target models on Windows | Medium | Medium | **High** | Investigate compatibility early in W2; treat as optional runtime | Proceed with llama.cpp + Transformers as primary runtimes |
| R3 | **Python 3.14 package compatibility** — missing wheels for torch, llama-cpp-python | Medium | High | **High** | Check PyPI for 3.14 wheels early; test `pip install` before committing to stack | Use `--no-build-isolation` or build from source; consider conda |
| R4 | **Thermal throttling** on laptop causes inconsistent benchmarks | High | Medium | **High** | Implement warm-up runs; take ≥5 repeated measurements; report std dev; run with power adapter | Use median instead of mean; document thermal conditions |
| R5 | **Background processes** affect measurement accuracy | Medium | Medium | **Medium** | Close unnecessary applications; document running processes; use process-level monitoring | Report measurement variance; flag outlier runs |
| R6 | **Model download size/time** exceeds practical limits | Medium | Low | **Medium** | Select smallest quantized variants (Q4_K_M); verify download sizes before selection | Use fewer model variants; prioritize GGUF (single file) |
| R7 | **llama-cpp-python CUDA build** fails on Windows | Medium | High | **High** | Follow Windows CUDA build instructions; check pre-built wheels | Fall back to CPU-only llama.cpp; use alternative runtime |
| R8 | **Insufficient experimental diversity** weakens research contribution | Low | High | **Medium** | Plan minimum viable experiment matrix early; prioritize breadth over depth | Document limitations honestly; frame as "initial evaluation" |
| R9 | **Report format mismatch** — template may require sections we can't map | Low | Medium | **Low** | Extract format early (done); map all required sections before drafting | Extend template structure where needed; note deviations |
| R10 | **Fabrication temptation** — pressure to show results for untested configurations | Low | Critical | **High** | Strict policy: mark untested as "NOT TESTED"; never generate synthetic results as real | Leave cells empty rather than fabricate; document what wasn't possible |
| R11 | **CUDA version mismatch** between driver and PyTorch/llama.cpp | Medium | High | **High** | Verify CUDA toolkit version matches driver (13.4 UMD); install matching PyTorch | Use CPU-only mode as fallback |
| R12 | **Disk space** insufficient for multiple model files | Medium | Low | **Medium** | Estimate total download size; clean unused models after benchmarking | Test with fewer models; delete after measurement |

---

## Technical Uncertainties

| ID | Uncertainty | Investigation Plan | Resolution Deadline |
|----|-------------|-------------------|---------------------|
| U1 | Can llama-cpp-python be installed with CUDA support on Python 3.14/Windows? | Test `pip install llama-cpp-python` with CUDA flags in W2 | End of Week 2 |
| U2 | Which Phi/Gemma/Qwen/SmolLM checkpoints have GGUF variants available? | Search HuggingFace Hub in W1–W2 | End of Week 2 |
| U3 | Does ONNX Runtime GenAI support text generation on Windows with CUDA? | Test installation and basic inference in W2 | End of Week 2 |
| U4 | Can PyTorch with Transformers fit any target model in 4GB VRAM? | Calculate FP16/INT8 memory requirements in W2 | End of Week 2 |
| U5 | Is psutil sufficient for GPU memory monitoring, or is pynvml needed? | Test both approaches in W2 | End of Week 2 |
| U6 | How stable are TTFT measurements on Windows (timer resolution)? | Test `time.perf_counter_ns()` in W3 | End of Week 3 |

---

## Assumptions

1. The laptop has sufficient disk space (≥20 GB free) for model files and results.
2. Internet connectivity is available for model downloads from HuggingFace Hub.
3. No external devices (mobile, edge) are available for testing — only the laptop.
4. The user will provide student names and registration numbers before final report generation.
5. The project is for 7th semester (based on template), academic year 2025–2026.

---

*Last Updated: 2026-11-21*
