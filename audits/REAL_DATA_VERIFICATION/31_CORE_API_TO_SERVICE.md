# 31 — Core/API → Service (TASK-09 + TASK-10)

## Transition
Core/API boundary DTO va Core/API → Service (FLOW-019 bo'yicha LIVE
Telegram `*_service.py` application service'lari — `platform_layer/
platform_service/` EMAS, u Foundation).

## Input
Ikki xil live consumer yo'li mavjud:
1. **Pipeline signal delivery yo'li:** approve'langan winner nomzod →
   `SignalFormatter.format_signal(...)` → matn (DTO chegarasi).
   Evidence: `core_layer/pipeline/pipeline.py:566-574`.
2. **Telegram bot buyruq yo'li (FLOW-019):** foydalanuvchi buyrug'i →
   handler → application service.

## Processing (file:line) — Core/API DTO
- SignalFormatter DTO chegarasi: `core_layer/pipeline/pipeline.py:568`
  `self.signal_formatter.format_signal(...)`; formatter
  `platform_layer/telegram/signal_formatter.py` — `FormattedSignal` DTO'ni
  quradi va matn qaytaradi (analiz/risk/decision qilmaydi).

## Processing (file:line) — Core/API → Service (FLOW-019)
- Handlers application service'larni chaqiradi (DB'ga to'g'ridan-to'g'ri
  emas): `platform_layer/telegram/handlers.py:171-179` importlar
  (`UserService`, `RegistrationService`, `AdminService`, `SignalService`,
  `SubscriptionService`, `NotificationService`, `SignalAccessService`,
  `FeedbackService`).
- LIVE application service'lar: `platform_layer/telegram/user_service.py`,
  `signal_service.py`, `admin_service.py`, `subscription_service.py`,
  `notification_service.py`, `feedback_service.py`,
  `registration_service.py`, `signal_access_service.py`,
  `current_price_service.py`.
- Arxitektura qoidasi (CLAUDE.md): handlers → service → repository. Handler
  DB'ga bevosita murojaat qilmaydi — `handlers.py:155` "A handler must
  never import database.* or core_layer.pipeline directly".

## Output
Service'lar business logikani bajaradi, repository orqali SQL'ni
chaqiradi, handler'ga matn/natija qaytaradi.

## Next Consumer
Handler → Telegram API (32-hujjat).

## Ownership-rule check
- FLOW-019 LIVE application service'lar `platform_layer/telegram/*_service.py`
  da (Foundation `platform_layer/platform_service/` EMAS) — PASS.
- Handler → Service → Repository chegarasi saqlangan (CLAUDE.md
  enforced).

## Status
**PASS** — Core/API DTO (`SignalFormatter`/`FormattedSignal`) va Core/API →
Service (FLOW-019 handlers → `*_service.py`) real kod bilan tasdiqlangan.
</content>
