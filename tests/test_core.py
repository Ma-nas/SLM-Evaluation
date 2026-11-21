"""
SLM Evaluation Harness — Tests for core utilities
"""
import time
import tempfile
from pathlib import Path

import pytest

# ─── Timer Tests ─────────────────────────────────────────────────

from src.utils.timer import PerfTimer, TimerResult, TimerCollection


class TestPerfTimer:
    def test_context_manager(self):
        with PerfTimer("test") as t:
            time.sleep(0.01)  # 10ms
        result = t.result
        assert result.name == "test"
        assert result.elapsed_ms >= 5  # Allow some tolerance
        assert result.elapsed_ns > 0
        assert result.elapsed_s > 0

    def test_manual_start_stop(self):
        t = PerfTimer("manual")
        t.start()
        time.sleep(0.01)
        result = t.stop()
        assert result.elapsed_ms >= 5
    
    def test_mark_while_running(self):
        t = PerfTimer("running")
        t.start()
        time.sleep(0.01)
        elapsed = t.mark()
        assert elapsed >= 5
        assert t.is_running
        t.stop()
        assert not t.is_running

    def test_not_started_raises(self):
        t = PerfTimer("never_started")
        with pytest.raises(RuntimeError):
            t.stop()

    def test_result_before_stop_raises(self):
        t = PerfTimer("incomplete")
        t.start()
        with pytest.raises(RuntimeError):
            _ = t.result

    def test_timer_collection(self):
        tc = TimerCollection()
        with PerfTimer("a") as t1:
            time.sleep(0.005)
        tc.add(t1.result)
        with PerfTimer("b") as t2:
            time.sleep(0.005)
        tc.add(t2.result)
        
        summary = tc.summary()
        assert "a" in summary
        assert "b" in summary
        assert tc.get_ms("a") is not None
        assert tc.get_s("b") is not None
        assert tc.get_ms("nonexistent") is None


# ─── Database Tests ──────────────────────────────────────────────

from src.benchmarks.database import BenchmarkDB


class TestBenchmarkDB:
    @pytest.fixture
    def db(self, tmp_path):
        db_path = tmp_path / "test_benchmarks.db"
        db = BenchmarkDB(db_path=db_path)
        db.initialize()
        yield db
        db.close()

    def test_initialize_creates_tables(self, db):
        conn = db._get_conn()
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        table_names = [t["name"] for t in tables]
        assert "experiments" in table_names
        assert "runs" in table_names
        assert "metrics" in table_names
        assert "device_profiles" in table_names
        assert "compatibility" in table_names

    def test_insert_device_profile(self, db):
        profile = {
            "device_id": "test-device-001",
            "device_category": "laptop",
            "cpu": {"model": "Test CPU", "architecture": "x86_64", "cores_physical": 4, "cores_logical": 8},
            "ram_total_mb": 16000,
            "gpu": {"model": "Test GPU", "vram_total_mb": 4096, "driver_version": "1.0"},
            "os_name": "TestOS",
            "os_version": "1.0",
            "python_version": "3.14",
        }
        device_id = db.insert_device_profile(profile)
        assert device_id == "test-device-001"

    def test_full_benchmark_workflow(self, db):
        # Insert device
        db.insert_device_profile({"device_id": "dev-1", "device_category": "laptop"})
        
        # Create experiment
        exp_id = db.insert_experiment(
            model_id="test-model",
            runtime="test-runtime",
            device_id="dev-1",
            device_mode="cpu",
            model_name="Test Model",
            parameters_b=1.5,
            quantization="q4_k_m",
        )
        assert exp_id.startswith("exp-")
        
        # Insert warmup run
        warmup_id = db.insert_run(
            experiment_id=exp_id,
            run_number=1,
            prompt_text="Hello world",
            is_warmup=True,
            prompt_category="short_qa",
            output_text="Hi there!",
            prompt_tokens=3,
            output_tokens=5,
        )
        
        # Insert measurement run
        run_id = db.insert_run(
            experiment_id=exp_id,
            run_number=3,
            prompt_text="Hello world",
            is_warmup=False,
            prompt_category="short_qa",
            output_text="Hi there!",
            prompt_tokens=3,
            output_tokens=5,
        )
        
        # Insert metrics
        db.insert_metric(run_id, "ttft_ms", 42.5, "ms")
        db.insert_metric(run_id, "total_time_ms", 150.3, "ms")
        db.insert_metric(run_id, "tokens_per_second", 33.2, "tokens/s")
        db.insert_metric(run_id, "peak_ram_mb", 512.0, "MB")
        
        # Query results
        results = db.get_experiment_results(exp_id)
        assert results["model_id"] == "test-model"
        assert len(results["runs"]) == 2
        
        measurement_run = [r for r in results["runs"] if not r["is_warmup"]][0]
        assert "ttft_ms" in measurement_run["metrics"]
        assert measurement_run["metrics"]["ttft_ms"]["value"] == 42.5

    def test_insert_compatibility(self, db):
        db.insert_compatibility(
            model_id="phi3-mini",
            model_format="gguf",
            runtime="llama_cpp",
            device_mode="cuda",
            status="tested_ok",
            notes="Runs with 33 GPU layers"
        )
        # Insert duplicate should replace
        db.insert_compatibility(
            model_id="phi3-mini",
            model_format="gguf",
            runtime="llama_cpp",
            device_mode="cuda",
            status="tested_ok",
            notes="Updated: 33 GPU layers, stable"
        )
        
        conn = db._get_conn()
        rows = conn.execute("SELECT * FROM compatibility").fetchall()
        assert len(rows) == 1

    def test_get_all_experiments(self, db):
        db.insert_device_profile({"device_id": "d1", "device_category": "laptop"})
        db.insert_experiment(model_id="m1", runtime="r1", device_id="d1")
        db.insert_experiment(model_id="m2", runtime="r2", device_id="d1")
        
        exps = db.get_all_experiments()
        assert len(exps) == 2


# ─── Device Profiler Tests ───────────────────────────────────────

from src.devices.profiler import profile_device, DeviceProfile


class TestDeviceProfiler:
    def test_profile_returns_device_profile(self):
        profile = profile_device("laptop")
        assert isinstance(profile, DeviceProfile)
        assert profile.device_category == "laptop"
        assert profile.device_id != ""
        assert profile.os_name != "Unknown"
        assert profile.python_version != "Unknown"
    
    def test_cpu_detected(self):
        profile = profile_device()
        assert profile.cpu.model != "Unknown"
        assert profile.cpu.cores_logical > 0
    
    def test_to_json(self):
        profile = profile_device()
        json_str = profile.to_json()
        assert "device_id" in json_str
        assert "cpu" in json_str
    
    def test_summary(self):
        profile = profile_device()
        summary = profile.summary()
        assert "Device Profile" in summary
        assert "CPU" in summary


# ─── Model Registry Tests ───────────────────────────────────────

from src.models.registry import ModelRegistry, ModelEntry, ModelFamily, QuantizationType


class TestModelRegistry:
    def test_register_and_get(self):
        registry = ModelRegistry()
        entry = ModelEntry(
            model_id="test-model-q4",
            display_name="Test Model Q4",
            family=ModelFamily.PHI,
            parameters_billions=1.5,
            format="gguf",
            quantization=QuantizationType.Q4_K_M,
            compatible_runtimes=["llama_cpp"],
            min_vram_mb=1500,
        )
        registry.register(entry)
        
        assert registry.count == 1
        assert registry.get("test-model-q4") == entry
        assert registry.get("nonexistent") is None

    def test_list_by_family(self):
        registry = ModelRegistry()
        registry.register(ModelEntry("m1", "M1", ModelFamily.PHI, 1.0, "gguf"))
        registry.register(ModelEntry("m2", "M2", ModelFamily.GEMMA, 2.0, "gguf"))
        registry.register(ModelEntry("m3", "M3", ModelFamily.PHI, 3.0, "gguf"))
        
        phi_models = registry.list_by_family(ModelFamily.PHI)
        assert len(phi_models) == 2

    def test_list_compatible(self):
        registry = ModelRegistry()
        registry.register(ModelEntry(
            "m1", "M1", ModelFamily.PHI, 1.0, "gguf",
            compatible_runtimes=["llama_cpp"], min_vram_mb=1000
        ))
        registry.register(ModelEntry(
            "m2", "M2", ModelFamily.GEMMA, 2.0, "gguf",
            compatible_runtimes=["llama_cpp"], min_vram_mb=5000
        ))
        
        # With 4GB VRAM, only m1 fits
        fits = registry.list_compatible("llama_cpp", vram_mb=4096)
        assert len(fits) == 1
        assert fits[0].model_id == "m1"

    def test_fits_vram(self):
        entry = ModelEntry("m", "M", ModelFamily.PHI, 1.0, "gguf", min_vram_mb=2000)
        assert entry.fits_vram(4096)
        assert not entry.fits_vram(1000)
        
        cpu_only = ModelEntry("c", "C", ModelFamily.PHI, 1.0, "gguf", min_vram_mb=0)
        assert cpu_only.fits_vram(0)


# ─── Runtime Interface Tests ────────────────────────────────────

from src.runtimes.base import GenerationConfig, GenerationResult


class TestGenerationResult:
    def test_tokens_per_second(self):
        result = GenerationResult(
            prompt="test",
            output_text="hello world",
            output_tokens=10,
            prompt_tokens=5,
            total_generation_time_ms=1000.0,
        )
        assert result.tokens_per_second == 10.0

    def test_tokens_per_second_no_time(self):
        result = GenerationResult(
            prompt="test", output_text="hi", output_tokens=1, prompt_tokens=1,
        )
        assert result.tokens_per_second is None

    def test_time_per_output_token(self):
        result = GenerationResult(
            prompt="test",
            output_text="hello world tokens here and more",
            output_tokens=10,
            prompt_tokens=5,
            time_to_first_token_ms=50.0,
            total_generation_time_ms=500.0,
        )
        # (500 - 50) / (10 - 1) = 50ms
        assert result.time_per_output_token_ms == 50.0
