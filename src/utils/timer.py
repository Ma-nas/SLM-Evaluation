"""
SLM Evaluation Harness — High-Precision Timer Utility
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TimerResult:
    """Stores the result of a timing measurement."""
    name: str
    start_ns: int
    end_ns: int

    @property
    def elapsed_ns(self) -> int:
        return self.end_ns - self.start_ns

    @property
    def elapsed_ms(self) -> float:
        return self.elapsed_ns / 1_000_000

    @property
    def elapsed_s(self) -> float:
        return self.elapsed_ns / 1_000_000_000

    def __repr__(self) -> str:
        return f"TimerResult(name={self.name!r}, elapsed={self.elapsed_ms:.2f}ms)"


class PerfTimer:
    """
    High-precision timer using time.perf_counter_ns().
    
    Usage as context manager:
        with PerfTimer("model_load") as t:
            model = load_model()
        print(t.result.elapsed_ms)
    
    Usage as manual timer:
        t = PerfTimer("inference")
        t.start()
        # ... do work ...
        t.stop()
        print(t.result.elapsed_s)
    """

    def __init__(self, name: str = "unnamed") -> None:
        self.name = name
        self._start_ns: Optional[int] = None
        self._end_ns: Optional[int] = None

    def start(self) -> "PerfTimer":
        """Start the timer. Returns self for chaining."""
        self._start_ns = time.perf_counter_ns()
        self._end_ns = None
        return self

    def stop(self) -> TimerResult:
        """Stop the timer and return the result."""
        if self._start_ns is None:
            raise RuntimeError(f"Timer '{self.name}' was never started")
        self._end_ns = time.perf_counter_ns()
        return self.result

    def mark(self) -> float:
        """Return elapsed milliseconds without stopping the timer."""
        if self._start_ns is None:
            raise RuntimeError(f"Timer '{self.name}' was never started")
        now = time.perf_counter_ns()
        return (now - self._start_ns) / 1_000_000

    @property
    def result(self) -> TimerResult:
        """Get the timer result. Timer must be stopped first."""
        if self._start_ns is None or self._end_ns is None:
            raise RuntimeError(f"Timer '{self.name}' not complete (start/stop both required)")
        return TimerResult(
            name=self.name,
            start_ns=self._start_ns,
            end_ns=self._end_ns,
        )

    @property
    def is_running(self) -> bool:
        return self._start_ns is not None and self._end_ns is None

    def __enter__(self) -> "PerfTimer":
        self.start()
        return self

    def __exit__(self, *exc) -> None:
        self.stop()

    def __repr__(self) -> str:
        if self._end_ns is not None:
            return f"PerfTimer(name={self.name!r}, elapsed={self.result.elapsed_ms:.2f}ms)"
        elif self._start_ns is not None:
            return f"PerfTimer(name={self.name!r}, running, {self.mark():.2f}ms elapsed)"
        return f"PerfTimer(name={self.name!r}, not started)"


@dataclass
class TimerCollection:
    """Collect multiple named timers for a benchmark run."""
    timers: dict[str, TimerResult] = field(default_factory=dict)

    def add(self, result: TimerResult) -> None:
        self.timers[result.name] = result

    def get_ms(self, name: str) -> Optional[float]:
        r = self.timers.get(name)
        return r.elapsed_ms if r else None

    def get_s(self, name: str) -> Optional[float]:
        r = self.timers.get(name)
        return r.elapsed_s if r else None

    def summary(self) -> dict[str, float]:
        """Return all timings in milliseconds."""
        return {name: r.elapsed_ms for name, r in self.timers.items()}
