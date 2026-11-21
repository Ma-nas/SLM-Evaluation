# Literature Review

## Small Language Models: Landscape, Compression, Runtimes, and Benchmarking

---

## 1. Introduction

The field of Natural Language Processing has undergone a paradigm shift since the emergence of large language models (LLMs). While models with hundreds of billions of parameters have demonstrated remarkable capabilities, the practical reality of deployment—cost, latency, privacy, and hardware requirements—has catalyzed a counter-movement toward **Small Language Models (SLMs)**, typically defined as models with 1B to 10B parameters. These models aim to deliver competitive task performance while fitting within the resource constraints of consumer devices, edge hardware, and privacy-sensitive environments.

This literature review surveys five key areas relevant to our research: (1) the SLM landscape and model families, (2) model compression and quantization techniques, (3) inference runtimes for desktop and edge deployment, (4) existing benchmarking frameworks and their limitations, and (5) edge AI and on-device inference challenges.

---

## 2. The Small Language Model Landscape

### 2.1 Microsoft Phi Series

The Phi family pioneered the "data quality over scale" philosophy. Beginning with **Phi-1** (1.3B, 2023), Microsoft demonstrated that models trained on carefully curated "textbook-quality" synthetic data could achieve disproportionately strong performance on coding and reasoning tasks relative to their size.

- **Phi-2** (2.7B, 2023): Achieved performance comparable to Mistral-7B and LLaMA-2-7B on several benchmarks, despite being less than half the size.
- **Phi-3-mini** (3.8B, 2024): Released in multiple context-length variants (4K and 128K tokens). Demonstrated strong mathematical reasoning and coding performance. Available under MIT license, making it one of the most permissively licensed SLMs.
- **Phi-3.5-mini** (3.8B, 2024): Incremental improvement over Phi-3-mini with better multilingual and long-context performance.
- **Phi-4-mini** (2025): Continued the trend of dense reasoning capability at small scale.

The Phi series established that aggressive data curation and synthetic data generation can substitute for raw parameter count, a finding with significant implications for edge deployment.

**References:**
- [Gunasekar2023] Gunasekar et al., "Textbooks Are All You Need," arXiv:2306.11644, 2023.
- [Abdin2024] Abdin et al., "Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone," arXiv:2404.14219, 2024.

### 2.2 Google Gemma Series

The Gemma family derives from Google's Gemini research, offering open-weight models designed for efficiency and broad deployment.

- **Gemma 1** (2B, 7B, 2024): Dense transformer architectures with strong general-purpose performance.
- **Gemma 2** (2B, 9B, 27B, 2024): Introduced sliding-window attention and alternating attention patterns. The **Gemma-2-2B** variant (approximately 2.6B parameters) is particularly relevant for resource-constrained evaluation, offering 8K context length.
- **Gemma 3** (2025): Expanded into multimodal variants.

Gemma models are released under the Gemma Terms of Use, a custom permissive license that allows commercial use with safety and acceptable-use restrictions.

**References:**
- [GemmaTeam2024] Gemma Team, Google DeepMind, "Gemma: Open Models Based on Gemini Research and Technology," arXiv:2403.08295, 2024.
- [GemmaTeam2024b] Gemma Team, "Gemma 2: Improving Open Language Models at a Practical Size," Google DeepMind Technical Report, 2024.

### 2.3 Alibaba Qwen Series

The Qwen family from Alibaba Cloud is notable for its granular size range and strong multilingual capabilities.

- **Qwen2** (0.5B, 1.5B, 7B, 72B, 2024): Broad parameter range with particular strength in Chinese-English bilingual tasks.
- **Qwen2.5** (0.5B, 1.5B, 3B, 7B, 14B, 72B, 2024): Significant improvements in coding, mathematics, structured data extraction (JSON parsing), and tool calling. The **Qwen2.5-1.5B-Instruct** variant (1.54B total parameters, 1.31B non-embedding) uses SwiGLU activation, RMSNorm, and Grouped-Query Attention (GQA with 12 Q heads and 2 KV heads), supports 29+ languages, and handles contexts up to 32K tokens.

Released under the Apache 2.0 license, making them highly permissive for research and commercial use.

**References:**
- [Yang2024] Yang et al., "Qwen2 Technical Report," arXiv:2407.10671, 2024.
- [Qwen2024] Qwen Team, "Qwen2.5: A Party of Foundation Models," Alibaba Cloud Blog, 2024.

### 2.4 HuggingFace SmolLM

SmolLM represents the ultra-compact end of the SLM spectrum, specifically designed for on-device execution.

- **SmolLM** (135M, 360M, 1.7B, 2024): Trained on the SmolLM-Corpus derived from FineWeb-Edu, Cosmopedia, and Python-Edu.
- **SmolLM2** (135M, 360M, 1.7B, 2024): Trained on 11 trillion tokens spanning FineWeb-Edu, DCLM, The Stack, and custom math/coding datasets. Instruction-tuned using DPO (Direct Preference Optimization) via UltraFeedback and Argilla datasets. 8K context length, Apache 2.0 license.

SmolLM2-1.7B is state-of-the-art for its size class, demonstrating that sub-2B models can handle meaningful dialogue, math, and code generation.

**References:**
- [Allal2024] Allal et al., "SmolLM — blazingly fast and remarkably powerful," HuggingFace Blog, 2024.
- [HuggingFace2024] HuggingFace, "SmolLM2 Model Card," huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct, 2024.

### 2.5 Meta LLaMA and Mistral (Reference Points)

- **LLaMA 3.2** (1B, 3B, 2024): Meta's compact models explicitly optimized for edge and mobile deployment, with native tool-calling support.
- **Mistral 7B** (7.3B, 2023): While exceeding the SLM boundary, Mistral's architectural innovations (sliding-window attention, grouped-query attention) influenced subsequent SLM designs.

**References:**
- [Touvron2023] Touvron et al., "LLaMA: Open and Efficient Foundation Language Models," arXiv:2302.13971, 2023.
- [Jiang2023] Jiang et al., "Mistral 7B," arXiv:2310.06825, 2023.

---

## 3. Model Compression and Quantization

Quantization reduces model precision from floating-point (FP16/FP32) to lower bit-widths, dramatically reducing memory footprint and improving inference throughput.

### 3.1 Post-Training Quantization (PTQ)

- **GPTQ** (Frantar et al., 2023): One-shot weight quantization using approximate second-order information. Achieves 4-bit quantization with minimal perplexity increase. Requires calibration data.
- **AWQ** (Lin et al., 2024): Activation-Aware Weight Quantization. Identifies salient weight channels and applies per-channel scaling before quantization. Generally preserves quality better than uniform quantization.
- **Round-to-Nearest (RTN)**: Simplest quantization approach; competitive at 8-bit but degrades at 4-bit.

### 3.2 GGUF Format and K-Quant Methods

The GGUF (GPT-Generated Unified Format) format, developed for llama.cpp, has become the de facto standard for local inference. GGUF encapsulates model weights, tokenizer, and metadata in a single file.

The K-quant quantization methods introduced in llama.cpp provide mixed-precision quantization:

| Level | Bits Per Weight | Relative Size | Quality Retention |
|-------|----------------|---------------|-------------------|
| Q8_0 | ~8.5 | ~53% of FP16 | ~99.8% |
| Q6_K | ~6.5 | ~42% | ~99% |
| Q5_K_M | ~5.7 | ~36% | ~98% |
| **Q4_K_M** | **~4.5** | **~30%** | **~95-97%** |
| Q3_K_M | ~3.5 | ~22% | ~90-93% |
| Q2_K | ~2.5 | ~15% | ~80-85% |

**Q4_K_M** is widely regarded as the "sweet spot," assigning slightly higher precision (5-6 bit) to critical layers while compressing less sensitive layers to 4 bits. For a 3.8B parameter model, Q4_K_M reduces the file from ~7.6GB (FP16) to ~2.3GB.

**References:**
- [Frantar2023] Frantar et al., "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers," arXiv:2210.17323, 2023.
- [Lin2024] Lin et al., "AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration," arXiv:2306.00978, 2024.

---

## 4. Inference Runtimes

### 4.1 llama.cpp

An open-source C/C++ inference engine originally targeting Meta's LLaMA models, now supporting a broad range of architectures. Key characteristics:
- **GGUF format**: Single-file model format with embedded tokenizer and metadata.
- **CPU + GPU hybrid offloading**: Can distribute model layers between CPU (RAM) and GPU (VRAM), critical for VRAM-limited devices.
- **K-quant support**: Native support for the full range of GGUF quantization levels.
- **Cross-platform**: Linux, macOS, Windows, with CUDA, Metal, and Vulkan GPU backends.
- **Python bindings**: `llama-cpp-python` provides a Python API compatible with OpenAI's API format.

llama.cpp's memory efficiency makes it the primary choice for VRAM-constrained consumer hardware.

**References:**
- [Gerganov2023] Gerganov, G., "llama.cpp," github.com/ggerganov/llama.cpp, 2023–present.

### 4.2 HuggingFace Transformers / PyTorch

The standard research ecosystem for LLM inference and fine-tuning:
- **Broad model support**: Supports virtually every published model architecture via the AutoModel API.
- **Formats**: SafeTensors (default), PyTorch .bin files.
- **Quantization**: bitsandbytes (4-bit/8-bit via NF4), GPTQ, AWQ integration.
- **GPU**: Full CUDA support, automatic device placement.
- **Drawbacks**: Higher memory overhead than llama.cpp; designed primarily for training, not optimized inference.

**References:**
- [Wolf2020] Wolf et al., "Transformers: State-of-the-Art Natural Language Processing," EMNLP 2020 (System Demonstrations).

### 4.3 ONNX Runtime

Microsoft's cross-platform inference engine:
- **ONNX format**: Standardized graph representation for ML models.
- **Backends**: CUDA, DirectML, TensorRT, CPU.
- **ORT GenAI**: Specialized extension for generative AI models.
- **Limitations**: Requires model conversion to ONNX format; not all architectures are fully supported. GenAI support for newer model architectures may lag.

### 4.4 Other Runtimes (Context)

- **vLLM**: Server-focused, PagedAttention for throughput optimization. Not designed for single-device benchmarking.
- **TensorRT-LLM**: NVIDIA-specific, optimized for data-center GPUs. Overkill for consumer hardware.
- **MLC-LLM**: Targets mobile/web deployment via Apache TVM compilation.

---

## 5. Existing Benchmarking Frameworks

### 5.1 EleutherAI lm-evaluation-harness

The most widely used open-source LLM evaluation framework. Supports hundreds of tasks (MMLU, HellaSwag, ARC, WinoGrande, etc.) with standardized prompting and scoring. However, it focuses exclusively on **model quality** (accuracy, perplexity) and does not measure inference performance metrics (latency, throughput, memory).

**References:**
- [Gao2023] Gao et al., "A framework for few-shot language model evaluation," Zenodo, 2023. github.com/EleutherAI/lm-evaluation-harness.

### 5.2 HuggingFace Open LLM Leaderboard

Aggregates lm-evaluation-harness results for community-submitted models. Provides quality comparisons but: (a) runs on standardized server hardware, not consumer devices; (b) does not report latency, throughput, or memory; (c) does not consider quantization effects or runtime differences.

### 5.3 MLPerf Inference

Industry-standard benchmark suite from MLCommons for hardware inference performance. Covers multiple ML tasks but: (a) primarily targets data-center and cloud hardware; (b) complex submission process; (c) limited coverage of LLM-specific metrics like TTFT.

### 5.4 Gaps in Existing Frameworks

None of the established benchmarking frameworks:
1. Compare the same model across multiple inference runtimes on the same hardware.
2. Measure deployment-relevant metrics (TTFT, peak VRAM, model loading time) alongside quality.
3. Formally characterize the device running the benchmark using a standardized schema.
4. Analyze landscape lock-in: which model-format-runtime combinations are possible and which are blocked.

---

## 6. Edge AI and On-Device Inference

The deployment of language models on consumer and edge devices faces several well-documented challenges:

1. **Memory constraints**: Consumer GPUs have 4–12 GB VRAM, requiring aggressive quantization for models >2B parameters.
2. **Thermal throttling**: Sustained inference on laptops causes thermal throttling, introducing measurement variability.
3. **Format fragmentation**: Models published in one format (e.g., SafeTensors) may not be directly usable in another runtime (e.g., llama.cpp), requiring conversion steps that may introduce errors.
4. **Runtime dependencies**: Each runtime requires specific libraries, drivers, and sometimes hardware features (e.g., CUDA compute capability ≥7.0).
5. **Reproducibility**: Without standardized device descriptions and measurement protocols, benchmark results across papers are incomparable.

By 2025, the technical enablers for edge SLM deployment have matured significantly—quantization is robust, runtimes are cross-platform, and sub-4B models achieve practical quality—but the evaluation methodology has not kept pace. This creates the research opportunity our project addresses.

---

## 7. Summary

The convergence of high-quality SLMs (Phi, Gemma, Qwen, SmolLM), efficient quantization (GGUF K-quants), and cross-platform runtimes (llama.cpp, Transformers) has made on-device LLM inference practical. However, the benchmarking ecosystem remains fragmented: quality and performance are evaluated separately, runtime comparisons are ad-hoc, device characteristics are unreported, and format/runtime lock-in is unexamined. Our project addresses this gap with a unified evaluation harness.

---

*Last Updated: 2026-11-21*
