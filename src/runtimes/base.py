"""
SLM Evaluation Harness — Runtime Adapter Interface

Abstract base class that all inference runtime adapters must implement.
This ensures consistent API across llama.cpp, Transformers, ONNX Runtime, etc.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Iterator
from enum import Enum


class RuntimeType(Enum):
    """Supported inference runtime types."""
    LLAMA_CPP = "llama_cpp"
    TRANSFORMERS = "transformers"
    ONNX = "onnx_runtime"


class ModelFormat(Enum):
    """Supported model file formats."""
    GGUF = "gguf"
    SAFETENSORS = "safetensors"
    PYTORCH = "pytorch"
    ONNX = "onnx"


@dataclass
class GenerationConfig:
    """Parameters for text generation, standardized across runtimes."""
    max_tokens: int = 256
    temperature: float = 0.0
    top_p: float = 1.0
    top_k: int = -1          # -1 means disabled
    repeat_penalty: float = 1.0
    seed: int = 42            # Fixed seed for reproducibility
    stop_sequences: list[str] = field(default_factory=list)


@dataclass
class GenerationResult:
    """Result of a single text generation call."""
    prompt: str
    output_text: str
    output_tokens: int
    prompt_tokens: int
    
    # Timing (all in milliseconds)
    time_to_first_token_ms: Optional[float] = None
    total_generation_time_ms: Optional[float] = None
    model_load_time_ms: Optional[float] = None
    
    # Computed metrics
    @property
    def tokens_per_second(self) -> Optional[float]:
        if self.total_generation_time_ms and self.output_tokens > 0:
            return self.output_tokens / (self.total_generation_time_ms / 1000)
        return None
    
    @property
    def time_per_output_token_ms(self) -> Optional[float]:
        if (self.total_generation_time_ms is not None 
            and self.time_to_first_token_ms is not None 
            and self.output_tokens > 1):
            decode_time = self.total_generation_time_ms - self.time_to_first_token_ms
            return decode_time / (self.output_tokens - 1)
        return None

    # Error tracking
    error: Optional[str] = None
    success: bool = True


@dataclass
class RuntimeInfo:
    """Metadata about a runtime adapter."""
    runtime_type: RuntimeType
    version: str
    supported_formats: list[ModelFormat]
    supports_gpu: bool
    supports_streaming: bool
    gpu_backend: str = "none"  # "cuda", "metal", "directml", "none"


class RuntimeAdapter(ABC):
    """
    Abstract base class for inference runtime adapters.
    
    Every runtime (llama.cpp, Transformers, ONNX) must implement this interface.
    This ensures the benchmark engine can work with any runtime uniformly.
    
    Lifecycle:
        adapter = SomeRuntimeAdapter()
        adapter.load_model(model_path, device="cuda")
        result = adapter.generate(prompt, config)
        adapter.unload_model()
    """
    
    @abstractmethod
    def runtime_info(self) -> RuntimeInfo:
        """Return metadata about this runtime adapter."""
        ...
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this runtime's dependencies are installed and functional."""
        ...
    
    @abstractmethod
    def load_model(
        self,
        model_path: str,
        device: str = "cpu",          # "cpu" or "cuda"
        gpu_layers: int = -1,          # -1 = auto, 0 = none, N = specific layers
        **kwargs,
    ) -> None:
        """
        Load a model from the given path.
        
        Args:
            model_path: Path to model file or HuggingFace model ID
            device: Target device ("cpu" or "cuda")
            gpu_layers: Number of layers to offload to GPU (-1 for auto)
        """
        ...
    
    @abstractmethod
    def unload_model(self) -> None:
        """Unload the current model and free resources."""
        ...
    
    @abstractmethod
    def is_model_loaded(self) -> bool:
        """Check if a model is currently loaded."""
        ...
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        config: Optional[GenerationConfig] = None,
    ) -> GenerationResult:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input text prompt
            config: Generation parameters (uses defaults if None)
        
        Returns:
            GenerationResult with output text, token counts, and timing
        """
        ...
    
    def generate_streaming(
        self,
        prompt: str,
        config: Optional[GenerationConfig] = None,
    ) -> Iterator[str]:
        """
        Generate text token-by-token (streaming).
        
        Default implementation falls back to non-streaming generate.
        Override in adapters that support streaming.
        """
        result = self.generate(prompt, config)
        yield result.output_text
    
    @abstractmethod
    def get_model_info(self) -> dict:
        """
        Return information about the currently loaded model.
        
        Returns dict with keys like: name, parameters, format, quantization, file_size_mb
        """
        ...
    
    def check_compatibility(self, model_path: str) -> tuple[bool, str]:
        """
        Check if a model file is compatible with this runtime.
        
        Returns:
            (is_compatible, reason_if_not)
        """
        return True, "Compatibility check not implemented"


# ─── Package exports ─────────────────────────────────────────────
__all__ = [
    "RuntimeAdapter", "RuntimeType", "ModelFormat",
    "GenerationConfig", "GenerationResult", "RuntimeInfo",
]
