"""
SLM Evaluation Harness — Central Configuration
"""
from pathlib import Path

# ─── Project Paths ───────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
CONFIGS_DIR = PROJECT_ROOT / "configs"
RESULTS_DIR = PROJECT_ROOT / "results"
RAW_RESULTS_DIR = RESULTS_DIR / "raw"
PROCESSED_RESULTS_DIR = RESULTS_DIR / "processed"
FIGURES_DIR = RESULTS_DIR / "figures"
DB_PATH = RAW_RESULTS_DIR / "benchmarks.db"
MODELS_CACHE_DIR = PROJECT_ROOT / "models_cache"

# ─── Generation Parameters (defaults) ───────────────────────────
DEFAULT_MAX_TOKENS: int = 256
DEFAULT_TEMPERATURE: float = 0.0
DEFAULT_TOP_P: float = 1.0
DEFAULT_REPEAT_PENALTY: float = 1.0

# ─── Benchmark Settings ─────────────────────────────────────────
NUM_WARMUP_RUNS: int = 2
NUM_MEASUREMENT_RUNS: int = 5
TOTAL_RUNS: int = NUM_WARMUP_RUNS + NUM_MEASUREMENT_RUNS

# ─── Logging ─────────────────────────────────────────────────────
LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

# ─── Ensure directories exist ────────────────────────────────────
def ensure_dirs() -> None:
    """Create required project directories if they don't exist."""
    for d in [RAW_RESULTS_DIR, PROCESSED_RESULTS_DIR, FIGURES_DIR, MODELS_CACHE_DIR]:
        d.mkdir(parents=True, exist_ok=True)
