"""
SLM Evaluation Harness — Resource Monitoring

Monitors RAM and VRAM usage during benchmark runs.
"""
from __future__ import annotations

import os
import subprocess
import threading
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class MemorySnapshot:
    """A single memory measurement."""
    timestamp_ns: int
    ram_used_mb: float
    ram_total_mb: float
    vram_used_mb: Optional[float] = None
    vram_total_mb: Optional[float] = None


@dataclass
class MemoryStats:
    """Aggregated memory statistics from a monitoring session."""
    peak_ram_mb: float = 0.0
    baseline_ram_mb: float = 0.0
    delta_ram_mb: float = 0.0
    peak_vram_mb: Optional[float] = None
    baseline_vram_mb: Optional[float] = None
    delta_vram_mb: Optional[float] = None
    sample_count: int = 0


def get_process_ram_mb(pid: Optional[int] = None) -> float:
    """Get RAM usage of the current process in MB."""
    try:
        import psutil
        p = psutil.Process(pid or os.getpid())
        return p.memory_info().rss / (1024 * 1024)
    except ImportError:
        return 0.0


def get_system_ram_mb() -> tuple[float, float]:
    """Get (used, total) system RAM in MB."""
    try:
        import psutil
        mem = psutil.virtual_memory()
        return mem.used / (1024 * 1024), mem.total / (1024 * 1024)
    except ImportError:
        return 0.0, 0.0


def get_gpu_vram_mb() -> tuple[Optional[float], Optional[float]]:
    """Get (used, total) GPU VRAM in MB using nvidia-smi."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split(",")
            if len(parts) >= 2:
                return float(parts[0].strip()), float(parts[1].strip())
    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
        pass
    return None, None


class ResourceMonitor:
    """
    Background thread that samples RAM and VRAM at regular intervals.
    
    Usage:
        monitor = ResourceMonitor(interval_ms=100)
        monitor.start()
        # ... run benchmark ...
        stats = monitor.stop()
        print(f"Peak RAM: {stats.peak_ram_mb:.1f} MB")
    """
    
    def __init__(self, interval_ms: int = 200, pid: Optional[int] = None) -> None:
        self.interval_ms = interval_ms
        self.pid = pid
        self._snapshots: list[MemorySnapshot] = []
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
    
    def start(self) -> None:
        """Start background monitoring."""
        self._snapshots.clear()
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._sample_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> MemoryStats:
        """Stop monitoring and return aggregated statistics."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        return self._compute_stats()
    
    def _sample_loop(self) -> None:
        interval_s = self.interval_ms / 1000
        while not self._stop_event.is_set():
            snapshot = MemorySnapshot(
                timestamp_ns=time.perf_counter_ns(),
                ram_used_mb=get_process_ram_mb(self.pid),
                ram_total_mb=0.0,
            )
            vram_used, vram_total = get_gpu_vram_mb()
            snapshot.vram_used_mb = vram_used
            snapshot.vram_total_mb = vram_total
            self._snapshots.append(snapshot)
            self._stop_event.wait(interval_s)
    
    def _compute_stats(self) -> MemoryStats:
        if not self._snapshots:
            return MemoryStats()
        
        ram_values = [s.ram_used_mb for s in self._snapshots if s.ram_used_mb > 0]
        vram_values = [s.vram_used_mb for s in self._snapshots if s.vram_used_mb is not None]
        
        stats = MemoryStats(sample_count=len(self._snapshots))
        
        if ram_values:
            stats.peak_ram_mb = max(ram_values)
            stats.baseline_ram_mb = ram_values[0]
            stats.delta_ram_mb = stats.peak_ram_mb - stats.baseline_ram_mb
        
        if vram_values:
            stats.peak_vram_mb = max(vram_values)
            stats.baseline_vram_mb = vram_values[0]
            stats.delta_vram_mb = stats.peak_vram_mb - stats.baseline_vram_mb
        
        return stats


__all__ = ["ResourceMonitor", "MemoryStats", "MemorySnapshot",
           "get_process_ram_mb", "get_gpu_vram_mb", "get_system_ram_mb"]
