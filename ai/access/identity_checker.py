"""
AI Layer — AI Identity Checker (Phase 61.4: AI Product & Control
Layer, TASK 5).

Pure phone-reuse check -- never imports `database/` or `telegram/`,
and never reads a raw phone number or even a `phone_hash` value
itself. `ai/` deliberately holds no runtime dependency on `database/`
(`docs/PHASE61_4_PRODUCT_CONTROL_AUDIT.md`'s own finding, and
`ai/access/permission_service.py`'s docstring for the established
pattern this reuses): a caller who already legitimately queried
`database.user_repository.UserRepository.get_users_by_phone_hash()`
extracts the matching `telegram_id`s and passes them in here.
"""

from typing import Sequence


def is_phone_reused_by_another_account(
    current_telegram_id: str, telegram_ids_sharing_phone: Sequence[str],
) -> bool:
    """
    True if `telegram_ids_sharing_phone` contains any id other than
    `current_telegram_id` -- the exact abuse pattern (same phone
    number, a second Telegram account) TASK 5 exists to catch. Never
    raises: an empty sequence, or a sequence containing only
    `current_telegram_id` itself, is not reuse.
    """
    return any(telegram_id != current_telegram_id for telegram_id in telegram_ids_sharing_phone)
