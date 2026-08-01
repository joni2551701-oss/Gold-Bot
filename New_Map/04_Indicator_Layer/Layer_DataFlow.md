# Indicator Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat Indicator Layer ichidagi ma'lumot oqimini tavsiflaydi.
Bu implementatsiya emas.
Bu Indicator Layer uchun Canonical Data Flow hisoblanadi.
---
# Data Flow
```text
Market Context
        │
        ▼
IndicatorEngine
        │
        ├──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
Trend      Momentum   Volatility   Volume
Indicators Indicators Indicators  Indicators
        │              │              │              │
        └──────────────┴──────────────┬──────────────┘
                                      ▼
                        MarketStructureIndicators
                                      │
                                      ▼
                        SmartMoneyIndicators
                                      │
                                      ▼
                           CustomIndicators
                                      │
                                      ▼
                            IndicatorService
                                      │
                                      ▼
                           Indicator Context
                                      │
                                      ▼
                            Strategy Layer
```
---
# Input
• Market Context
• OHLC Data
• Volume Data
• Historical Data
• Runtime Configuration
---
# Output
• Trend Indicator State
• Momentum Indicator State
• Volatility Indicator State
• Volume Indicator State
• Market Structure Indicator State
• Smart Money Indicator State
• Custom Indicator State
• Indicator Context
---
# Data Rules
1. Indicator Layer faqat Context Layer'dan ma'lumot oladi.
2. Indicator Context immutable hisoblanadi.
3. IndicatorService yagona publish nuqtasi hisoblanadi.
4. Indicator Calculation faqat Indicator Layer ichida bajariladi.
5. Circular Dependency qat'iyan taqiqlanadi.
