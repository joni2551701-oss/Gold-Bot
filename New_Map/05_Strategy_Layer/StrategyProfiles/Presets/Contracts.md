# Presets Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Presets modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Presets quyidagilar uchun javobgar.
✓ Preset Creation
✓ Preset Loading
✓ Preset Saving
✓ Preset Validation
✓ Preset Version Management
✓ Strategy Configuration Generation
Presets bajarmaydi.
✗ Strategy Logic
✗ Indicator Calculation
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Preset Contents
Har bir Preset quyidagilarni saqlashi mumkin.
• Strategy
• Trading Style
• Session
• Timeframe
• Risk Profile
• Filters
• User Preferences
---
# Input Contract
• User Configuration
• System Configuration
---
# Output Contract
• Strategy Preset
• Strategy Configuration
---
# Allowed Dependencies
✓ StrategyProfiles
✓ StrategyEngine
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer Logic
---
# Runtime Contract
1. Preset Strategy Logic'ni o'zgartirmaydi.
2. Preset faqat Configuration saqlaydi.
3. Har bir Preset Version'ga ega bo'lishi kerak.
4. Configuration immutable bo'lishi kerak.
5. Validation majburiy.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Preset yaratiladi.
✓ Validation muvaffaqiyatli bajariladi.
✓ Preset saqlanadi.
✓ Preset yuklanadi.
✓ StrategyEngine konfiguratsiyani qabul qiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Presets Contract GoldBot Strategy Layer ichidagi barcha foydalanuvchi va tizim Strategy Configuration'larini saqlovchi hamda boshqaruvchi rasmiy arxitektura shartnomasi hisoblanadi.
