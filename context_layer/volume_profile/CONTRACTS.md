# VolumeProfile Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat VolumeProfile modulining rasmiy Architecture Contract hujjati hisoblanadi.
VolumeProfile GoldBot Context Layer ichidagi Auction Market va Volume Distribution'ni aniqlovchi yagona Canonical modul hisoblanadi.
---
# Module Responsibility
VolumeProfile quyidagilar uchun javobgar.
✓ Volume Profile Generation
✓ Point of Control Calculation
✓ Value Area Calculation
✓ VAH Detection
✓ VAL Detection
✓ HVN Detection
✓ LVN Detection
✓ Volume Distribution Analysis
✓ Volume Profile State Management
✓ Volume Profile Event Generation
VolumeProfile bajarmaydi.
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
VolumeProfile
↓
ContextService
↓
Boundary End
---
# Input Contract
• OHLC Data
• Volume Data
• Historical Data
• Session State
---
# Output Contract
• Volume Profile
• Point of Control (POC)
• Value Area High (VAH)
• Value Area Low (VAL)
• High Volume Nodes (HVN)
• Low Volume Nodes (LVN)
• Volume Profile State
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
• Building Profile
• Calculating
• Ready
• Failed
---
# Runtime Contract
1. Volume Data mavjud bo'lishi shart.
2. Profile POC'dan oldin yaratiladi.
3. Value Area har doim POC asosida hisoblanadi.
4. HVN va LVN Profile'dan olinadi.
5. Signal yaratish taqiqlanadi.
6. Indicator hisoblash taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
VolumeProfile:
✓ Volume Profile yaratadi.
✓ POC hisoblaydi.
✓ VAH va VAL hisoblaydi.
✓ HVN va LVN aniqlaydi.
✓ Volume Profile State yaratadi.
VolumeProfile:
✗ Strategy bajarmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Volume Profile yaratiladi.
✓ POC hisoblanadi.
✓ Value Area hisoblanadi.
✓ HVN va LVN aniqlanadi.
✓ Volume Profile State yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
VolumeProfile Contract GoldBot Context Layer ichidagi Auction Market Analysis modulining rasmiy arxitektura shartnomasi hisoblanadi.
VolumeProfile bozordagi hajm taqsimoti va muhim narx darajalarini aniqlab, Market Context uchun yagona Canonical Volume Profile State yaratadi.
