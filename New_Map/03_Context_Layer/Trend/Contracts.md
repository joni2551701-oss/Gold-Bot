# Trend Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Trend modulining rasmiy Architecture Contract hujjati hisoblanadi.
Trend GoldBot Context Layer ichidagi Market Trend'ni aniqlovchi yagona Canonical modul hisoblanadi.
---
# Module Responsibility
Trend quyidagilar uchun javobgar.
✓ Primary Trend Detection
✓ Secondary Trend Detection
✓ Trend Strength Analysis
✓ Trend Continuation Detection
✓ Trend Reversal Detection
✓ Premium / Discount Analysis
✓ Trend State Management
✓ Trend Event Generation
Trend bajarmaydi.
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
Session
↓
Trend
↓
ContextService
↓
Boundary End
---
# Input Contract
• OHLC Data
• Market Structure
• Session State
---
# Output Contract
• Trend Direction
• Trend Strength
• Premium Zone
• Discount Zone
• Trend Events
• Trend State
---
# Allowed Dependencies
✓ ContextEngine
✓ MarketStructure
✓ Session
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
• Trend Detection
• Trend Analysis
• Ready
• Failed
---
# Runtime Contract
1. Trend faqat tasdiqlangan Market Structure asosida aniqlanadi.
2. Trend Strength doimo hisoblanadi.
3. Premium / Discount zonalari aniqlanishi majburiy.
4. Trend State har bir yangi Candle bilan yangilanadi.
5. Signal yaratish taqiqlanadi.
6. Indicator hisoblash taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
Trend:
✓ Trend Direction yaratadi.
✓ Trend Strength baholaydi.
✓ Premium / Discount aniqlaydi.
✓ Trend Reversal aniqlaydi.
✓ Trend State yaratadi.
Trend:
✗ Strategy bajarmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Trend Direction aniqlanadi.
✓ Trend Strength hisoblanadi.
✓ Premium Zone aniqlanadi.
✓ Discount Zone aniqlanadi.
✓ Trend State yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Trend Contract GoldBot Context Layer ichidagi Market Trend Analysis modulining rasmiy arxitektura shartnomasi hisoblanadi.
Trend Market Context uchun bozor yo'nalishi va trend holatini yaratadigan yagona Canonical komponent hisoblanadi.
