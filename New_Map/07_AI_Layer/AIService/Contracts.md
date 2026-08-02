# AI Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat AIService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
AIService quyidagilar uchun javobgar.
✓ Public Entry Point (Signal Layer'dan AI Layer'ga kirish)
✓ Public Exit Point (AI Layer'dan Decision Layer'ga chiqish)
✓ Request Validation
✓ Response Serialization
✓ Session Management
✓ API Boundary Enforcement
AIService bajarmaydi.
✗ AI Analysis
✗ AI Execution
✗ Confidence Calculation
✗ Knowledge Management
✗ Learning
✗ Decision Making
✗ Signal Generation
✗ Trade Execution
---
# Module Boundary
```text
Signal Layer
↓
AIService (Entry)
↓
AIEngine
↓
AICoordinator
↓
AIEngine
↓
AIService (Exit)
↓
Decision Layer
```
---
# Input Contract
Kirish tomonida (Signal Layer'dan):
• AI Request
• Signal Result
• Session Information
• Context Metadata

Chiqish tomonida (AIEngine'dan):
• AI Package
---
# Output Contract
Kirish tomonida (AIEngine'ga):
• Validated AI Request

Chiqish tomonida (Decision Layer'ga):
• AI Response
• Standard Response
• Response Metadata
---
# Allowed Dependencies
✓ AIEngine
---
# Forbidden Dependencies
✗ AICoordinator (to'g'ridan-to'g'ri)
✗ PersonalAI / FundamentalAI / KnowledgeAI / VoiceAI / VisionAI / ExplanationAI / ConfidenceAI (to'g'ridan-to'g'ri)
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
---
# Runtime Contract
1. AI Layer'ga barcha kirish va chiqishlar AIService orqali amalga oshirilishi shart (Boundary Gateway).
2. Har bir kirish Request Validation'dan o'tishi shart.
3. AIService AI Logic bajarmaydi — faqat Entry/Exit Boundary vazifasini bajaradi.
4. AI javoblari standart formatga o'tkazilishi shart.
5. Session holati boshqarilishi shart.
6. AIService AICoordinator yoki AI modullari bilan to'g'ridan-to'g'ri ishlamaydi — faqat AIEngine orqali.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Signal Layer'dan Request qabul qilinadi.
✓ Validation bajariladi.
✓ AIEngine'ga uzatiladi.
✓ AIEngine'dan AI Package qabul qilinadi.
✓ Response standartlashtiriladi.
✓ Decision Layer'ga qaytariladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
AIService Contract GoldBot AI Layer uchun ikki tomonlama (bidirectional) Boundary Gateway sifatida ishlashini — Signal Layer'dan kirish va Decision Layer'ga chiqishni — belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
