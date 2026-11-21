#!/usr/bin/env python
"""
Device Profiler Script — Run this to capture your hardware profile.
Outputs the profile to console and saves to results/device_profile.json
"""
import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.devices.profiler import profile_device
from src.config.settings import RESULTS_DIR


def main():
    print("Profiling device...\n")
    profile = profile_device("laptop")
    
    print(profile.summary())
    
    # Save to JSON
    output_path = RESULTS_DIR / "device_profile.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(profile.to_json(), encoding="utf-8")
    print(f"\nProfile saved to: {output_path}")


if __name__ == "__main__":
    main()
