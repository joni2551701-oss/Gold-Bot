# MarketStructure Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat MarketStructure modulining rasmiy Architecture Contract hujjati hisoblanadi.
MarketStructure GoldBot Context Layer ichidagi Market Structure aniqlovchi yagona Canonical modul hisoblanadi.
---
# Module Responsibility
MarketStructure quyidagilar uchun javobgar.
✓ Swing Detection
✓ Market Structure Generation
✓ BOS Detection
✓ CHoCH Detection
✓ MSS Detection
✓ Structure State Management
✓ Structure Event Generation
MarketStructure bajarmaydi.
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
Market Data
↓
MarketStructure
↓
ContextService
↓
Boundary End
---
# Input Contract
• OHLC Data
• Candle Stream
• Historical Candles
• Market Events
---
# Output Contract
• Swing Points
• Market Structure
• BOS Events
• CHoCH Events
• MSS Events
• Structure State
---
# Allowed Dependencies
✓ ContextEngine
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
• Detecting Swings
• Building Structure
• Detecting BOS
• Detecting CHoCH
• Ready
• Failed
---
# Runtime Contract
1. Swing Detection majburiy birinchi bosqich.
2. Market Structure Swing asosida quriladi.
3. BOS Structure'dan keyin aniqlanadi.
4. CHoCH va MSS Structure holatiga asoslanadi.
5. Signal yaratish taqiqlanadi.
6. Indicator hisoblash taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
MarketStructure:
✓ Structure yaratadi.
✓ BOS aniqlaydi.
✓ CHoCH aniqlaydi.
✓ MSS aniqlaydi.
✓ Structure State yaratadi.
MarketStructure:
✗ Signal yaratmaydi.
✗ Strategy ishlatmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Swing Detection ishlaydi.
✓ Market Structure yaratiladi.
✓ BOS Detection ishlaydi.
✓ CHoCH Detection ishlaydi.
✓ MSS Detection ishlaydi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
MarketStructure Contract GoldBot Context Layer ichidagi Market Structure modulining rasmiy arxitektura shartnomasi hisoblanadi.
MarketStructure narx harakati asosida bozor strukturasini yaratadigan yagona Canonical komponent hisoblanadi.
