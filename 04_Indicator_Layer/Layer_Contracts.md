# Indicator Layer Contracts
Status: CANONICAL
---
# Purpose
Indicator Layer GoldBot Trading Engine uchun barcha texnik va proprietary indikatorlarni hisoblaydigan Canonical Layer hisoblanadi.
---
# Layer Responsibility
Indicator Layer quyidagilar uchun javobgar.
✓ Trend Indicators
✓ Momentum Indicators
✓ Volatility Indicators
✓ Volume Indicators
✓ Market Structure Indicators
✓ Smart Money Indicators
✓ Custom Indicators
✓ Indicator Context Generation
---
# Layer NOT Responsible
✗ Market Context Analysis
✗ Strategy
✗ Signal
✗ AI
✗ Decision
✗ Risk
✗ Execution
---
# Input Contract
• Market Context
• OHLC Data
• Volume Data
• Historical Data
---
# Output Contract
• Trend Indicator State
• Momentum Indicator State
• Volatility Indicator State
• Volume Indicator State
• Market Structure Indicator State
• Smart Money Indicator State
• Custom Indicator State
• Indicator Context
---
# Layer Boundary
```text
Context Layer
↓
Indicator Layer
↓
Strategy Layer
```
---
# Canonical Indicator Context
Indicator Context quyidagi komponentlardan tashkil topadi.
- Trend Indicators
- Momentum Indicators
- Volatility Indicators
- Volume Indicators
- Market Structure Indicators
- Smart Money Indicators
- Custom Indicators
Ushbu komponentlar birgalikda **Indicator Context** ni hosil qiladi va Strategy Layer uchun yagona indikator manbasi hisoblanadi.
---
# Layer Rules
1. Indicator Layer faqat Context Layer ma'lumotlaridan foydalanadi.
2. Indicator formulalari faqat Indicator Layer ichida hisoblanadi.
3. Indicator Context immutable hisoblanadi.
4. IndicatorService yagona publish nuqtasi hisoblanadi.
5. Signal yaratish taqiqlanadi.
6. AI ishlatish taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Barcha Indicator modullari muvaffaqiyatli bajariladi.
✓ Indicator Context yaratiladi.
✓ Indicator Validation muvaffaqiyatli yakunlanadi.
✓ Indicator Context Strategy Layer'ga uzatiladi.
✓ Layer Architecture Contract buzilmaydi.
