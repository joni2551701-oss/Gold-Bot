# Context Layer Contracts
Status: CANONICAL
---
# Purpose
Context Layer GoldBot Trading Engine uchun Market Context yaratadigan Canonical Layer hisoblanadi.
---
# Layer Responsibility
Context Layer javobgar:
✓ Market Structure
✓ Liquidity
✓ Order Block
✓ Fair Value Gap
✓ Wyckoff
✓ AMD
✓ Session
✓ Trend
✓ Volume Profile
✓ Market Context Generation
---
# Layer NOT Responsible
✗ Indicators
✗ Strategy
✗ Signal
✗ AI
✗ Decision
✗ Risk
✗ Execution
---
# Input Contract
• Validated Market Data
• Historical Data
• Event System
---
# Output Contract
• Market Context
• Context Metadata
• Context State
• Context Events
---
# Layer Boundary
```text
Data Layer
↓
Context Layer
↓
Indicator Layer
```
---
# Canonical Context
Market Context quyidagi komponentlardan tashkil topadi:
- Market Structure
- Liquidity
- Order Block
- Fair Value Gap
- Wyckoff State
- AMD State
- Session State
- Trend State
- Volume Profile State
Ushbu komponentlar birgalikda **Smart Money Context (SMC Context)** ni hosil qiladi.
---
# Layer Rules
1. Context Layer yagona Market Context yaratadi.
2. Context immutable hisoblanadi.
3. ContextService yagona publish nuqtasi.
4. Signal yaratish taqiqlanadi.
5. Indicator hisoblash taqiqlanadi.
6. AI ishlatish taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Barcha Context modullari ishlaydi.
✓ Market Context muvaffaqiyatli yaratiladi.
✓ ContextService agregatsiyani bajaradi.
✓ Market Context Indicator Layer'ga uzatiladi.
✓ Layer Architecture Contract buzilmaydi.
