# AI Engine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat AIEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
AIEngine quyidagilar uchun javobgar.
✓ AI Pipeline Management
✓ AI Module Routing
✓ AI Execution Coordination
✓ AI Lifecycle Management
✓ AI State Management
✓ AI Result Collection
AIEngine bajarmaydi.
✗ AI Analysis
✗ Personal Memory
✗ News Analysis
✗ Knowledge Search
✗ Voice Processing
✗ Vision Processing
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
Signal Layer
↓
AIEngine
↓
AI Modules
↓
AICoordinator
```
---
# Input Contract
• Signal Result
• User Request
• AI Request
• Context
---
# Output Contract
• AI Tasks
• AI Execution Plan
• AI Results
---
# Allowed Dependencies
✓ PersonalAI
✓ FundamentalAI
✓ KnowledgeAI
✓ VoiceAI
✓ VisionAI
✓ ExplanationAI
✓ ConfidenceAI
✓ AICoordinator
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Har bir AI Request AIEngine orqali o'tishi shart.
2. AIEngine faqat orchestration bajaradi.
3. Har bir AI modul mustaqil ishlaydi.
4. AI natijalari AICoordinator orqali birlashtiriladi.
5. AIEngine AI Logic bajarmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Request qabul qilinadi.
✓ Kerakli AI modullari tanlanadi.
✓ Pipeline bajariladi.
✓ Natijalar yig'iladi.
✓ AICoordinator'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
AIEngine Contract GoldBot AI Layer ichidagi barcha AI modullarining ishlashini boshqaruvchi rasmiy Canonical Architecture Contract hisoblanadi.
