# EXPERIMENT TRACKER

## Experiment Design

### Independent Variables
1. **Model**: SLM variant (e.g., Phi-3-mini, Gemma-2-2B, Qwen2.5-1.5B, SmolLM2-1.7B)
2. **Quantization**: FP16, Q8_0, Q4_K_M
3. **Runtime**: llama.cpp, Transformers/PyTorch, ONNX Runtime (if compatible)
4. **Device Class**: CPU-only, GPU-assisted (RTX 3050)

### Dependent Variables (Metrics)
| Metric | Unit | Collection Method |
|--------|------|-------------------|
| Model Loading Time | seconds | `time.perf_counter_ns()` |
| Time to First Token (TTFT) | milliseconds | Streaming callback timing |
| End-to-End Latency | seconds | Wall-clock start to finish |
| Time Per Output Token | milliseconds | Total generation time / output tokens |
| Output Tokens Per Second | tokens/sec | Computed from above |
| Peak RAM Usage | MB | `psutil.Process.memory_info()` |
| Peak VRAM Usage | MB | `nvidia-smi` / `pynvml` |
| Model File Size | MB | Filesystem |
| Task Quality Score | varies | Task-specific metrics (to be defined) |
| Runtime Compatibility | boolean | Does it run without error? |
| Failure Rate | percentage | Failed runs / total attempted runs |

### Controlled Variables
- Prompt dataset: Fixed set of standardized prompts
- Generation parameters: `max_tokens=256, temperature=0.0, top_p=1.0` (greedy decoding)
- Warm-up: 2 runs discarded before 5 measurement runs
- System state: Minimal background processes, power adapter connected
- Input length: Standardized per prompt category

### Experiment Matrix (Planned)

> **Status: NOT YET EXECUTED — All entries below are PLANNED, not measured**

| # | Model | Quantization | Runtime | Device | Status |
|---|-------|-------------|---------|--------|--------|
| — | TBD | TBD | TBD | TBD | ⬜ Not configured |

*The experiment matrix will be populated after model selection (Week 2) and runtime adapter implementation (Week 3).*

---

## Prompt Workload Categories (Planned)

| Category | Description | Approximate Input Length | Purpose |
|----------|-------------|------------------------|---------|
| Short QA | Simple factual questions | ~30 tokens | TTFT, quick response latency |
| Summarization | Summarize a short passage | ~200 tokens | Quality + throughput |
| Reasoning | Multi-step logical problem | ~100 tokens | Quality under constraint |
| Code Generation | Simple Python function | ~50 tokens | Quality + structured output |
| Instruction Following | Specific formatting task | ~80 tokens | Instruction adherence |

---

## Raw Data Storage

- Database: `results/benchmarks.db` (SQLite)
- Schema: To be designed in Week 3
- Raw logs: `results/raw/` directory
- Each run identified by UUID with full metadata

---

## Results (Pending Experiments)

> ⚠️ **No experiments have been executed yet.**
> This section will be populated with actual measurements starting in Week 4.

---

*Last Updated: 2026-11-21*
