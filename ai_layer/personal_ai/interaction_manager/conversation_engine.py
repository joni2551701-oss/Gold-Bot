"""
AI Layer — Conversation Engine (Phase 61.3: AI Intelligence Layer,
TASK 5; extended Phase 63.5: AI Conversation Intelligence Foundation,
TASK 3).

The first caller of two foundation packages that were built but never
called: `ai/session/` (Phase 61.0, TASK 7 -- `SessionManager`/
`ConversationState`/`ContextWindow`, confirmed unused in production
code by this phase's own TASK 1 audit) and
`ai/runtime/ai_service.py`'s `AIService.ask()` (Phase 61.2). This
module adds no new session storage, no new provider call, and no new
capability -- it is a thin orchestration layer:

    get-or-create ConversationState (SessionManager)
      -> record the user's turn
      -> ContextWindow-trim recent history into a prompt
      -> RuntimeRequest(capability=CHAT) -> AIService.ask()
      -> on acceptance, record the assistant's turn
      -> return the RuntimeResponse plus session_id

`ask()` requires an already-built `AIContext` from the caller (via
`ai_layer.ai_engine.context.context_builder.build_ai_context()`) rather than
constructing one itself -- `AIService.ask()`'s cache-key path
(`ai_layer.ai_engine.cache.cache_policy.build_cache_key_from_context()`) raises
`ValueError` on an `AIContext` whose `snapshot_id` is `None`, which a
directly-constructed `AIContext()` would leave unset. This module
never works around that by constructing its own `AIContext` -- doing
so would also require importing `context/`, which `ai/` deliberately
never does (see `ai/context/context_adapter.py`'s docstring).

Not wired into `platform_layer/telegram/command_router.py` this phase -- same
"foundation, not yet live-wired" posture as every other Phase 61.x
module (`docs/PHASE61_3_INTELLIGENCE_AUDIT.md`'s `telegram/` finding:
no free-text/conversational handling exists anywhere in `telegram/`
today).

Phase 63.5 added a second, deterministic surface on this same class,
alongside `start_session()`/`ask()`, which are completely unchanged:
`append()`/`summarize()`/`history()`/`context()`/`reset()`/`close()`.
None of these six call `AIService.ask()` or make any network call --
per `docs/PHASE63_5_AUDIT.md`'s own finding, `ConversationEngine`
already existed as the one real Manager for Conversation, so
Constitution Article 11 forbids a second, competing class for the same
concern; the deterministic surface this phase's own brief asked for is
added here instead.
"""

from dataclasses import dataclass
from typing import Optional, Sequence

from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_engine.capabilities.capability import Capability
from ai_layer.ai_engine.context.context_snapshot import AIContext
from ai_layer.personal_ai.interaction_manager.models import ConversationContext, ConversationMode
from ai_layer.ai_engine.runtime.ai_service import AIService
from ai_layer.ai_engine.runtime.runtime_request import RuntimeRequest
from ai_layer.ai_engine.runtime.runtime_response import RuntimeResponse
from ai_layer.ai_service.session.context_window import ContextWindow
from ai_layer.ai_service.session.conversation_state import ConversationState, ConversationTurn
from ai_layer.ai_service.session.session_manager import SessionManager


@dataclass(frozen=True)
class ConversationResult:
    session_id: str
    response: RuntimeResponse


def _format_prompt(turns) -> str:
    """Renders trimmed history as 'Role: content' lines, oldest first -- the same free-text role convention `ConversationTurn` itself uses, no new formatting vocabulary."""
    return "\n".join(f"{turn.role.capitalize()}: {turn.content}" for turn in turns)


class ConversationEngine:
    """Every dependency is injectable, same convention as `AIService` itself -- a test never needs a real provider or a real clock."""

    def __init__(
        self,
        session_manager: Optional[SessionManager] = None,
        ai_service: Optional[AIService] = None,
        context_window: Optional[ContextWindow] = None,
    ) -> None:
        self._session_manager = session_manager or SessionManager()
        self._ai_service = ai_service or AIService()
        self._context_window = context_window or ContextWindow()

    def start_session(self, telegram_id: str) -> ConversationState:
        return self._session_manager.create_session(telegram_id)

    def ask(
        self,
        session_id: str,
        message: str,
        ai_context: AIContext,
        role: AIRole,
        telegram_id: Optional[str] = None,
    ) -> ConversationResult:
        """Never raises: an unknown session_id produces an unaccepted ConversationResult, matching AIService.ask()'s own never-raises posture for every rejection path."""
        state = self._session_manager.get_session(session_id)
        if state is None:
            return ConversationResult(
                session_id=session_id,
                response=RuntimeResponse(
                    accepted=False, content=None, provider_name=None,
                    reason=f"unknown session_id {session_id}",
                ),
            )

        state.add_turn("user", message)

        recent_turns = self._context_window.trim(state.history())
        prompt = _format_prompt(recent_turns)

        request = RuntimeRequest(
            capability=Capability.CHAT,
            ai_context=ai_context,
            role=role,
            prompt=prompt,
            telegram_id=telegram_id or state.telegram_id,
        )
        response = self._ai_service.ask(request)

        if response.accepted and response.content:
            state.add_turn("assistant", response.content)

        return ConversationResult(session_id=session_id, response=response)

    # --- Phase 63.5 TASK 3: deterministic surface, additive only ---
    # None of the six methods below call AIService.ask() or make any
    # network call -- start() itself is already covered by
    # start_session() above, so no separate start() method is added.

    def append(self, session_id: str, role: str, content: str) -> bool:
        """Records one turn without calling AIService. Never raises: an unknown session_id returns False."""
        state = self._session_manager.get_session(session_id)
        if state is None:
            return False
        state.add_turn(role, content)
        return True

    def summarize(self, session_id: str) -> Optional[str]:
        """Joins each stored turn's `role: content` into one short string. Never raises: an unknown session_id returns None."""
        state = self._session_manager.get_session(session_id)
        if state is None:
            return None
        return "; ".join(f"{turn.role}: {turn.content}" for turn in state.history())

    def history(self, session_id: str) -> Sequence[ConversationTurn]:
        """Never raises: an unknown session_id returns an empty tuple."""
        state = self._session_manager.get_session(session_id)
        if state is None:
            return ()
        return state.history()

    def context(
        self,
        session_id: str,
        mode: ConversationMode = ConversationMode.GENERAL,
        knowledge_keys: Sequence[str] = (),
        memory_keys: Sequence[str] = (),
        reasoning_keys: Sequence[str] = (),
    ) -> Optional[ConversationContext]:
        """Assembles a ConversationContext from already-stored turns plus caller-supplied upstream-layer key pointers. Never raises: an unknown session_id returns None."""
        state = self._session_manager.get_session(session_id)
        if state is None:
            return None
        return ConversationContext(
            session_id=state.session_id,
            telegram_id=state.telegram_id,
            mode=mode,
            recent_messages=self._context_window.trim(state.history()),
            knowledge_keys=tuple(knowledge_keys),
            memory_keys=tuple(memory_keys),
            reasoning_keys=tuple(reasoning_keys),
        )

    def reset(self, session_id: str) -> bool:
        """Clears a session's turn history; the session itself stays alive. Never raises: an unknown session_id returns False."""
        state = self._session_manager.get_session(session_id)
        if state is None:
            return False
        state.clear_turns()
        return True

    def close(self, session_id: str) -> bool:
        """Ends a session via the existing SessionManager.end_session(). Never raises: an unknown session_id returns False."""
        if self._session_manager.get_session(session_id) is None:
            return False
        self._session_manager.end_session(session_id)
        return True
