# Personal AI Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat PersonalAI modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
PersonalAI quyidagilar uchun javobgar.
✓ User Interaction
✓ Persona Management
✓ User Profile Management
✓ Personalized Response
✓ Conversation Management
✓ KnowledgeAI Integration
PersonalAI bajarmaydi.
✗ Knowledge Storage
✗ Memory Storage
✗ News Analysis
✗ Voice Recognition
✗ Vision Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
AIEngine
↓
PersonalAI
↓
KnowledgeAI
↓
AICoordinator
```
---
# Input Contract
• User Request
• User Profile
• Conversation Context
• Knowledge Context
---
# Output Contract
• Personalized Response
• AI Context
• Interaction Result
---
# Allowed Dependencies
✓ AIEngine
✓ KnowledgeAI
✓ AICoordinator
---
# Forbidden Dependencies
✗ FundamentalAI
✗ VoiceAI
✗ VisionAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Har bir foydalanuvchi faqat bitta faol Persona bilan ishlaydi.
2. Senior va Seniorita bir xil AI Core'dan foydalanadi.
3. Shared Memory ishlatiladi.
4. Shared Knowledge ishlatiladi.
5. Persona faqat javob uslubi va taqdimotini o'zgartiradi.
6. PersonalAI yangi bilim saqlamaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Persona aniqlanadi.
✓ User Profile yuklanadi.
✓ KnowledgeAI bilan integratsiya ishlaydi.
✓ Personalized Response yaratiladi.
✓ AICoordinator'ga natija uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
PersonalAI Contract GoldBot ichidagi yagona Personal Intelligence modulining rasmiy arxitektura shartnomasi hisoblanadi. Senior va Seniorita alohida AI emas, balki bitta AI Core'ning ikki xil Persona ko'rinishidir.
