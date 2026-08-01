# Signal Builder Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalBuilder modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
SignalBuilder quyidagilar uchun javobgar.
✓ Signal Construction
✓ Entry Generation
✓ Stop Loss Generation
✓ Take Profit Generation
✓ Metadata Generation
✓ Signal Result Generation
SignalBuilder bajarmaydi.
✗ Signal Validation
✗ Signal Scoring
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
Confluence Engine
↓
SignalBuilder
↓
Signal Validator
```
---
# Input Contract
• Strategy Result
• Technical Confluence
• Strategy Metadata
---
# Output Contract
• Signal Result
• Direction
• Entry
• Stop Loss
• Take Profit
• Metadata
---
# Allowed Dependencies
✓ Strategy Result
✓ Confluence Engine
✓ Signal Model
---
# Forbidden Dependencies
✗ Signal Validator
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Strategy Result mavjud bo'lishi shart.
2. Technical Confluence mavjud bo'lishi shart.
3. SignalBuilder faqat Signal Result yaratadi.
4. Validation SignalBuilder tashqarisida bajariladi.
5. Signal Result immutable bo'lishi kerak.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Signal Result yaratiladi.
✓ Direction yaratiladi.
✓ Entry yaratiladi.
✓ Stop Loss yaratiladi.
✓ Take Profit yaratiladi.
✓ Metadata yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
SignalBuilder Contract GoldBot Signal Layer ichidagi standart Signal Result obyektini yaratuvchi rasmiy Canonical Architecture Contract hisoblanadi.
