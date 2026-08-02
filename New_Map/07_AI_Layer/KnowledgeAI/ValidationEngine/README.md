# Validation Engine
Status: CANONICAL
---
# Purpose
ValidationEngine GoldBot KnowledgeAI ichidagi Canonical Knowledge Validation moduli hisoblanadi.
Uning asosiy vazifasi yangi Knowledge, Memory yoki External AI javoblarini tekshirish, ishonchliligini baholash va faqat tasdiqlangan ma'lumotlarni LearningEngine'ga uzatishdir.
ValidationEngine yangi bilim yaratmaydi.
ValidationEngine Learning bajarmaydi.
ValidationEngine Knowledge saqlamaydi.
---
# Objective
ValidationEngine quyidagi vazifalarni bajaradi.
• Knowledge Validation
• Fact Verification
• Source Validation
• Confidence Evaluation
• Duplicate Detection
• Knowledge Approval
---
# Layer Position
```text
ProviderRouter
↓
ValidationEngine
↓
LearningEngine
↓
KnowledgeManager
```
---
# Responsibilities
ValidationEngine
✓ Knowledge tekshiradi
✓ Source ishonchliligini baholaydi
✓ Duplicate aniqlaydi
✓ Confidence hisoblaydi
✓ Validation Report yaratadi
✓ Learning uchun Approval beradi
---
# Not Responsible
ValidationEngine
✗ Learning
✗ Memory Storage
✗ Knowledge Storage
✗ AI Analysis
✗ Signal Generation
✗ Decision Making
---
# Input
ValidationEngine qabul qiladi.
• New Knowledge
• External AI Response
• RAG Result
• Knowledge Metadata
---
# Output
ValidationEngine yaratadi.
• Validation Result
• Confidence Score
• Validation Report
• Approved Knowledge
---
# Workflow
```text
Receive Knowledge
↓
Validate Source
↓
Check Duplicate
↓
Evaluate Confidence
↓
Approve / Reject
↓
LearningEngine
```
---
# Golden Rules
1. Har qanday yangi Knowledge Validation'dan o'tishi shart.
2. Duplicate Knowledge rad etiladi.
3. Confidence Score hisoblanadi.
4. Ishonchsiz Knowledge Learning'ga yuborilmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ValidationEngine/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ValidationEngine GoldBot AI ichidagi barcha yangi bilimlarni tekshiruvchi va faqat ishonchli ma'lumotlarni LearningEngine'ga uzatuvchi Canonical modul hisoblanadi.
