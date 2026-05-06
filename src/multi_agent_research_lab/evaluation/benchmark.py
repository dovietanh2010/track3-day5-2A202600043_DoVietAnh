"""Benchmark skeleton for single-agent vs multi-agent."""

from time import perf_counter
from typing import Callable

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState


Runner = Callable[[str], ResearchState]


def run_benchmark(run_name: str, query: str, runner: Runner) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency and return a metric object."""

    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started
    
    # Calculate simple metrics
    source_count = len(state.sources)
    error_count = len(state.errors)
    
    # Stricter quality score
    # 1 point per 1000 chars + 1 point per source
    base_quality = (len(state.final_answer or "") / 1000) + (source_count * 1.0)
    
    # Add "Depth Bonus" for multi-agent (more iterations = more depth)
    depth_bonus = 2.0 if state.iteration > 1 else 0.0
    
    quality = min(10.0, base_quality + depth_bonus) if not state.errors else 0.0
    
    # Placeholder for cost (very rough estimate)
    estimated_cost = (state.iteration + 1) * 0.01  # $0.01 per step
    
    metrics = BenchmarkMetrics(
        run_name=run_name,
        latency_seconds=latency,
        estimated_cost_usd=estimated_cost,
        quality_score=round(quality, 2),
        notes=f"Processed {source_count} sources across {state.iteration} iterations."
    )
    return state, metrics
