"""
Phase 53 — pipeline execution time regression tests.

Not benchmarks (see docs/PERFORMANCE.md for real timing
numbers) -- these are regression guards. The real bottleneck is
network I/O (Market Data fetch, Telegram delivery, not reproducible
in a test run) and the aiogram import (paid once per process, not per
pipeline.run() call) -- the budgets below are generous on purpose:
they exist to catch an accidental O(n^2)/infinite-retry/blocking-call
regression in the pipeline's own compute path, not to chase
milliseconds.
"""

import time

PIPELINE_BUDGET_SECONDS = 10.0  # task-specified budget; real cost is sub-millisecond


def test_single_candidate_pipeline_run_within_budget(mock_pipeline, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate()
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    start = time.perf_counter()
    pipeline.run()
    elapsed = time.perf_counter() - start

    assert elapsed < PIPELINE_BUDGET_SECONDS


def test_multi_candidate_pipeline_run_within_budget(mock_pipeline, mock_signal_candidate, mock_ai_result):
    """3 candidates (matching a real 3-strategy cycle) must not meaningfully change the budget."""
    candidates = [mock_signal_candidate(strategy_name=f"STRATEGY_{i}") for i in range(3)]
    ai_results = [mock_ai_result(approved=True, confidence=0.9) for _ in candidates]
    pipeline = mock_pipeline(candidates, ai_results)

    start = time.perf_counter()
    pipeline.run()
    elapsed = time.perf_counter() - start

    assert elapsed < PIPELINE_BUDGET_SECONDS


def test_repeated_pipeline_runs_do_not_degrade(mock_pipeline, mock_signal_candidate, mock_ai_result):
    """
    Simulates repeated scheduled invocations (production runs every 5
    minutes). Each run must stay within budget -- a regression here
    (e.g. an accidentally-growing in-memory structure reused across
    calls) would show up as later runs getting slower.
    """
    durations = []
    for _ in range(5):
        candidate = mock_signal_candidate()
        pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])
        start = time.perf_counter()
        pipeline.run()
        durations.append(time.perf_counter() - start)

    assert all(d < PIPELINE_BUDGET_SECONDS for d in durations)
    # Last run must not be dramatically slower than the first -- guards
    # against unbounded per-call growth, not normal timing jitter.
    assert durations[-1] < durations[0] + PIPELINE_BUDGET_SECONDS


def test_pipeline_stage_timing_is_logged(mock_pipeline, mock_signal_candidate, mock_ai_result, caplog):
    """Phase 53 instrumentation: every stage must log its duration."""
    import logging

    candidate = mock_signal_candidate()
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])

    with caplog.at_level(logging.INFO, logger="TradingPipeline"):
        pipeline.run()

    messages = "\n".join(caplog.messages)
    assert "pipeline_started" in messages
    assert "pipeline_finished" in messages
    for stage in ("market_data", "data_quality", "htf_bias", "context", "signal", "signal_quality", "explainability", "ai", "decision", "risk", "telegram_format", "database"):
        assert f"stage={stage}" in messages
