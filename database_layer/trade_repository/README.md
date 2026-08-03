# Trade Repository
Status: CANONICAL
---
# Purpose
TradeRepository GoldBot Database Layer ichidagi Canonical Trade Persistence moduli hisoblanadi.
Uning asosiy vazifasi barcha Trade, Order, Position va Execution ma'lumotlarini Database'da saqlash, yangilash va o'qishdir.
TradeRepository Business Logic bajarmaydi.
TradeRepository Trading Decision qabul qilmaydi.
TradeRepository faqat Trade Domain ma'lumotlari bilan ishlaydi.
---
# Objective
TradeRepository quyidagi vazifalarni bajaradi.
• Trade Storage
• Order Storage
• Position Storage
• Execution Storage
• Trade History Management
• Trade Query Processing
---
# Layer Position
```text
DatabaseManager
↓
TradeRepository
↓
Database Storage
```
---
# Responsibilities
TradeRepository
✓ Trade saqlaydi
✓ Order saqlaydi
✓ Position saqlaydi
✓ Execution natijalarini saqlaydi
✓ Trade History yaratadi
✓ Trade Query bajaradi
---
# Not Responsible
TradeRepository
✗ Trading Decision
✗ Risk Calculation
✗ Market Data Storage
✗ User Storage
✗ Cache Management
✗ Backup Management
---
# Input
TradeRepository qabul qiladi.
• Trade Record
• Order Record
• Position Record
• Execution Record
• Query Request
---
# Output
TradeRepository yaratadi.
• Trade Result
• Trade History
• Query Result
• Repository Metadata
---
# Workflow
```text
Receive Repository Request
↓
Validate Data
↓
Persist Trade Data
↓
Execute Query
↓
Return Repository Result
```
---
# Internal Storage (Real Implementations)
Domen: Savdo va risk domeni.
Repository Aggregation Rule (RAR-001): Database Layer'da repository soni biznes obyektlari soniga teng bo'lishi shart emas. Quyidagi storage implementatsiyalari alohida modul emas — ular shu Repository modulining ichki mas'uliyati hisoblanadi.
```text
TradeRepository
├── signal
├── risk_decision
├── risk_state
└── emergency
```
| Storage | Mas'uliyat |
|---|---|
| `signal` | Signal yozuvlari (SignalRecord) |
| `risk_decision` | Risk qarorlari tarixi (append-only) |
| `risk_state` | Symbol bo'yicha risk hisob holati (upsert) |
| `emergency` | Emergency holat o'tishlari (KILLED va h.k., append-only) |
---
# Golden Rules
1. Har bir Trade Unique ID bilan saqlanishi shart.
2. Trade History o'zgartirilmaydi.
3. Position holati doimo yangilanadi.
4. Execution natijalari audit uchun saqlanadi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
TradeRepository/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
TradeRepository GoldBot Database Layer ichidagi barcha Trade, Order, Position va Execution ma'lumotlarini boshqaruvchi Canonical Repository moduli hisoblanadi.
