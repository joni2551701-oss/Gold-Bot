# AI Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat GoldBot AI Layer ichidagi umumiy ma'lumot oqimini (Data Flow) tavsiflaydi.
AI Layer barcha AI modullarini yagona Pipeline sifatida ishlatadi va Decision Layer uchun AI Package yaratadi.
---
# Layer Data Flow
```text
External Layers
(Data / Context / Signal)
        │
        ▼
AIService
        │
        ▼
AIEngine
        │
        ▼
AICoordinator
        │
        ├──────────────┐
        ▼              ▼
PersonalAI      KnowledgeAI
        │              │
        ▼              ▼
FundamentalAI   VisionAI
        │              │
        └──────┬───────┘
               ▼
ExplanationAI
               ▼
ConfidenceAI
               ▼
AI Package
               ▼
Decision Layer
```
---
# Input Sources
• Context Layer
• Signal Layer
• User Request
• Vision Input
• Voice Input
---
# Output
• Unified AI Context
• AI Package
• Confidence Report
• Explanation
---
# Golden Rules
1. AI faqat Context beradi.
2. Decision Layer qaror qabul qiladi.
3. AI Signal yaratmaydi.
4. AI Trade ochmaydi.
5. AI Layer yagona Pipeline sifatida ishlaydi.
