import os
from collections.abc import Iterator
from contextlib import contextmanager
from time import perf_counter
from typing import Any

from langsmith import traceable


@contextmanager
def trace_span(name: str, attributes: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
    """Span context that records local duration and marks the scope for LangSmith."""
    
    started = perf_counter()
    span: dict[str, Any] = {"name": name, "attributes": attributes or {}, "duration_seconds": None}
    
    # We use traceable here to ensure this span is recorded if tracing is enabled
    @traceable(name=name)
    def _execute():
        pass
        
    _execute()
    
    try:
        yield span
    finally:
        span["duration_seconds"] = perf_counter() - started
