"""
SLM Evaluation Harness — Model Registry

Catalog of SLM checkpoints with metadata for format, quantization,
license, and compatibility information.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class ModelFamily(Enum):
    PHI = "microsoft-phi"
    GEMMA = "google-gemma"
    QWEN = "alibaba-qwen"
    SMOLLM = "huggingface-smollm"
    LLAMA = "meta-llama"
    MISTRAL = "mistralai"
    OTHER = "other"


class QuantizationType(Enum):
    FP16 = "fp16"
    FP32 = "fp32"
    INT8 = "int8"
    Q8_0 = "q8_0"
    Q6_K = "q6_k"
    Q5_K_M = "q5_k_m"
    Q4_K_M = "q4_k_m"
    Q4_0 = "q4_0"
    Q3_K_M = "q3_k_m"
    Q2_K = "q2_k"
    GPTQ_4BIT = "gptq_4bit"
    AWQ_4BIT = "awq_4bit"
    NONE = "none"


@dataclass
class ModelEntry:
    """A single model checkpoint in the registry."""
    # Identity
    model_id: str                              # Unique identifier
    display_name: str                          # Human-readable name
    family: ModelFamily
    
    # Technical specs
    parameters_billions: float                 # e.g., 1.5, 2.0, 3.8
    
    # File info
    format: str                                # "gguf", "safetensors", "onnx"
    quantization: QuantizationType = QuantizationType.NONE
    file_size_mb: Optional[int] = None         # Approximate download size
    
    # Sources
    huggingface_repo: str = ""                 # e.g., "microsoft/Phi-3-mini-4k-instruct-gguf"
    download_filename: str = ""                # Specific file within the repo
    
    # License
    license: str = "Unknown"
    license_url: str = ""
    
    # Compatibility (known)
    compatible_runtimes: list[str] = field(default_factory=list)   # ["llama_cpp", "transformers"]
    min_ram_mb: int = 0                        # Estimated minimum RAM required
    min_vram_mb: int = 0                       # Estimated minimum VRAM (0 = CPU only)
    
    # Status
    tested: bool = False
    test_notes: str = ""

    def fits_vram(self, vram_mb: int) -> bool:
        """Check if this model can fit in the given VRAM."""
        if self.min_vram_mb == 0:
            return True  # CPU-only compatible
        return vram_mb >= self.min_vram_mb

    def summary(self) -> str:
        quant = f" ({self.quantization.value})" if self.quantization != QuantizationType.NONE else ""
        size = f", ~{self.file_size_mb} MB" if self.file_size_mb else ""
        return f"{self.display_name} [{self.parameters_billions}B, {self.format}{quant}{size}]"


class ModelRegistry:
    """
    Central registry of available SLM models.
    
    Models are added programmatically or loaded from a config file.
    The registry tracks compatibility, tested status, and download info.
    """
    
    def __init__(self) -> None:
        self._models: dict[str, ModelEntry] = {}
    
    def register(self, model: ModelEntry) -> None:
        """Add a model to the registry."""
        self._models[model.model_id] = model
    
    def get(self, model_id: str) -> Optional[ModelEntry]:
        """Retrieve a model by ID."""
        return self._models.get(model_id)
    
    def list_all(self) -> list[ModelEntry]:
        """List all registered models."""
        return list(self._models.values())
    
    def list_by_family(self, family: ModelFamily) -> list[ModelEntry]:
        """List models from a specific family."""
        return [m for m in self._models.values() if m.family == family]
    
    def list_compatible(self, runtime: str, vram_mb: int = 0) -> list[ModelEntry]:
        """List models compatible with a given runtime and VRAM budget."""
        results = []
        for m in self._models.values():
            if runtime in m.compatible_runtimes:
                if vram_mb == 0 or m.fits_vram(vram_mb):
                    results.append(m)
        return results
    
    def list_tested(self) -> list[ModelEntry]:
        """List only models that have been actually tested."""
        return [m for m in self._models.values() if m.tested]
    
    @property
    def count(self) -> int:
        return len(self._models)
    
    def summary_table(self) -> str:
        """Generate a text summary table of all registered models."""
        if not self._models:
            return "No models registered."
        
        lines = [
            f"{'Model ID':<35} {'Family':<15} {'Params':<8} {'Format':<12} {'Quant':<10} {'Tested':<8}",
            "─" * 90,
        ]
        for m in self._models.values():
            lines.append(
                f"{m.model_id:<35} {m.family.value:<15} {m.parameters_billions:<8.1f} "
                f"{m.format:<12} {m.quantization.value:<10} {'✓' if m.tested else '✗':<8}"
            )
        return "\n".join(lines)


def build_default_registry() -> ModelRegistry:
    """
    Build the default model registry with candidate SLMs.
    
    NOTE: These entries are CANDIDATES — they have not been tested yet.
    The 'tested' field is False until actual benchmark runs confirm compatibility.
    Model details will be verified and updated during Week 2 model selection.
    """
    registry = ModelRegistry()
    
    # ── Placeholder entries — to be populated after web research in model_selection.md ──
    # Entries will be added after verifying:
    #   1. Exact checkpoint availability on HuggingFace
    #   2. GGUF quantization availability
    #   3. License compatibility
    #   4. Estimated VRAM requirements
    #   5. Runtime compatibility
    
    return registry


# ─── Package exports ─────────────────────────────────────────────
__all__ = [
    "ModelEntry", "ModelFamily", "QuantizationType",
    "ModelRegistry", "build_default_registry",
]
