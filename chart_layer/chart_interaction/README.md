# Chart Interaction
Status: BLUEPRINT
---
# Purpose
Chart_Interaction GoldBot Chart Layer ichidagi Canonical Chart Interaction moduli hisoblanadi.
Mouse, Keyboard, Touch, Zoom, Pan, Drag va Selection'ni boshqaruvchi Canonical User Interaction moduli.
Chart_Interaction Signal yaratmaydi.
Chart_Interaction BOS/CHoCH hisoblamaydi.
Chart_Interaction AI ishlatmaydi.
Chart_Interaction Risk hisoblamaydi.
---
# Objective
Chart_Interaction quyidagi vazifalarni bajaradi.
• Mouse Handling
• Keyboard Handling
• Touch Handling
• Zoom Management
• Pan Management
• Drag Management
• Selection Management
• Hotkey Management
---
# Layer Position
```text
Chart_Renderer
↓
Chart_Interaction
↓
Objects
```
---
# Responsibilities
Chart_Interaction
✓ Mouse hodisalarini qabul qiladi
✓ Keyboard hodisalarini qabul qiladi
✓ Touch hodisalarini qabul qiladi
✓ Zoom/Pan/Drag'ni boshqaradi
✓ Selection'ni boshqaradi
---
# Not Responsible
Chart_Interaction
✗ Rendering
✗ Data Calculation
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ Drawing Tool Logic (Drawing_Tools vazifasi)
---
# Input
Chart_Interaction qabul qiladi.
• Mouse Event
• Keyboard Event
• Touch Event
• Gesture Event
---
# Output
Chart_Interaction yaratadi.
• Interaction Context
• Zoom State
• Pan State
• Selection State
---
# Workflow
```text
Chart_Renderer
↓
Chart_Interaction
↓
Objects
```
---
# Internal Modules (Planned — Foundation Freeze'dan keyin implementatsiya qilinadi)
```text
Chart_Interaction
├── Mouse/
├── Keyboard/
├── Touch/
├── Zoom/
├── Pan/
├── Drag/
├── Selection/
└── Hotkeys/
```
---
# Golden Rules
1. Chart_Interaction faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Modules
```text
Chart_Interaction/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
Predecessor: Chart_Renderer · Successor: Objects
---
# Summary
Chart_Interaction GoldBot Chart Layer ichidagi Chart Interaction vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, yuqoridagi Internal Modules ro'yxati Foundation Freeze'dan keyin haqiqiy implementatsiya bilan to'ldiriladi.
