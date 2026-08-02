# Database Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat GoldBot Database Layer ichidagi ma'lumotlar oqimini (Data Flow) tavsiflaydi.
Database Layer GoldBot tizimidagi barcha Persistent Data'ni qabul qiladi, saqlaydi, yangilaydi va Platform Layer hamda boshqa Layer'larga ishonchli tarzda taqdim etadi.
---
# Layer Data Flow
```text
Trade Monitoring Layer
        │
        ▼
DatabaseService (Entry)
        │
        ▼
DatabaseManager
        │
        ├──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
TradeRepository  UserRepository  MarketRepository  JournalRepository
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                       │
                       ▼
                 CacheManager
                       │
                       ▼
                 BackupManager
                       │
                       ▼
                 DatabaseService (Exit)
                       │
                       ▼
                 Platform Layer
```
---
# Input Sources
• Trade Data
• User Data
• Market Data
• AI Journal
• Audit Log
• Cache Request
• Backup Request
---
# Output
• Database Records
• Query Results
• Cache Response
• Backup Archive
• Repository Metadata
• Database Metadata
---
# Data Flow Rules
1. Barcha Database Request'lar DatabaseService orqali o'tadi.
2. DatabaseManager Connection va Transaction'ni boshqaradi.
3. Repository faqat o'z Domain Data'si bilan ishlaydi.
4. Cache Database bilan sinxron bo'lishi shart.
5. Backup faqat Persistent Data'dan yaratiladi.
6. BackupManager Layer tashqarisiga chiqmaydi — natija DatabaseService orqali Platform Layer'ga uzatiladi.
---
# Summary
Database Layer GoldBot arxitekturasidagi Canonical Persistent Storage Pipeline hisoblanadi.
