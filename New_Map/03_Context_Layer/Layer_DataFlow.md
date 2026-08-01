# Context Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat Context Layer ichidagi ma'lumot oqimini tavsiflaydi.
Bu implementatsiya emas.
Bu Context Layer uchun Canonical Data Flow hisoblanadi.
---
# Data Flow
```text
Validated Market Data
        │
        ▼
ContextEngine
        │
        ├──────────────┐
        ▼              ▼
MarketStructure   Liquidity
        │              │
        └──────┬───────┘
               ▼
         OrderBlock
               │
               ▼
        FairValueGap
               │
               ▼
           Wyckoff
               │
               ▼
              AMD
               │
               ▼
           Session
               │
               ▼
             Trend
               │
               ▼
        VolumeProfile
               │
               ▼
        ContextService
               │
               ▼
        Market Context
               │
               ▼
      Indicator Layer
```
---
# Input
• Validated Market Data
• Historical Data
• Current Candle
• Event System
---
# Output
• Market Context
• Context Metadata
• Context State
• Context Events
---
# Data Rules
1. Context faqat Data Layer'dan ma'lumot oladi.
2. Context immutable hisoblanadi.
3. ContextService yagona chiqish nuqtasi.
4. Circular Dependency taqiqlanadi.
