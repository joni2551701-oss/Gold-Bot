# Session Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Session modulining rasmiy Architecture Contract hujjati hisoblanadi.
Session GoldBot Context Layer ichidagi Trading Session holatini aniqlovchi yagona Canonical modul hisoblanadi.
---
# Module Responsibility
Session quyidagilar uchun javobgar.
✓ Session Detection
✓ Session Open Detection
✓ Session Close Detection
✓ Kill Zone Detection
✓ Session Overlap Detection
✓ Session Volatility Analysis
✓ Trading Day Classification
✓ Session State Management
✓ Session Event Generation
Session bajarmaydi.
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
Trading Calendar
↓
Session
↓
ContextService
↓
Boundary End
---
# Input Contract
• Current Time
• Trading Calendar
• Market Data
---
# Output Contract
• Current Session
• Session Open
• Session Close
• Kill Zone
• Session Overlap
• Session State
---
# Allowed Dependencies
✓ ContextEngine
✓ ContextService
✓ Event System
✓ Trading Calendar
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
• Session Detection
• Kill Zone Detection
• Active
• Completed
• Failed
---
# Runtime Contract
1. Session faqat Trading Calendar va vaqt asosida aniqlanadi.
2. Kill Zone faqat aktiv Session ichida hisoblanadi.
3. Session Overlap alohida aniqlanishi shart.
4. Session State har bir yangi vaqt yangilanishida qayta hisoblanadi.
5. Signal yaratish taqiqlanadi.
6. Indicator hisoblash taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
Session:
✓ Trading Session aniqlaydi.
✓ Kill Zone aniqlaydi.
✓ Session Overlap aniqlaydi.
✓ Session Volatility baholaydi.
✓ Session State yaratadi.
Session:
✗ Strategy bajarmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Current Session aniqlanadi.
✓ Kill Zone aniqlanadi.
✓ Session Overlap aniqlanadi.
✓ Session State yaratiladi.
✓ Session Event yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Session Contract GoldBot Context Layer ichidagi Trading Session Analysis modulining rasmiy arxitektura shartnomasi hisoblanadi.
Session vaqt, Trading Calendar va bozor sessiyalariga asoslangan yagona Canonical Session Context komponentidir.
