"""
SLM Evaluation Harness — Device Profiler

Automatically detects and reports hardware and software specifications
for the current machine, following the Device-Class Specification schema.
"""
from __future__ import annotations

import os
import platform
import subprocess
import json
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime, timezone


@dataclass
class CPUInfo:
    model: str = "Unknown"
    architecture: str = "Unknown"
    cores_physical: int = 0
    cores_logical: int = 0
    max_clock_mhz: int = 0


@dataclass
class GPUInfo:
    model: str = "None"
    architecture: str = "Unknown"
    vram_total_mb: int = 0
    driver_version: str = "Unknown"
    cuda_version: str = "Unknown"
    compute_capability: str = "Unknown"


@dataclass
class DeviceProfile:
    """Complete device specification following the project schema."""
    device_id: str = ""
    device_category: str = "unknown"  # desktop, laptop, mobile, edge, server, cloud
    timestamp: str = ""
    
    # CPU
    cpu: CPUInfo = field(default_factory=CPUInfo)
    
    # Memory
    ram_total_mb: int = 0
    
    # GPU
    gpu: GPUInfo = field(default_factory=GPUInfo)
    has_gpu: bool = False
    
    # OS
    os_name: str = "Unknown"
    os_version: str = "Unknown"
    os_architecture: str = "Unknown"
    
    # Python
    python_version: str = "Unknown"
    
    # Limitations
    measurement_limitations: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
    
    def summary(self) -> str:
        lines = [
            "═══ Device Profile ═══",
            f"  ID:       {self.device_id}",
            f"  Category: {self.device_category}",
            f"  OS:       {self.os_name} {self.os_version} ({self.os_architecture})",
            f"  CPU:      {self.cpu.model}",
            f"            {self.cpu.cores_physical}C/{self.cpu.cores_logical}T @ {self.cpu.max_clock_mhz} MHz",
            f"  RAM:      {self.ram_total_mb} MB ({self.ram_total_mb / 1024:.1f} GB)",
        ]
        if self.has_gpu:
            lines.extend([
                f"  GPU:      {self.gpu.model}",
                f"  VRAM:     {self.gpu.vram_total_mb} MB ({self.gpu.vram_total_mb / 1024:.1f} GB)",
                f"  Driver:   {self.gpu.driver_version}",
                f"  CUDA:     {self.gpu.cuda_version}",
            ])
        else:
            lines.append("  GPU:      None detected")
        
        if self.measurement_limitations:
            lines.append("  Limitations:")
            for lim in self.measurement_limitations:
                lines.append(f"    - {lim}")
        
        lines.append("═" * 24)
        return "\n".join(lines)


def _run_cmd(cmd: list[str]) -> Optional[str]:
    """Run a command and return stdout, or None on failure."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None


def _detect_cpu() -> CPUInfo:
    """Detect CPU information using platform and OS-specific methods."""
    info = CPUInfo()
    info.architecture = platform.machine()
    
    # Get CPU name
    if os.name == 'nt':
        cpu_name = os.environ.get("PROCESSOR_IDENTIFIER", "")
        # Try PowerShell for better name
        ps_result = _run_cmd([
            "powershell", "-NoProfile", "-Command",
            "(Get-CimInstance Win32_Processor).Name"
        ])
        if ps_result:
            info.model = ps_result.strip()
        elif cpu_name:
            info.model = cpu_name
            
        # Core counts
        ps_result = _run_cmd([
            "powershell", "-NoProfile", "-Command",
            "$p = Get-CimInstance Win32_Processor; "
            "\"$($p.NumberOfCores),$($p.NumberOfLogicalProcessors),$($p.MaxClockSpeed)\""
        ])
        if ps_result:
            parts = ps_result.strip().split(",")
            if len(parts) >= 3:
                info.cores_physical = int(parts[0])
                info.cores_logical = int(parts[1])
                info.max_clock_mhz = int(parts[2])
    else:
        # Linux/macOS
        info.model = platform.processor() or "Unknown"
        cpu_count = os.cpu_count()
        if cpu_count:
            info.cores_logical = cpu_count
            # Try to get physical cores
            try:
                import psutil
                info.cores_physical = psutil.cpu_count(logical=False) or cpu_count
            except ImportError:
                info.cores_physical = cpu_count
    
    return info


def _detect_ram() -> int:
    """Detect total RAM in MB."""
    try:
        import psutil
        return int(psutil.virtual_memory().total / (1024 * 1024))
    except ImportError:
        pass
    
    if os.name == 'nt':
        result = _run_cmd([
            "powershell", "-NoProfile", "-Command",
            "[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1MB)"
        ])
        if result:
            return int(result.strip())
    
    return 0


def _detect_gpu() -> tuple[bool, GPUInfo]:
    """Detect NVIDIA GPU using nvidia-smi."""
    info = GPUInfo()
    
    result = _run_cmd([
        "nvidia-smi",
        "--query-gpu=name,memory.total,driver_version",
        "--format=csv,noheader,nounits"
    ])
    
    if result is None:
        return False, info
    
    parts = [p.strip() for p in result.split(",")]
    if len(parts) >= 3:
        info.model = parts[0]
        try:
            info.vram_total_mb = int(float(parts[1]))
        except ValueError:
            pass
        info.driver_version = parts[2]
    
    # Try to get CUDA version
    cuda_result = _run_cmd(["nvidia-smi", "--query-gpu=compute_cap", "--format=csv,noheader"])
    if cuda_result:
        info.compute_capability = cuda_result.strip()
    
    return True, info


def profile_device(device_category: str = "laptop") -> DeviceProfile:
    """
    Profile the current device and return a DeviceProfile.
    
    Args:
        device_category: One of 'desktop', 'laptop', 'mobile', 'edge', 'server', 'cloud'
    
    Returns:
        DeviceProfile with detected hardware and software information.
    """
    profile = DeviceProfile()
    profile.timestamp = datetime.now(timezone.utc).isoformat()
    profile.device_category = device_category
    
    # OS
    profile.os_name = f"{platform.system()} {platform.release()}"
    profile.os_version = platform.version()
    profile.os_architecture = platform.machine()
    
    # Python
    profile.python_version = platform.python_version()
    
    # CPU
    profile.cpu = _detect_cpu()
    
    # RAM
    profile.ram_total_mb = _detect_ram()
    
    # GPU
    profile.has_gpu, profile.gpu = _detect_gpu()
    
    # Device ID (hash-based, anonymized)
    id_parts = f"{profile.cpu.model}-{profile.ram_total_mb}-{profile.gpu.model}"
    profile.device_id = f"dev-{hash(id_parts) & 0xFFFFFFFF:08x}"
    
    # Known limitations
    limitations = []
    if device_category == "laptop":
        limitations.append("Thermal throttling may affect sustained benchmark performance")
        limitations.append("Battery vs AC power state affects CPU/GPU boost clocks")
    if profile.has_gpu and profile.gpu.vram_total_mb <= 4096:
        limitations.append(f"Limited VRAM ({profile.gpu.vram_total_mb} MB) constrains model sizes")
    if platform.system() == "Windows":
        limitations.append("Background OS processes may affect measurement precision")
    limitations.append("Power consumption measurement not available without specialized hardware")
    profile.measurement_limitations = limitations
    
    return profile


# ─── Package init ────────────────────────────────────────────────
__all__ = ["DeviceProfile", "CPUInfo", "GPUInfo", "profile_device"]
