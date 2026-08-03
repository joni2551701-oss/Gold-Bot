# AI Engine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat AIEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
AIEngine quyidagilar uchun javobgar.
✓ Entry Orchestration
✓ Request Routing
✓ Runtime Pipeline Control
✓ AI Lifecycle Management
✓ AI State Management
AIEngine bajarmaydi.
✗ AI Module Execution (AICoordinator vazifasi)
✗ AI Analysis
✗ Personal Memory
✗ News Analysis
✗ Knowledge Search
✗ Voice Processing (VoiceAI vazifasi — AIEngine Voice'ni o'zi qayta ishlamaydi, lekin VoiceAI subsystemini AICoordinator orqali orkestratsiya qiladi)
✗ Vision Processing
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
AIService
↓
AIEngine
↓
AICoordinator
```
---
# Input Contract
• AI Request (AIService'dan)
• Context
---
# Output Contract
• AI Execution Plan
• Runtime Status

AICoordinator'dan qaytgandan so'ng:
• AI Result (AIService'ga uzatish uchun)
---
# Allowed Dependencies
✓ AIService
✓ AICoordinator
---
# Forbidden Dependencies
✗ PersonalAI (to'g'ridan-to'g'ri)
✗ FundamentalAI (to'g'ridan-to'g'ri)
✗ KnowledgeAI (to'g'ridan-to'g'ri)
✗ VoiceAI (to'g'ridan-to'g'ri)
✗ VisionAI (to'g'ridan-to'g'ri)
✗ ExplanationAI (to'g'ridan-to'g'ri)
✗ ConfidenceAI (to'g'ridan-to'g'ri)
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Har bir AI Request AIService orqali AIEngine'ga yetib keladi.
2. AIEngine faqat Request Routing va Pipeline Control bajaradi.
3. AI modullarini bevosita chaqirish taqiqlanadi — bu AICoordinator vazifasi.
4. AICoordinator'dan qaytgan natija o'zgartirilmasdan AIService'ga uzatiladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Request AIService'dan qabul qilinadi.
✓ Pipeline Control bajariladi.
✓ AICoordinator'ga uzatiladi.
✓ Natija AIService'ga qaytariladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
AIEngine Contract GoldBot AI Layer ichidagi Entry Orchestration, Request Routing va Runtime Pipeline Control'ni boshqaruvchi rasmiy Canonical Architecture Contract hisoblanadi. AI modullarining bevosita ishga tushirilishi AICoordinator vakolatida qoladi.
