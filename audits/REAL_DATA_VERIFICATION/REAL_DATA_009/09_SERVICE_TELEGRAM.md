# 09 — Service → Telegram — REAL-DATA-009

## Transition

Service → Telegram (telegram_format message quradi; Notifier/
telegram_delivery yuboradi; AI→Telegram bypass yo'q).

- **INPUT:** best approved candidate + uning ai_result/decision/
  risk_result — `pipeline.py:566-573`.
- **PROCESSING:**
  - `self.signal_formatter.format_signal(candidate, ai_result,
    decision, risk_result)` — `pipeline.py:568`
    (`platform_layer/telegram/signal_formatter.py`).
  - `self.notifier.send_messages(telegram_messages)` — `pipeline.py:599`
    (`platform_layer/telegram/notifier.py:120`), faqat
    `send_notifications=True` va `execution_decision.proceed` bo'lsa
    (`pipeline.py:593`).
- **OUTPUT:** `telegram_messages: List[str]` (`pipeline.py:565`),
  `notification_results: List[bool]` (`pipeline.py:592`).
- **NEXT CONSUMER:** TelegramBot → Telegram API (real user).

## AI → Telegram bypass YO'Q

`Notifier` docstring (`notifier.py:28-31`): "send_message() only
delivers text. It must never analyze signals, calculate risk, approve
trades, or modify decisions." Telegram xabari FAQAT DecisionEngine
APPROVE + RiskManager approved bo'lgan candidate uchun quriladi
(`pipeline.py:547-551, 566`). AI to'g'ridan-to'g'ri Telegram'ga
yubormaydi.

## 0-message tushuntirish

Run `31240675527`da `telegram_format Produced 0 telegram message(s)` —
sabab: AI `approved=False` qildi, shuning uchun candidate
notification-eligible emas (`pipeline.py:550`). Bu Trading Safety
notification-eligibility filtri to'g'ri ishlayotgani (REJECT/BLOCKED
signallar Telegram'ga o'tmaydi) — xatolik EMAS. Kod yo'li PASS.

## Ownership

SignalFormatter — message building; Notifier — delivery. Layer
boundary saqlangan.

## Status: PASS (kod yo'li; 0-message run tushuntirilgan)
</content>
