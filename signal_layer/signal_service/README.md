# Signal Service
Status: CANONICAL
---
# Purpose
SignalService GoldBot Signal Layer ichidagi rasmiy Service Boundary hisoblanadi.
Uning asosiy vazifasi Signal Layer va boshqa Layer'lar o'rtasidagi barcha Signal almashinuvini boshqarishdir.
SignalService Signal Layer uchun yagona public entry point hisoblanadi.
SignalService signal yaratmaydi.
SignalService signalni baholamaydi.
SignalService AI ishlatmaydi.
SignalService faqat Signal Service API vazifasini bajaradi.
---
# Objective
SignalService quyidagi vazifalarni bajaradi.
• Signal Request Processing
• Signal Delivery
• Signal Query
• Signal Lifecycle Management
• Signal Event Publishing
• Layer Communication
---
# Layer Position
```text
Signal Layer
↓
SignalService
↓
AI Layer
```
---
# Responsibilities
SignalService
✓ Signal Request qabul qiladi
✓ Signal Result uzatadi
✓ Signal Status boshqaradi
✓ Signal Event yaratadi
✓ Layer Communication bajaradi
✓ Standard Signal API taqdim etadi
---
# Not Responsible
SignalService
✗ Signal Generation
✗ Signal Validation
✗ Signal Scoring
✗ Signal Formatting
✗ AI Analysis
✗ Decision Making
✗ Risk Management
✗ Trade Execution
---
# Input
SignalService qabul qiladi.
• Signal Request
• Formatted Signal
• Signal Metadata
---
# Output
SignalService uzatadi.
• Published Signal
• Signal Response
• Forwarded Signal Result
• Delivery Metadata
• Signal Status
• Signal Event
---
# Workflow
```text
Receive Request
↓
Validate Request
↓
Load Signal
↓
Publish Signal
↓
AI Layer
```
---
# Golden Rules
1. SignalService Signal Layer uchun yagona Service Boundary hisoblanadi.
2. Signal mazmuni o'zgartirilmaydi.
3. SignalService faqat uzatish bilan shug'ullanadi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
SignalService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
SignalService GoldBot Signal Layer ichidagi barcha Signal almashinuvini boshqaruvchi Canonical Service Boundary hisoblanadi.
