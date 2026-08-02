# Signal Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
SignalService quyidagilar uchun javobgar.
✓ Signal Request Processing
✓ Signal Delivery
✓ Signal Response Generation
✓ Signal Status Management
✓ Signal Event Publishing
✓ Layer Communication
SignalService bajarmaydi.
✗ Signal Generation
✗ Signal Validation
✗ Signal Scoring
✗ Signal Formatting
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
Signal Formatter
↓
SignalService
↓
AI Layer
```
---
# Input Contract
• Formatted Signal
• Signal Metadata
• Signal Request
---
# Output Contract
• Signal Response
• Forwarded Signal Result
• Delivery Metadata
• Signal Status
• Signal Event
---
# Allowed Dependencies
✓ SignalFormatter
✓ Event System
✓ Signal Model
---
# Forbidden Dependencies
✗ AI Layer Internal Modules
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Barcha Signal almashinuvi SignalService orqali amalga oshiriladi.
2. Signal mazmuni o'zgartirilmaydi.
3. SignalService faqat transport va Service Boundary vazifasini bajaradi.
4. Har bir Request bitta Response qaytarishi kerak.
5. Signal Result immutable bo'lishi kerak.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Signal Request qabul qilinadi.
✓ Request tekshiriladi.
✓ Signal yuklanadi.
✓ Signal Response yaratiladi.
✓ Signal AI Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
SignalService Contract GoldBot Signal Layer ichidagi barcha Signal almashinuvini boshqaruvchi va AI Layer bilan bog'lovchi rasmiy Canonical Architecture Contract hisoblanadi.
