-- SLM Evaluation Harness — SQLite Schema
-- Stores benchmark experiments, runs, and metrics

-- Device profiles recorded during benchmarking
CREATE TABLE IF NOT EXISTS device_profiles (
    device_id       TEXT PRIMARY KEY,
    device_category TEXT NOT NULL,
    cpu_model       TEXT,
    cpu_arch        TEXT,
    cpu_cores       INTEGER,
    cpu_threads     INTEGER,
    ram_total_mb    INTEGER,
    gpu_model       TEXT,
    gpu_vram_mb     INTEGER,
    gpu_driver      TEXT,
    os_name         TEXT,
    os_version      TEXT,
    python_version  TEXT,
    profile_json    TEXT,  -- Full JSON profile for extensibility
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Experiment = one complete benchmark session (model × runtime × device × quantization)
CREATE TABLE IF NOT EXISTS experiments (
    experiment_id   TEXT PRIMARY KEY,
    timestamp       TEXT NOT NULL DEFAULT (datetime('now')),
    model_id        TEXT NOT NULL,
    model_name      TEXT,
    model_family    TEXT,
    parameters_b    REAL,
    quantization    TEXT,
    model_format    TEXT,
    runtime         TEXT NOT NULL,
    runtime_version TEXT,
    device_id       TEXT REFERENCES device_profiles(device_id),
    device_mode     TEXT NOT NULL DEFAULT 'cpu',  -- 'cpu' or 'cuda'
    gpu_layers      INTEGER DEFAULT 0,
    config_json     TEXT,  -- Full generation config as JSON
    notes           TEXT,
    status          TEXT NOT NULL DEFAULT 'pending'  -- pending, running, completed, failed
);

-- Individual benchmark runs within an experiment
CREATE TABLE IF NOT EXISTS runs (
    run_id          TEXT PRIMARY KEY,
    experiment_id   TEXT NOT NULL REFERENCES experiments(experiment_id),
    run_number      INTEGER NOT NULL,
    is_warmup       INTEGER NOT NULL DEFAULT 0,  -- 1 = warmup (excluded from stats)
    prompt_category TEXT,
    prompt_text     TEXT NOT NULL,
    output_text     TEXT,
    prompt_tokens   INTEGER,
    output_tokens   INTEGER,
    started_at      TEXT NOT NULL DEFAULT (datetime('now')),
    completed_at    TEXT,
    success         INTEGER NOT NULL DEFAULT 1,
    error_message   TEXT
);

-- Metric measurements attached to individual runs
CREATE TABLE IF NOT EXISTS metrics (
    metric_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          TEXT NOT NULL REFERENCES runs(run_id),
    metric_name     TEXT NOT NULL,
    metric_value    REAL NOT NULL,
    metric_unit     TEXT NOT NULL,
    UNIQUE(run_id, metric_name)
);

-- Compatibility matrix: model × format × runtime × device
CREATE TABLE IF NOT EXISTS compatibility (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id        TEXT NOT NULL,
    model_format    TEXT NOT NULL,
    runtime         TEXT NOT NULL,
    device_mode     TEXT NOT NULL,  -- 'cpu' or 'cuda'
    status          TEXT NOT NULL,  -- 'supported', 'unsupported', 'tested_ok', 'tested_fail', 'not_tested', 'requires_conversion'
    error_details   TEXT,
    tested_at       TEXT,
    notes           TEXT,
    UNIQUE(model_id, model_format, runtime, device_mode)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_runs_experiment ON runs(experiment_id);
CREATE INDEX IF NOT EXISTS idx_metrics_run ON metrics(run_id);
CREATE INDEX IF NOT EXISTS idx_experiments_model ON experiments(model_id);
CREATE INDEX IF NOT EXISTS idx_experiments_runtime ON experiments(runtime);
