# Preliminary Model Selection

## SLM Candidates for Cross-Platform Evaluation

---

## 1. Selection Criteria

Models are evaluated against the following requirements:

| Criterion | Requirement |
|-----------|-------------|
| Parameter count | ≤ 3.8B (to fit in 4GB VRAM with quantization) |
| GGUF availability | Must have Q4_K_M and Q8_0 GGUF variants on HuggingFace |
| SafeTensors availability | Must be available for Transformers runtime |
| License | Must permit academic research use |
| Instruct-tuned | Prefer instruction-tuned variants for task evaluation |
| Active maintenance | Model card and community support available |

---

## 2. Candidate Survey

### 2.1 Microsoft Phi-3-mini-4k-instruct

| Attribute | Value |
|-----------|-------|
| **Parameters** | 3.8B |
| **Family** | Microsoft Phi-3 |
| **Context Length** | 4,096 tokens |
| **Architecture** | Decoder-only transformer |
| **License** | MIT (permissive) |
| **HuggingFace Repo** | `microsoft/Phi-3-mini-4k-instruct` |
| **GGUF Availability** | ✅ `QuantFactory/Phi-3-mini-4k-instruct-GGUF`, `bartowski/Phi-3-mini-4k-instruct-GGUF` |
| **SafeTensors** | ✅ Official repo |
| **Q4_K_M Size** | ~2.2 GB |
| **Q8_0 Size** | ~4.0 GB |
| **FP16 Size** | ~7.6 GB |
| **Estimated VRAM (Q4_K_M)** | ~2.5 GB (fits in 4GB) |
| **Estimated VRAM (Q8_0)** | ~4.3 GB (marginal — may need partial CPU offloading) |
| **Known Strengths** | Strong reasoning, math, code |
| **llama.cpp Compatible** | ✅ Yes |
| **Transformers Compatible** | ✅ Yes |

**Verdict:** ✅ **SELECTED** — Best-in-class reasoning at this size, MIT license, excellent GGUF support. The 3.8B size is the upper bound of what fits in 4GB VRAM at Q4.

---

### 2.2 Google Gemma-2-2B-it

| Attribute | Value |
|-----------|-------|
| **Parameters** | 2.6B |
| **Family** | Google Gemma 2 |
| **Context Length** | 8,192 tokens |
| **Architecture** | Decoder-only with sliding-window + global attention alternation |
| **License** | Gemma Terms of Use (permissive, allows commercial/research) |
| **HuggingFace Repo** | `google/gemma-2-2b-it` |
| **GGUF Availability** | ✅ `google/gemma-2-2b-GGUF`, `bartowski/gemma-2-2b-it-GGUF` |
| **SafeTensors** | ✅ Official repo |
| **Q4_K_M Size** | ~1.6 GB |
| **Q8_0 Size** | ~2.8 GB |
| **FP16 Size** | ~5.2 GB |
| **Estimated VRAM (Q4_K_M)** | ~2.0 GB (comfortably fits) |
| **Estimated VRAM (Q8_0)** | ~3.0 GB (fits in 4GB) |
| **Known Strengths** | General-purpose, good instruction following |
| **llama.cpp Compatible** | ✅ Yes |
| **Transformers Compatible** | ✅ Yes |

**Verdict:** ✅ **SELECTED** — Smaller than Phi-3, comfortably fits at Q8_0. Different architecture (Gemma vs Phi) provides interesting comparison. Official GGUF from Google.

---

### 2.3 Alibaba Qwen2.5-1.5B-Instruct

| Attribute | Value |
|-----------|-------|
| **Parameters** | 1.54B (1.31B non-embedding) |
| **Family** | Alibaba Qwen 2.5 |
| **Context Length** | 32,768 tokens (generates up to 8,192) |
| **Architecture** | Decoder-only, SwiGLU, RMSNorm, GQA (12 Q / 2 KV heads) |
| **License** | Apache 2.0 (highly permissive) |
| **HuggingFace Repo** | `Qwen/Qwen2.5-1.5B-Instruct` |
| **GGUF Availability** | ✅ `Qwen/Qwen2.5-1.5B-Instruct-GGUF` (official) |
| **SafeTensors** | ✅ Official repo |
| **Q4_K_M Size** | ~1.0 GB |
| **Q8_0 Size** | ~1.7 GB |
| **FP16 Size** | ~3.1 GB |
| **Estimated VRAM (Q4_K_M)** | ~1.3 GB (easily fits) |
| **Estimated VRAM (FP16)** | ~3.5 GB (fits in 4GB!) |
| **Known Strengths** | Multilingual (29+ languages), coding, JSON/structured output |
| **llama.cpp Compatible** | ✅ Yes |
| **Transformers Compatible** | ✅ Yes |

**Verdict:** ✅ **SELECTED** — Smallest selected model, fits in VRAM even at FP16. Official GGUF from Qwen team. Apache 2.0 license. Enables testing FP16 vs Q4 quality comparison on GPU.

---

### 2.4 HuggingFace SmolLM2-1.7B-Instruct

| Attribute | Value |
|-----------|-------|
| **Parameters** | 1.7B |
| **Family** | HuggingFace SmolLM2 |
| **Context Length** | 8,192 tokens |
| **Architecture** | Decoder-only transformer |
| **License** | Apache 2.0 |
| **HuggingFace Repo** | `HuggingFaceTB/SmolLM2-1.7B-Instruct` |
| **GGUF Availability** | ✅ `HuggingFaceTB/SmolLM2-1.7B-Instruct-GGUF` (official) |
| **SafeTensors** | ✅ Official repo |
| **Q4_K_M Size** | ~1.0 GB |
| **Q8_0 Size** | ~1.8 GB |
| **FP16 Size** | ~3.4 GB |
| **Estimated VRAM (Q4_K_M)** | ~1.3 GB (easily fits) |
| **Known Strengths** | On-device optimized, trained on 11T tokens, strong math/dialogue |
| **llama.cpp Compatible** | ✅ Yes |
| **Transformers Compatible** | ✅ Yes |

**Verdict:** ✅ **SELECTED** — State-of-the-art for sub-2B class. Official GGUF. Similar size to Qwen2.5-1.5B, enabling controlled comparison of different model families at comparable parameter counts.

---

## 3. Rejected Candidates

| Model | Reason for Rejection |
|-------|---------------------|
| Phi-3-mini-128k-instruct | Same parameters as 4K variant; 128K context increases memory usage; not needed for our benchmarks |
| Gemma-2-9B | 9B parameters — far exceeds 4GB VRAM budget even at Q4 |
| Qwen2.5-3B-Instruct | Could be included; deferred to keep matrix manageable. Can be added later. |
| LLaMA-3.2-1B/3B | Requires Meta license acceptance; potential gating complications |
| Mistral-7B | 7.3B parameters — exceeds VRAM budget |
| SmolLM2-360M | Too small for meaningful quality evaluation against larger SLMs |

---

## 4. Final Selection Summary

| # | Model | Parameters | VRAM (Q4_K_M) | License | Families Covered |
|---|-------|-----------|---------------|---------|-----------------|
| 1 | Phi-3-mini-4k-instruct | 3.8B | ~2.5 GB | MIT | Microsoft Phi |
| 2 | Gemma-2-2B-it | 2.6B | ~2.0 GB | Gemma ToU | Google Gemma |
| 3 | Qwen2.5-1.5B-Instruct | 1.54B | ~1.3 GB | Apache 2.0 | Alibaba Qwen |
| 4 | SmolLM2-1.7B-Instruct | 1.7B | ~1.3 GB | Apache 2.0 | HuggingFace SmolLM |

This selection provides:
- **Four different model families** for cross-family comparison
- **Three different parameter scales** (1.5B, 1.7B, 2.6B, 3.8B) for scaling analysis
- **All four models fit in 4GB VRAM** at Q4_K_M quantization
- **All have official GGUF** from model authors or verified community quantizers
- **All have permissive licenses** for academic research

---

## 5. Planned Experiment Matrix

Each model will be tested across these configurations (where hardware-compatible):

| Model | Q4_K_M + llama.cpp | Q8_0 + llama.cpp | FP16 + Transformers | Q4 + Transformers |
|-------|-------------------|------------------|--------------------|--------------------|
| Phi-3-mini | CPU ✓, GPU ✓ | CPU ✓, GPU ⚠️ | CPU only (>4GB) | TBD |
| Gemma-2-2B | CPU ✓, GPU ✓ | CPU ✓, GPU ✓ | CPU ✓, GPU ⚠️ | TBD |
| Qwen2.5-1.5B | CPU ✓, GPU ✓ | CPU ✓, GPU ✓ | CPU ✓, GPU ✓ | TBD |
| SmolLM2-1.7B | CPU ✓, GPU ✓ | CPU ✓, GPU ✓ | CPU ✓, GPU ✓ | TBD |

✓ = Expected to fit | ⚠️ = Marginal, needs testing | TBD = To be determined

> **NOTE:** All entries above are ESTIMATES based on model card data. Actual compatibility will be verified during Week 3 implementation.

---

*Last Updated: 2026-11-21*
