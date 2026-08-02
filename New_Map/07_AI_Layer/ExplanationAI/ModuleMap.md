# Explanation AI Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ExplanationAI ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
VoiceAI
↓
ExplanationAI
↓
ConfidenceAI
```
---
# Module Architecture
```text
ExplanationAI
        │
        ├── Context Analyzer
        ├── Explanation Generator
        ├── Reasoning Builder
        ├── Education Adapter
        ├── Language Adapter
        └── Response Formatter
```
---
# Internal Components
## Context Analyzer
Berilgan Context'ni tahlil qiladi.
---
## Explanation Generator
Asosiy tushuntirishni yaratadi.
---
## Reasoning Builder
Bosqichma-bosqich izohni shakllantiradi.
---
## Education Adapter
Foydalanuvchi bilim darajasiga moslashtiradi.
---
## Language Adapter
Til va uslubni moslashtiradi.
---
## Response Formatter
Yakuniy javobni formatlaydi.
---
# Allowed Dependencies
✓ AICoordinator
✓ VisionAI
✓ VoiceAI
✓ ConfidenceAI
---
# Forbidden Dependencies
✗ Decision Engine
✗ PersonalAI
✗ Signal Layer
✗ Execution Layer
✗ Risk Layer
---
# Summary
ExplanationAI GoldBot AI ichidagi barcha Explainability jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
