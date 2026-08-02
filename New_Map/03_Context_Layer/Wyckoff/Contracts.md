# Wyckoff Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Wyckoff modulining rasmiy Architecture Contract hujjati hisoblanadi.
Wyckoff GoldBot Context Layer ichidagi Wyckoff Market Cycle'ni aniqlovchi yagona Canonical modul hisoblanadi.
---
# Module Responsibility
Wyckoff quyidagilar uchun javobgar.
✓ Market Phase Detection
✓ Accumulation Detection
✓ Distribution Detection
✓ Re-Accumulation Detection
✓ Re-Distribution Detection
✓ Spring Detection
✓ Upthrust Detection
✓ SOS Detection
✓ SOW Detection
✓ Wyckoff State Management
✓ Wyckoff Event Generation
Wyckoff bajarmaydi.
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
MarketStructure
↓
Liquidity
↓
Wyckoff
↓
ContextService
↓
Boundary End
---
# Input Contract
• OHLC Data
• Market Structure
• Liquidity State
---
# Output Contract
• Market Phase
• Spring Events
• Upthrust Events
• SOS Events
• SOW Events
• Wyckoff State
---
# Allowed Dependencies
✓ ContextEngine
✓ MarketStructure
✓ Liquidity
✓ ContextService
✓ Event System
---
# Forbidden Dependencies
✗ Indicator Layer
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# State Contract
• Initializing
• Phase Detection
• Event Detection
• Ready
• Failed
---
# Runtime Contract
1. Market Phase aniqlanishi majburiy.
2. Spring va Upthrust Phase ichida tekshiriladi.
3. SOS va SOW Phase natijasiga bog'liq.
4. Wyckoff State har bir yangi Candle bilan yangilanadi.
5. Signal yaratish taqiqlanadi.
6. Indicator hisoblash taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
Wyckoff:
✓ Market Phase yaratadi.
✓ Spring aniqlaydi.
✓ Upthrust aniqlaydi.
✓ SOS aniqlaydi.
✓ SOW aniqlaydi.
✓ Wyckoff State yaratadi.
Wyckoff:
✗ Strategy bajarmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Market Phase aniqlanadi.
✓ Spring Detection ishlaydi.
✓ Upthrust Detection ishlaydi.
✓ SOS Detection ishlaydi.
✓ SOW Detection ishlaydi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Wyckoff Contract GoldBot Context Layer ichidagi Wyckoff Analysis modulining rasmiy arxitektura shartnomasi hisoblanadi.
Wyckoff bozordagi Composite Operator faoliyati va Market Cycle holatini aniqlovchi yagona Canonical komponent hisoblanadi.
