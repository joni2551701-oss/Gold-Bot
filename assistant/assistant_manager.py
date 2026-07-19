"""
Assistant Layer — Assistant Manager (Phase 65.3: Personal AI Assistant
Foundation, TASK 4).

Owns exactly one new resource type: `AssistantProfile` (see
`docs/PHASE65_3_AUDIT.md` Question 2/4 for why this is not a duplicate
of `ai.persona.persona_manager.PersonaManager`,
`ai.session.session_manager.SessionManager`, or
`voice.session.manager.VoiceSessionManager`). Every mutator is
Owner-gated via `assistant.access.is_personal_ai_enabled_for()`
(TASK 7) -- never raises on a denied caller, returns
`None`/`False` the same "never fabricate a success" convention every
manager in this codebase already follows.

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
from assistant.models import AssistantProfile
from configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags
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
