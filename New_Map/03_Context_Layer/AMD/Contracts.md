# AMD Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat AMD modulining rasmiy Architecture Contract hujjati hisoblanadi.
AMD GoldBot Context Layer ichidagi Accumulation–Manipulation–Distribution Market Cycle'ni aniqlovchi yagona Canonical modul hisoblanadi.
---
# Module Responsibility
AMD quyidagilar uchun javobgar.
✓ Accumulation Detection
✓ Manipulation Detection
✓ Distribution Detection
✓ Phase Transition Detection
✓ Liquidity Manipulation Detection
✓ Breakout Confirmation
✓ AMD State Management
✓ AMD Event Generation
AMD bajarmaydi.
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
AMD
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
• AMD Phase
• Accumulation Zone
• Manipulation Zone
• Distribution Zone
• Phase Events
• AMD State
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
• Accumulation
• Manipulation
• Distribution
• Ready
• Failed
---
# Runtime Contract
1. AMD faqat tasdiqlangan Market Structure asosida ishlaydi.
2. Liquidity Manipulation aniqlanishi majburiy.
3. Phase ketma-ketligi buzilmasligi kerak.
4. Distribution Manipulation'dan keyin boshlanishi mumkin.
5. Signal yaratish taqiqlanadi.
6. Indicator hisoblash taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
AMD:
✓ Market Cycle aniqlaydi.
✓ Phase Transition kuzatadi.
✓ Liquidity Manipulation aniqlaydi.
✓ AMD State yaratadi.
AMD:
✗ Strategy bajarmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Accumulation aniqlanadi.
✓ Manipulation aniqlanadi.
✓ Distribution aniqlanadi.
✓ Phase Validation ishlaydi.
✓ AMD State yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
AMD Contract GoldBot Context Layer ichidagi Institutional AMD Analysis modulining rasmiy arxitektura shartnomasi hisoblanadi.
AMD bozordagi Accumulation → Manipulation → Distribution siklini aniqlab, Market Context uchun yagona Canonical AMD State yaratadi.
