"""FLOW-017 Personal AI Core -- Memory-First Production Wiring tests.

Unit + Integration + End-to-End for the memory-first orchestrator and
its live Telegram consumer (`/ask`). The External AI API is exercised
through an injected fake ConversationEngine so the tests are
deterministic and never touch a real provider.
"""

import asyncio
from types import SimpleNamespace

from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.knowledge_ai.memory_manager.memory_runtime import MemoryRuntime
from ai_layer.knowledge_ai.memory_manager.models import MemoryType, MemoryScope
from ai_layer.personal_ai.interaction_manager.memory_first_query import (
    MemoryAnswer,
    PersonalAIResult,
    answer_question,
    personal_ai_memory_key,
    MEMORY_KEY_PREFIX,
)
from core_layer.configuration.feature_flags import FeatureFlags

FLAGS_ON = FeatureFlags(enable_personal_ai=True)


class FakeEngine:
    """Stand-in for ConversationEngine -- counts calls so a memory hit
    can be proven to skip the API."""

    def __init__(self, content="XAUUSD is spot gold priced in US dollars.", accepted=True):
        self.calls = 0
        self._content = content
        self._accepted = accepted

    def start_session(self, telegram_id):
        return SimpleNamespace(session_id="sess-1")

    def ask(self, session_id, message, ai_context, role, telegram_id=None):
        self.calls += 1
        resp = SimpleNamespace(
            accepted=self._accepted, content=self._content if self._accepted else None,
            reason="ok" if self._accepted else "provider offline", metadata={"confidence": 0.9},
        )
        return SimpleNamespace(session_id=session_id, response=resp)


# --- Unit -----------------------------------------------------------------
def test_memory_key_is_deterministic_and_normalized():
    a = personal_ai_memory_key("What is XAUUSD?")
    b = personal_ai_memory_key("  what   IS   xauusd? ")
    assert a == b
    assert a.startswith(MEMORY_KEY_PREFIX)
    assert personal_ai_memory_key("different") != a


def test_memory_answer_contract_fields():
    ma = MemoryAnswer(question="q", answer="a", topic="t")
    for field_name in ("question", "answer", "topic", "tags", "timestamp", "source", "confidence", "version"):
        assert hasattr(ma, field_name)
    assert ma.version == "1.0"


def test_empty_question_is_failed():
    r = answer_question("   ", AIRole.OWNER, flags=FLAGS_ON, conversation_engine=FakeEngine(), memory_runtime=MemoryRuntime())
    assert isinstance(r, PersonalAIResult)
    assert r.accepted is False and r.source == "failed"


def test_gate_denies_when_flag_off_even_for_owner():
    eng = FakeEngine()
    r = answer_question("hi", AIRole.OWNER, conversation_engine=eng, memory_runtime=MemoryRuntime())  # DEFAULT_FLAGS: off
    assert r.source == "denied" and r.accepted is False
    assert eng.calls == 0  # API never touched on a denied role


def test_gate_denies_admin_even_when_flag_on():
    eng = FakeEngine()
    r = answer_question("hi", AIRole.ADMIN, flags=FLAGS_ON, conversation_engine=eng, memory_runtime=MemoryRuntime())
    assert r.source == "denied"
    assert eng.calls == 0


# --- Integration (memory-first) -------------------------------------------
def test_memory_miss_calls_api_and_stores():
    mem = MemoryRuntime()
    eng = FakeEngine()
    r = answer_question("What is XAUUSD?", AIRole.OWNER, flags=FLAGS_ON, conversation_engine=eng, memory_runtime=mem)
    assert r.source == "api" and r.from_memory is False and r.accepted is True
    assert eng.calls == 1
    # stored under the deterministic key as a MemoryAnswer with Source=api
    entry = mem.recall(personal_ai_memory_key("What is XAUUSD?"))
    assert entry is not None
    assert isinstance(entry.value, MemoryAnswer)
    assert entry.value.source == "api"
    assert entry.memory_type is MemoryType.LONG_TERM
    assert entry.scope is MemoryScope.KNOWLEDGE_REFERENCE


def test_memory_hit_skips_api():
    mem = MemoryRuntime()
    eng = FakeEngine()
    first = answer_question("Explain FVG", AIRole.OWNER, flags=FLAGS_ON, conversation_engine=eng, memory_runtime=mem)
    assert first.source == "api" and eng.calls == 1
    # same question (different spacing/case) -> memory hit, NO second API call
    second = answer_question("  explain   fvg ", AIRole.OWNER, flags=FLAGS_ON, conversation_engine=eng, memory_runtime=mem)
    assert second.source == "memory" and second.from_memory is True
    assert second.answer == first.answer
    assert eng.calls == 1  # API was NOT called again


def test_api_rejection_is_failed_and_not_stored():
    mem = MemoryRuntime()
    eng = FakeEngine(accepted=False)
    r = answer_question("offline?", AIRole.OWNER, flags=FLAGS_ON, conversation_engine=eng, memory_runtime=mem)
    assert r.accepted is False and r.source == "failed"
    assert mem.recall(personal_ai_memory_key("offline?")) is None  # nothing stored on failure


# --- End-to-End (live Telegram consumer) ----------------------------------
def test_ask_command_is_registered_and_owner_gated():
    from platform_layer.telegram.commands import OWNER_COMMANDS, COMMANDS
    from platform_layer.telegram import handlers
    assert "ask" in OWNER_COMMANDS
    assert "ask" not in COMMANDS  # OWNER-only, not a public command
    assert hasattr(handlers, "ask_handler")


def test_ask_handler_empty_returns_usage():
    from platform_layer.telegram import handlers
    out = asyncio.run(handlers.ask_handler(telegram_id=111, args=""))
    assert "/ask" in out


def test_route_owner_ask_reaches_personal_ai_gate():
    from platform_layer.telegram.command_router import route_command
    # Owner (111 per tests/conftest) reaches Personal AI Core; with the
    # default flag off the gate returns its disabled message -- proof the
    # live chain Telegram -> router -> handler -> Personal AI runs.
    res = asyncio.run(route_command("/ask what is xauusd", telegram_id=111, username="owner"))
    assert "Personal AI" in res.text


def test_route_non_owner_ask_permission_denied():
    from platform_layer.telegram.command_router import route_command
    res = asyncio.run(route_command("/ask hi", telegram_id=222, username="user"))
    assert "denied" in res.text.lower()
