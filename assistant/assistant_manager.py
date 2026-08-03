"""
Assistant Layer — Assistant Manager (Phase 65.3: Personal AI Assistant
Foundation, TASK 4; extended Phase 65.4: Personal AI Runtime
Integration, TASK 1/8).

Owns two resource types: `AssistantProfile` (durable per-user
settings, Phase 65.3) and `AssistantRuntime` (a live session record,
Phase 65.4 TASK 8) -- see `docs/PHASE65_3_AUDIT.md` Question 2/4 and
`docs/PHASE65_4_AUDIT.md` Question 1 for why neither duplicates
`ai.persona.persona_manager.PersonaManager`,
`ai.session.session_manager.SessionManager`, or
`voice.session.manager.VoiceSessionManager`, and why runtime
lifecycle is added here rather than in a new `AssistantRuntimeManager`
class (Rule 3: no new Foundation package). Every mutator is
Owner-gated via `assistant.access.is_personal_ai_enabled_for()`
(TASK 7) -- never raises on a denied caller, returns
`None`/`False` the same "never fabricate a success" convention every
manager in this codebase already follows. This class itself still
imports nothing from `voice/`, `ai.conversation/`, `ai.memory/`, or
`ai.intelligence_runtime` -- per Phase 65.4's own Director Note 3
("Assistant orchestration qatlami bo'lib qoladi... biznes logikasini
o'zida saqlamaydi"), it only manages the `AssistantRuntime` lifecycle
record; the real cross-layer composition lives in
`assistant/runtime_adapter.py`.

In-memory only, no persistence, no background job -- same foundation
posture `ai/session/session_manager.py` and
`voice/session/manager.py` both already commit to.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Optional

from ai.access.permissions import AIRole
from assistant.access import is_personal_ai_enabled_for
from assistant.identity_manager import IdentityManager
from assistant.models import AssistantProfile, AssistantRuntime
from goldbot.core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags
from core.logger import setup_logger

logger = setup_logger("AssistantManager")


class AssistantManager:
    """Every dependency is injectable, same convention as every other Phase 61.x-65.x manager -- a caller/test never needs the real static registry or a real clock to exercise this class."""

    def __init__(
        self,
        identity_manager: Optional[IdentityManager] = None,
        flags: FeatureFlags = DEFAULT_FLAGS,
    ) -> None:
        self._identities = identity_manager or IdentityManager()
        self._flags = flags
        self._profiles: Dict[str, AssistantProfile] = {}
        self._runtimes: Dict[str, AssistantRuntime] = {}

    def create_assistant(
        self,
        user_id: str,
        role: AIRole,
        identity_name: str = "Senior",
        language: str = "en",
        timezone_name: str = "UTC",
    ) -> Optional[AssistantProfile]:
        """Never raises: denied role, an unknown identity_name, or a role missing entitlement all return None rather than creating a profile."""
        if not is_personal_ai_enabled_for(role, self._flags):
            logger.warning(f"create_assistant blocked: role={role} is not entitled to Personal AI Assistant")
            return None
        if not self._identities.exists(identity_name):
            logger.warning(f"create_assistant called with an unknown identity: {identity_name}")
            return None

        assistant_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        profile = AssistantProfile(
            assistant_id=assistant_id, user_id=user_id, selected_identity=identity_name,
            selected_language=language, timezone=timezone_name, created_at=now, updated_at=now,
        )
        self._profiles[assistant_id] = profile
        logger.info(f"Assistant created: assistant_id={assistant_id}, user_id={user_id}, identity={identity_name}")
        return profile

    def get_assistant(self, assistant_id: str) -> Optional[AssistantProfile]:
        return self._profiles.get(assistant_id)

    def get_assistant_for_user(self, user_id: str) -> Optional[AssistantProfile]:
        """Never raises: no profile for this user returns None. Linear scan -- this codebase's own convention is to avoid a premature secondary index until scale requires one."""
        return next((p for p in self._profiles.values() if p.user_id == user_id), None)

    def switch_identity(self, assistant_id: str, identity_name: str, role: AIRole) -> bool:
        """Never raises: denied role, an unknown assistant_id, or an unknown identity_name all return False, leaving the profile unchanged."""
        if not is_personal_ai_enabled_for(role, self._flags):
            logger.warning(f"switch_identity blocked: role={role} is not entitled to Personal AI Assistant")
            return False
        profile = self._profiles.get(assistant_id)
        if profile is None:
            return False
        if not self._identities.exists(identity_name):
            logger.warning(f"switch_identity called with an unknown identity: {identity_name}")
            return False
        profile.selected_identity = identity_name
        profile.updated_at = datetime.now(timezone.utc)
        return True

    def update_settings(
        self,
        assistant_id: str,
        role: AIRole,
        selected_voice: Optional[str] = None,
        selected_language: Optional[str] = None,
        timezone_name: Optional[str] = None,
    ) -> bool:
        """Never raises: denied role or an unknown assistant_id returns False. Only caller-supplied (non-None) fields are updated -- omitted fields keep their current value."""
        if not is_personal_ai_enabled_for(role, self._flags):
            logger.warning(f"update_settings blocked: role={role} is not entitled to Personal AI Assistant")
            return False
        profile = self._profiles.get(assistant_id)
        if profile is None:
            return False
        if selected_voice is not None:
            profile.selected_voice = selected_voice
        if selected_language is not None:
            profile.selected_language = selected_language
        if timezone_name is not None:
            profile.timezone = timezone_name
        profile.updated_at = datetime.now(timezone.utc)
        return True

    # --- Phase 65.4 TASK 1/8: Assistant Runtime lifecycle ---

    def create_runtime(self, assistant_id: str, role: AIRole) -> Optional[AssistantRuntime]:
        """Never raises: denied role or an unknown assistant_id returns None rather than creating a runtime for a nonexistent profile."""
        if not is_personal_ai_enabled_for(role, self._flags):
            logger.warning(f"create_runtime blocked: role={role} is not entitled to Personal AI Assistant")
            return None
        if assistant_id not in self._profiles:
            logger.warning(f"create_runtime called with an unknown assistant_id: {assistant_id}")
            return None

        session_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        runtime = AssistantRuntime(session_id=session_id, assistant_id=assistant_id, started_at=now, updated_at=now, active=True)
        self._runtimes[session_id] = runtime
        logger.info(f"Assistant runtime created: session_id={session_id}, assistant_id={assistant_id}")
        return runtime

    def load_runtime(self, session_id: str) -> Optional[AssistantRuntime]:
        return self._runtimes.get(session_id)

    def restore_runtime(self, session_id: str, role: AIRole) -> bool:
        """Never raises: denied role or an unknown session_id returns False. Re-activates a previously closed runtime without minting a new session_id."""
        if not is_personal_ai_enabled_for(role, self._flags):
            logger.warning(f"restore_runtime blocked: role={role} is not entitled to Personal AI Assistant")
            return False
        runtime = self._runtimes.get(session_id)
        if runtime is None:
            return False
        runtime.active = True
        runtime.updated_at = datetime.now(timezone.utc)
        return True

    def close_runtime(self, session_id: str, role: AIRole) -> bool:
        """Never raises: denied role or an unknown session_id returns False. The runtime record itself is kept (not deleted) so load_runtime()/runtime_status() still resolve it -- restore_runtime() can re-activate it later."""
        if not is_personal_ai_enabled_for(role, self._flags):
            logger.warning(f"close_runtime blocked: role={role} is not entitled to Personal AI Assistant")
            return False
        runtime = self._runtimes.get(session_id)
        if runtime is None:
            return False
        runtime.active = False
        runtime.updated_at = datetime.now(timezone.utc)
        return True

    def runtime_status(self, session_id: str) -> Optional[str]:
        """Never raises: an unknown session_id returns None. Returns 'active' or 'closed' for a known runtime -- never a fabricated status."""
        runtime = self._runtimes.get(session_id)
        if runtime is None:
            return None
        return "active" if runtime.active else "closed"
