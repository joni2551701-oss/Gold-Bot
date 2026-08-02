# Decision Service
Status: CANONICAL
---
# Purpose
DecisionService GoldBot Decision Layer uchun Canonical Boundary Gateway hisoblanadi.
Uning asosiy vazifasi Decision Layer'ning yagona Public Entry Point va Public Exit Point bo'lishidir — AI Layer'dan kelgan so'rovlarni Decision Pipeline'ga kiritish va DecisionLogger'dan qaytgan yakuniy natijani Risk Layer'ga chiqarish.
DecisionService Decision yaratmaydi.
DecisionService Rule tekshirmaydi.
DecisionService Approval bermaydi.
DecisionService Logger emas.
DecisionService faqat Entry/Exit Boundary, Validation va Serialization vazifalarini bajaradi.
---
# Objective
DecisionService quyidagi vazifalarni bajaradi.
• Public Entry Point
• Public Exit Point
• Request Validation
• Response Serialization
• Session Management
• API Boundary Enforcement
---
# Layer Position
```text
AI Layer
↓
DecisionService (Entry)
↓
DecisionConfidence
↓
RuleEngine
↓
ApprovalEngine
↓
DecisionEngine
↓
DecisionLogger
↓
DecisionService (Exit)
↓
Risk Layer
```
---
# Responsibilities
DecisionService
✓ AI Layer'dan Decision Request qabul qiladi (Entry)
✓ Request formatini tekshiradi
✓ DecisionConfidence'ga uzatadi
✓ DecisionLogger'dan yakuniy natijani qabul qiladi
✓ Decision Response'ni standartlashtiradi
✓ Risk Layer'ga uzatadi (Exit)
✓ Session boshqaradi
---
# Not Responsible
DecisionService
✗ Decision Making
✗ Rule Validation
✗ Approval
✗ Confidence Calculation
✗ Logging
✗ Trade Execution
✗ Database Management
---
# Input
DecisionService qabul qiladi.
• Decision Request (AI Layer'dan)
• Logged Final Decision (DecisionLogger'dan)
• Session Metadata
---
# Output
DecisionService yaratadi.
• Validated Decision Request (DecisionConfidence'ga)
• Decision Response (Risk Layer'ga)
• Standard Response
• Service Metadata
---
# Workflow
```text
Receive Request (AI Layer)
↓
Validate Request
↓
Forward To DecisionConfidence
↓
Receive Logged Decision (DecisionLogger)
↓
Standardize Response
↓
Return Response (Risk Layer)
```
---
# Golden Rules
1. DecisionService Decision Layer'ning yagona Entry Point va yagona Exit Point hisoblanadi.
2. Decision Logic DecisionService ichida bajarilmaydi.
3. Decision javoblari standart formatga o'tkaziladi.
4. Decision Layer tashqarisiga faqat DecisionService orqali kiriladi va chiqiladi.
5. DecisionLogger Layer tashqarisiga chiqmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
DecisionService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
DecisionService GoldBot Decision Layer uchun ikki tomonlama (bidirectional) Boundary Gateway hisoblanadi — AI Layer'dan Decision Layer'ga kirish va Decision Layer'dan Risk Layer'ga chiqish uchun yagona nuqta.
