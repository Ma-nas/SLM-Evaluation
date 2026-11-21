# SLM-Evaluation

## Landscape Lock-In, Device-Class Specification, and Cross-Platform Evaluation Harness for Small Language Models (SLMs)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

### Project Overview

A modular Python framework for benchmarking Small Language Models (SLMs) across different inference runtimes and device classes. The project investigates **landscape lock-in** (ecosystem dependencies that constrain model portability), defines a **device-class specification** for characterizing inference hardware, and provides a **cross-platform evaluation harness** for reproducible SLM benchmarking.

### Research Questions

| ID | Question |
|----|----------|
| RQ1 | How does SLM performance vary across different device classes (CPU-only vs GPU-assisted)? |
| RQ2 | How do inference runtimes affect model performance, compatibility, and portability? |
| RQ3 | What trade-offs exist between quantization, model quality, inference speed, and resource consumption? |
| RQ4 | How can a standardized evaluation harness improve benchmark reproducibility? |

### Key Features

- **Device Profiler** — Automatic detection of CPU, GPU, RAM, VRAM, OS, and driver versions
- **Model Registry** — Catalog of SLM checkpoints with format, quantization, and compatibility metadata
- **Runtime Adapters** — Unified interface for llama.cpp, Transformers/PyTorch, and ONNX Runtime
- **Benchmark Engine** — Controlled measurement of TTFT, throughput, latency, and memory consumption
- **Quality Evaluation** — Task-specific quality metrics alongside performance benchmarks
- **Results Storage** — SQLite database with full experiment metadata for reproducibility
- **Visualization** — Statistical analysis and comparison charts

### Project Structure

```
SLM-Evaluation/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── research/            # Literature review, gap analysis, model selection
│   ├── architecture/        # System design, device specification
│   ├── experimental-design/ # Benchmark methodology, prompt workloads
│   └── report/              # University research report
├── src/
│   ├── models/              # Model registry and management
│   ├── devices/             # Device profiler and specification
│   ├── runtimes/            # Runtime adapter interface and implementations
│   ├── benchmarks/          # Benchmark execution engine
│   ├── evaluation/          # Quality evaluation metrics
│   ├── monitoring/          # Resource monitoring (RAM, VRAM)
│   ├── config/              # Central configuration
│   └── utils/               # Timer, logging, helpers
├── tests/                   # Unit and integration tests
├── configs/                 # Experiment configuration files
├── scripts/                 # CLI scripts for running benchmarks
├── results/
│   ├── raw/                 # Raw experiment data
│   ├── processed/           # Aggregated statistics
│   └── figures/             # Generated charts and graphs
└── presentation/            # Slides and viva preparation
```

### Hardware Requirements

| Component | Minimum | Tested On |
|-----------|---------|-----------|
| CPU | x86_64, 4+ cores | Intel i5-12450H (8C/12T) |
| RAM | 8 GB | 16 GB |
| GPU | NVIDIA with CUDA (optional) | RTX 3050 Laptop (4 GB VRAM) |
| OS | Windows 10 / Linux | Windows 11 Build 26300 |
| Python | 3.10+ | 3.14.3 |

### Installation

```bash
# Clone the repository
git clone https://github.com/Ma-nas/SLM-Evaluation.git
cd SLM-Evaluation

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Quick Start

```bash
# Profile your device
python scripts/profile_device.py

# Run benchmarks (after downloading models)
python scripts/run_benchmark.py --config configs/default.yaml

# View results
python scripts/visualize_results.py
```

### Team

| Member | Role | Responsibilities |
|--------|------|-----------------|
| Member 1 | Research Scientist | Literature review, SLM selection, quality evaluation |
| Member 2 | System Architect | Device profiling, runtime integration, compatibility |
| Member 3 | Benchmarking Specialist | Benchmark execution, data analysis, visualization |

### Status

**Phase:** Week 1 — Research Foundation

See [PROGRESS_TRACKER.md](PROGRESS_TRACKER.md) for detailed status.

### License

This project is developed as part of a B.Tech final year project at JAIN (Deemed-to-be University).

---

*Academic Year 2025–2026*
