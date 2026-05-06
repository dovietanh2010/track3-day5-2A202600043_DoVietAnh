"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to a detailed markdown report."""

    lines = [
        "# Benchmark Performance Report",
        "",
        "This report provides a quantitative comparison between different research agent configurations.",
        "",
        "## Detailed Metrics",
        "",
        "| Run Name | Latency (s) | Est. Cost (USD) | Quality Score | Observations |",
        "| :--- | ---: | ---: | ---: | :--- |"
    ]
    
    for item in metrics:
        cost = f"${item.estimated_cost_usd:.4f}" if item.estimated_cost_usd is not None else "N/A"
        quality = f"{item.quality_score:.1f}/10" if item.quality_score is not None else "N/A"
        lines.append(f"| **{item.run_name}** | {item.latency_seconds:.2f}s | {cost} | {quality} | {item.notes} |")
    
    lines.append("")
    lines.append("## Summary Analysis")
    
    if len(metrics) >= 2:
        # Simple comparison if we have at least 2 runs
        m1, m2 = metrics[0], metrics[1]
        latency_diff = abs(m1.latency_seconds - m2.latency_seconds)
        faster = m1.run_name if m1.latency_seconds < m2.latency_seconds else m2.run_name
        
        lines.append(f"- **Efficiency**: `{faster}` was faster by {latency_diff:.2f} seconds.")
        
        if m1.quality_score is not None and m2.quality_score is not None:
            if m1.quality_score != m2.quality_score:
                higher = m1.run_name if m1.quality_score > m2.quality_score else m2.run_name
                lines.append(f"- **Quality**: `{higher}` provided a higher quality output based on internal metrics.")
            else:
                lines.append("- **Quality**: Both configurations provided similar quality levels.")

    lines.append("")
    lines.append("---")
    lines.append("*Report generated automatically by Multi-Agent Research Lab Evaluation Suite.*")
    
    return "\n".join(lines) + "\n"
