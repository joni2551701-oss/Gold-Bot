"""
AI Layer — Runtime Trace (Phase 61.3: AI Intelligence Layer, TASK 8).

Combines a `request_id`'s matching `AIRequestLogEntry`
(`ai/audit/request_log.py`) and every `AIResponseLogEntry`
(`ai/audit/response_log.py`) sharing that `request_id` into one lookup
result -- neither log class is modified; this is a read-only join over
their existing `.all()` output, not a new storage mechanism. Reuses
`ai_layer.ai_engine.runtime.runtime_response.RuntimeResponse.request_id` (Phase 61.3
TASK 8's own addition) as the id a caller already has in hand after an
`AIService.ask()` call.
"""

from dataclasses import dataclass
from typing import List, Optional

from ai_layer.ai_service.audit.request_log import AIRequestLogEntry, RequestLog
from ai_layer.ai_service.audit.response_log import AIResponseLogEntry, ResponseLog


@dataclass(frozen=True)
class RuntimeTrace:
    """
    request: the matching AIRequestLogEntry, or None if request_id is
        unknown to this RequestLog (e.g. a cache-hit response, which
        was never logged as a request -- see RuntimeResponse.request_id's
        own docstring).
    responses: every AIResponseLogEntry sharing this request_id, oldest
        first -- ordinarily exactly one (a single provider attempt logs
        exactly one outcome), never more than one per attempt.
    """
    request_id: str
    request: Optional[AIRequestLogEntry]
    responses: List[AIResponseLogEntry]


def trace_request(request_log: RequestLog, response_log: ResponseLog, request_id: str) -> RuntimeTrace:
    """Never raises: an unknown request_id produces a RuntimeTrace with request=None and an empty responses list, not an error."""
    request_entry = next((entry for entry in request_log.all() if entry.request_id == request_id), None)
    responses = [entry for entry in response_log.all() if entry.request_id == request_id]
    return RuntimeTrace(request_id=request_id, request=request_entry, responses=responses)
