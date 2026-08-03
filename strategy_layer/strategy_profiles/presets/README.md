# Presets
Status: CANONICAL
---
# Purpose
Presets GoldBot Strategy Layer ichidagi foydalanuvchi va tizim tomonidan oldindan tayyorlangan Strategy Configuration'larni boshqaruvchi Canonical modul hisoblanadi.
Preset strategiya emas.
Preset bir nechta konfiguratsiyani yagona profil sifatida saqlaydi.
---
# Objective
Presets quyidagi vazifalarni bajaradi.
• Preset Creation
• Preset Loading
• Preset Saving
• Preset Validation
• Preset Versioning
• Preset Management
---
# Preset Components
Har bir Preset quyidagilarni o'z ichiga olishi mumkin.
• Strategy
• Trading Style
• Session
• Timeframe
• Risk Profile
• Filters
• User Preferences
---
# Responsibilities
Presets
✓ Strategy Configuration saqlaydi
✓ Preset yuklaydi
✓ Preset yangilaydi
✓ Preset Validation bajaradi
✓ StrategyManager uchun tayyor konfiguratsiya beradi
---
# Not Responsible
Presets
✗ Strategy Logic
✗ Indicator Calculation
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk Calculation
✗ Trade Execution
---
# Input
• User Configuration
• System Configuration
---
# Output
• Strategy Preset
• Strategy Configuration
---
# Workflow
```text
User Configuration
↓
Build Preset
↓
Validate
↓
Save
↓
Load
↓
StrategyManager
```
---
# Golden Rules
1. Preset Strategy Logic'ni o'zgartirmaydi.
2. Preset faqat Configuration hisoblanadi.
3. Preset Version qo'llab-quvvatlanadi.
4. Configuration immutable hisoblanadi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Presets/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Presets GoldBot Strategy Layer ichidagi barcha Strategy Configuration'larni saqlovchi Canonical modul hisoblanadi.
