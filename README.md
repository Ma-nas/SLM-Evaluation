<p align="center">
  <h1 align="center">SLM-Evaluation</h1>
  <p align="center">
    <strong>Cross-Platform Evaluation Harness for Small Language Models</strong>
  </p>
  <p align="center">
    <a href="#quick-start">Quick Start</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#models">Models</a> •
    <a href="#benchmarks">Benchmarks</a> •
    <a href="docs/">Documentation</a>
  </p>
</p>

---

> **Landscape Lock-In, Device-Class Specification, and Cross-Platform Evaluation Harness for Small Language Models (SLMs)**

A modular Python framework for benchmarking Small Language Models across inference runtimes and device classes. Investigates ecosystem lock-in, defines hardware specifications, and provides reproducible measurement protocols.

## Research Questions

| ID | Question |
|----|----------|
| **RQ1** | How does SLM performance vary across different device classes (CPU-only vs GPU-assisted)? |
| **RQ2** | How do inference runtimes affect model performance, compatibility, and portability? |
| **RQ3** | What trade-offs exist between quantization, model quality, inference speed, and resource consumption? |
| **RQ4** | How can a standardized evaluation harness improve benchmark reproducibility? |

## Architecture

```
src/
├── config/          # Central configuration and settings
├── devices/         # Hardware profiler and device-class specification
├── models/          # Model registry with format and compatibility metadata
├── runtimes/        # Runtime adapter interface (llama.cpp, Transformers, ONNX)
├── benchmarks/      # Benchmark engine and SQLite results storage
├── evaluation/      # Task-quality evaluation metrics
├── monitoring/      # RAM and VRAM resource monitoring
└── utils/           # Timer, logging, and shared utilities
```

## Models

Four SLM families selected for cross-platform evaluation:

| Model | Parameters | License | Formats |
|-------|-----------|---------|---------|
| [Phi-3-mini-4k-instruct](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) | 3.8B | MIT | GGUF, SafeTensors |
| [Gemma-2-2B-it](https://huggingface.co/google/gemma-2-2b-it) | 2.6B | Gemma ToU | GGUF, SafeTensors |
| [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) | 1.54B | Apache 2.0 | GGUF, SafeTensors |
| [SmolLM2-1.7B-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct) | 1.7B | Apache 2.0 | GGUF, SafeTensors |

## Benchmarks

Metrics collected per configuration:

| Metric | Unit | Method |
|--------|------|--------|
| Model Loading Time | seconds | `time.perf_counter_ns()` |
| Time to First Token (TTFT) | ms | Streaming callback |
| Tokens Per Second (TPS) | tok/s | Output tokens ÷ generation time |
| End-to-End Latency | seconds | Wall clock |
| Peak RAM | MB | `psutil` |
| Peak VRAM | MB | `nvidia-smi` |

## Quick Start

```bash
# Clone
git clone https://github.com/Ma-nas/SLM-Evaluation.git
cd SLM-Evaluation

# Install core dependencies
pip install -r requirements.txt

# Profile your hardware
python scripts/profile_device.py

# Run tests
python -m pytest tests/ -v
```

## Hardware Tested

| Component | Specification |
|-----------|---------------|
| CPU | Intel i5-12450H (8C/12T) |
| RAM | 16 GB |
| GPU | NVIDIA RTX 3050 Laptop (4 GB VRAM) |
| OS | Windows 11 |
| Python | 3.14 |

## Repository Structure

```
SLM-Evaluation/
├── README.md                   # This file
├── LICENSE                     # MIT License
├── requirements.txt            # Python dependencies
├── .gitignore
│
├── src/                        # Source code
│   ├── config/                 #   Central configuration
│   ├── devices/                #   Device profiler
│   ├── models/                 #   Model registry
│   ├── runtimes/               #   Runtime adapters (llama.cpp, Transformers)
│   ├── benchmarks/             #   Benchmark engine + SQLite storage
│   ├── evaluation/             #   Quality metrics
│   ├── monitoring/             #   Resource monitoring
│   └── utils/                  #   Timer, logging utilities
│
├── tests/                      # Unit and integration tests
├── scripts/                    # CLI tools (profiler, benchmark runner)
├── configs/                    # Experiment configurations (YAML)
│
├── docs/                       # Documentation
│   ├── research/               #   Literature review, model selection, gap analysis
│   ├── architecture/           #   System design, device specification
│   ├── experimental-design/    #   Benchmark methodology
│   ├── project-management/     #   Planning, tracking, risk register
│   └── report/                 #   University research report
│
├── results/                    # Experiment outputs
│   ├── raw/                    #   Raw benchmark data
│   ├── processed/              #   Aggregated statistics
│   └── figures/                #   Generated charts
│
└── presentation/               # Slides and viva preparation
```

## Team

| Role | Responsibilities |
|------|-----------------|
| **Research Scientist** | Literature review, model selection, quality evaluation |
| **System Architect** | Device profiling, runtime adapters, compatibility matrix |
| **Benchmarking Specialist** | Experiment execution, statistical analysis, visualization |

See [`docs/project-management/TEAM_TASKS.md`](docs/project-management/TEAM_TASKS.md) for detailed task tracking.

## Documentation

| Document | Description |
|----------|-------------|
| [Literature Review](docs/research/literature_review.md) | SLM landscape, quantization, runtimes, benchmarking frameworks |
| [Research Gap](docs/research/research_gap.md) | Identified gaps and our contributions |
| [Model Selection](docs/research/model_selection.md) | Candidate analysis and final selection rationale |
| [Project Master Plan](docs/project-management/PROJECT_MASTER_PLAN.md) | Six-week execution plan |
| [Architecture Decisions](docs/project-management/ARCHITECTURE_DECISIONS.md) | Technical decision log |
| [Risk Register](docs/project-management/RESEARCH_RISK_REGISTER.md) | Risk assessment and mitigations |

## License

[MIT](LICENSE)

---

<sub>B.Tech Final Year Project — JAIN (Deemed-to-be University) — 2025–2026</sub>
