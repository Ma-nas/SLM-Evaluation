"""
SLM Evaluation Harness — Database Manager

SQLite database for storing benchmark experiments, runs, and metrics.
"""
from __future__ import annotations

import sqlite3
import json
import uuid
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone

from src.config.settings import DB_PATH, ensure_dirs


class BenchmarkDB:
    """
    Manager for the benchmark results SQLite database.
    
    Usage:
        db = BenchmarkDB()
        db.initialize()
        
        exp_id = db.insert_experiment(model_id="phi3-mini-q4", ...)
        run_id = db.insert_run(experiment_id=exp_id, ...)
        db.insert_metric(run_id=run_id, name="ttft_ms", value=45.2, unit="ms")
        
        results = db.get_experiment_results(exp_id)
        db.close()
    """
    
    def __init__(self, db_path: Optional[Path] = None) -> None:
        self.db_path = db_path or DB_PATH
        self._conn: Optional[sqlite3.Connection] = None
    
    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            ensure_dirs()
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
        return self._conn
    
    def initialize(self) -> None:
        """Create database tables from schema.sql."""
        schema_path = Path(__file__).parent / "schema.sql"
        schema_sql = schema_path.read_text(encoding="utf-8")
        conn = self._get_conn()
        conn.executescript(schema_sql)
        conn.commit()
    
    def insert_device_profile(self, profile_dict: dict) -> str:
        """Insert or update a device profile. Returns device_id."""
        conn = self._get_conn()
        device_id = profile_dict.get("device_id", f"dev-{uuid.uuid4().hex[:8]}")
        conn.execute("""
            INSERT OR REPLACE INTO device_profiles 
            (device_id, device_category, cpu_model, cpu_arch, cpu_cores, cpu_threads,
             ram_total_mb, gpu_model, gpu_vram_mb, gpu_driver, os_name, os_version,
             python_version, profile_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            device_id,
            profile_dict.get("device_category", "unknown"),
            profile_dict.get("cpu", {}).get("model", ""),
            profile_dict.get("cpu", {}).get("architecture", ""),
            profile_dict.get("cpu", {}).get("cores_physical", 0),
            profile_dict.get("cpu", {}).get("cores_logical", 0),
            profile_dict.get("ram_total_mb", 0),
            profile_dict.get("gpu", {}).get("model", ""),
            profile_dict.get("gpu", {}).get("vram_total_mb", 0),
            profile_dict.get("gpu", {}).get("driver_version", ""),
            profile_dict.get("os_name", ""),
            profile_dict.get("os_version", ""),
            profile_dict.get("python_version", ""),
            json.dumps(profile_dict),
        ))
        conn.commit()
        return device_id
    
    def insert_experiment(
        self,
        model_id: str,
        runtime: str,
        device_id: str,
        device_mode: str = "cpu",
        model_name: str = "",
        model_family: str = "",
        parameters_b: float = 0.0,
        quantization: str = "",
        model_format: str = "",
        runtime_version: str = "",
        gpu_layers: int = 0,
        config_json: str = "",
        notes: str = "",
    ) -> str:
        """Insert a new experiment. Returns experiment_id."""
        conn = self._get_conn()
        experiment_id = f"exp-{uuid.uuid4().hex[:12]}"
        conn.execute("""
            INSERT INTO experiments 
            (experiment_id, model_id, runtime, device_id, device_mode,
             model_name, model_family, parameters_b, quantization, model_format,
             runtime_version, gpu_layers, config_json, notes, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'running')
        """, (
            experiment_id, model_id, runtime, device_id, device_mode,
            model_name, model_family, parameters_b, quantization, model_format,
            runtime_version, gpu_layers, config_json, notes,
        ))
        conn.commit()
        return experiment_id
    
    def insert_run(
        self,
        experiment_id: str,
        run_number: int,
        prompt_text: str,
        is_warmup: bool = False,
        prompt_category: str = "",
        output_text: str = "",
        prompt_tokens: int = 0,
        output_tokens: int = 0,
        success: bool = True,
        error_message: str = "",
    ) -> str:
        """Insert a benchmark run. Returns run_id."""
        conn = self._get_conn()
        run_id = f"run-{uuid.uuid4().hex[:12]}"
        conn.execute("""
            INSERT INTO runs 
            (run_id, experiment_id, run_number, is_warmup, prompt_category,
             prompt_text, output_text, prompt_tokens, output_tokens,
             success, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_id, experiment_id, run_number, int(is_warmup), prompt_category,
            prompt_text, output_text, prompt_tokens, output_tokens,
            int(success), error_message,
        ))
        conn.commit()
        return run_id
    
    def insert_metric(
        self,
        run_id: str,
        name: str,
        value: float,
        unit: str,
    ) -> None:
        """Insert a metric measurement for a run."""
        conn = self._get_conn()
        conn.execute("""
            INSERT OR REPLACE INTO metrics (run_id, metric_name, metric_value, metric_unit)
            VALUES (?, ?, ?, ?)
        """, (run_id, name, value, unit))
        conn.commit()
    
    def update_experiment_status(self, experiment_id: str, status: str) -> None:
        """Update experiment status (pending, running, completed, failed)."""
        conn = self._get_conn()
        conn.execute(
            "UPDATE experiments SET status = ? WHERE experiment_id = ?",
            (status, experiment_id),
        )
        conn.commit()
    
    def get_experiment_results(self, experiment_id: str) -> dict:
        """Get all runs and metrics for an experiment."""
        conn = self._get_conn()
        
        exp = conn.execute(
            "SELECT * FROM experiments WHERE experiment_id = ?",
            (experiment_id,),
        ).fetchone()
        
        if not exp:
            return {}
        
        runs = conn.execute(
            "SELECT * FROM runs WHERE experiment_id = ? ORDER BY run_number",
            (experiment_id,),
        ).fetchall()
        
        result = dict(exp)
        result["runs"] = []
        for run in runs:
            run_dict = dict(run)
            metrics = conn.execute(
                "SELECT metric_name, metric_value, metric_unit FROM metrics WHERE run_id = ?",
                (run["run_id"],),
            ).fetchall()
            run_dict["metrics"] = {m["metric_name"]: {"value": m["metric_value"], "unit": m["metric_unit"]} for m in metrics}
            result["runs"].append(run_dict)
        
        return result
    
    def get_all_experiments(self) -> list[dict]:
        """List all experiments with summary info."""
        conn = self._get_conn()
        rows = conn.execute("""
            SELECT e.*, COUNT(r.run_id) as total_runs,
                   SUM(CASE WHEN r.is_warmup = 0 THEN 1 ELSE 0 END) as measurement_runs
            FROM experiments e
            LEFT JOIN runs r ON e.experiment_id = r.experiment_id
            GROUP BY e.experiment_id
            ORDER BY e.timestamp DESC
        """).fetchall()
        return [dict(r) for r in rows]
    
    def insert_compatibility(
        self,
        model_id: str,
        model_format: str,
        runtime: str,
        device_mode: str,
        status: str,
        error_details: str = "",
        notes: str = "",
    ) -> None:
        """Record a compatibility test result."""
        conn = self._get_conn()
        conn.execute("""
            INSERT OR REPLACE INTO compatibility
            (model_id, model_format, runtime, device_mode, status, error_details, tested_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)
        """, (model_id, model_format, runtime, device_mode, status, error_details, notes))
        conn.commit()
    
    def close(self) -> None:
        """Close the database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
    
    def __enter__(self) -> "BenchmarkDB":
        self.initialize()
        return self
    
    def __exit__(self, *exc) -> None:
        self.close()


# ─── Package exports ─────────────────────────────────────────────
__all__ = ["BenchmarkDB"]
