# Database Layer
Status: CANONICAL
---
# Purpose
Database Layer GoldBot arxitekturasidagi Canonical Persistent Storage Layer hisoblanadi.
Uning asosiy vazifasi GoldBot tizimining barcha doimiy ma'lumotlarini xavfsiz saqlash, boshqarish, tiklash va boshqa Layer'larga standart Database Service orqali taqdim etishdir.
Database Layer Trading Decision qabul qilmaydi.
Database Layer Order Execution bajarmaydi.
Database Layer faqat ma'lumotlarni saqlash va boshqarish bilan shug'ullanadi.
---
# Objective
Database Layer quyidagi vazifalarni bajaradi.
• Database Management
• Trade Storage
• User Storage
• Market Data Storage
• AI Journal Storage
• Cache Management
• Backup & Restore
---
# Layer Position
```text
Trade Monitoring Layer
↓
Database Layer
↓
Platform Layer
```
---
# Internal Modules
```text
Database Layer
├── DatabaseManager
├── TradeRepository
├── UserRepository
├── MarketRepository
├── JournalRepository
├── CacheManager
├── BackupManager
└── DatabaseService
```
---
# Responsibilities
Database Layer
✓ Database Connection boshqaradi
✓ Trade History saqlaydi
✓ User ma'lumotlarini saqlaydi
✓ Market Data saqlaydi
✓ AI Journal saqlaydi
✓ Cache boshqaradi
✓ Backup yaratadi
✓ Restore bajaradi
---
# Not Responsible
Database Layer
✗ Signal Generation
✗ AI Analysis
✗ Trading Decision
✗ Risk Calculation
✗ Order Execution
✗ Position Monitoring
---
# Input
Database Layer qabul qiladi.
• Trade Data
• User Data
• Market Data
• Journal Data
• Cache Data
• Backup Request
---
# Output
Database Layer yaratadi.
• Database Records
• Query Results
• Cache Response
• Backup Files
• Database Metadata
---
# Data Categories
```text
Trade Data
↓
User Data
↓
Market Data
↓
AI Journal
↓
Cache
↓
Backup
```
---
# Workflow
```text
Receive Database Request
↓
DatabaseService
↓
DatabaseManager
↓
Repository Processing
↓
Cache Update
↓
Backup Check
↓
Return Response
↓
Platform Layer
```
---
# Golden Rules
1. Database Layer barcha Persistent Data uchun yagona manba hisoblanadi.
2. Har bir Repository faqat o'z domeni bilan ishlaydi.
3. Cache doimo Database bilan sinxron bo'lishi shart.
4. Backup muntazam yaratilishi shart.
5. Database Transaction atomik bo'lishi shart.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
12_Database_Layer/
├── README.md
├── DatabaseManager/
├── TradeRepository/
├── UserRepository/
├── MarketRepository/
├── JournalRepository/
├── CacheManager/
├── BackupManager/
├── DatabaseService/
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md
```
---
# Summary
Database Layer GoldBot arxitekturasidagi Canonical Persistent Storage Layer hisoblanadi.
Trade Monitoring Layer barcha Runtime ma'lumotlarini Database Layer'ga uzatadi.
Database Layer esa ushbu ma'lumotlarni xavfsiz saqlaydi, Cache va Backup'ni boshqaradi hamda Platform Layer uchun ishonchli ma'lumot manbai sifatida xizmat qiladi.
