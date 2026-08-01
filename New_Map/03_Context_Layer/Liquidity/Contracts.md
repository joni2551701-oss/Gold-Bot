# Liquidity Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Liquidity modulining rasmiy Architecture Contract hujjati hisoblanadi.
Liquidity GoldBot Context Layer ichidagi bozordagi likvidlikni aniqlovchi yagona Canonical modul hisoblanadi.
---
# Module Responsibility
Liquidity quyidagilar uchun javobgar.
✓ Buy-side Liquidity Detection
✓ Sell-side Liquidity Detection
✓ Equal High Detection
✓ Equal Low Detection
✓ Liquidity Pool Generation
✓ Liquidity Sweep Detection
✓ Liquidity Grab Detection
✓ Liquidity State Management
Liquidity bajarmaydi.
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
ContextService
↓
Boundary End
---
# Input Contract
• OHLC Data
• Candle Stream
• Historical Candles
• Market Structure
---
# Output Contract
• Buy-side Liquidity
• Sell-side Liquidity
• Liquidity Pools
• Liquidity Sweep Events
• Liquidity Grab Events
• Liquidity State
---
# Allowed Dependencies
✓ ContextEngine
✓ MarketStructure
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
• Detecting
• Pool Building
• Sweep Detection
• Ready
• Failed
---
# Runtime Contract
1. Liquidity faqat tasdiqlangan Market Structure asosida hisoblanadi.
2. Equal High va Equal Low aniqlanishi majburiy.
3. Liquidity Pool Sweep'dan oldin yaratilishi shart.
4. Liquidity State har bir yangi Candle bilan yangilanadi.
5. Signal yaratish taqiqlanadi.
6. Indicator hisoblash taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
Liquidity:
✓ Liquidity Pool yaratadi.
✓ Sweep aniqlaydi.
✓ Grab aniqlaydi.
✓ Liquidity State yaratadi.
Liquidity:
✗ Strategy bajarmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Buy-side Liquidity aniqlanadi.
✓ Sell-side Liquidity aniqlanadi.
✓ Liquidity Pool yaratiladi.
✓ Sweep Detection ishlaydi.
✓ Liquidity State yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Liquidity Contract GoldBot Context Layer ichidagi Liquidity Analysis modulining rasmiy arxitektura shartnomasi hisoblanadi.
Liquidity bozordagi likvidlik zonalari va Liquidity Event'larni aniqlovchi yagona Canonical komponent hisoblanadi.
