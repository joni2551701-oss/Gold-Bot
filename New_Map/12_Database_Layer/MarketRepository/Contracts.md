# Market Repository Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat MarketRepository modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
MarketRepository quyidagilar uchun javobgar.
✓ Market Data Storage
✓ Candle Storage
✓ Tick Storage
✓ Indicator Storage
✓ Context Storage
✓ Signal History Storage
✓ Market Query Processing
MarketRepository bajarmaydi.
✗ Trading Decision
✗ Strategy Analysis
✗ AI Analysis
✗ Trade Storage
✗ User Storage
✗ Cache Management
---
# Module Boundary
```text
DatabaseManager
↓
MarketRepository
↓
Database Storage
```
---
# Input Contract
• Candle Record
• Tick Record
• Indicator Record
• Context Record
• Query Request
---
# Output Contract
• Market Result
• Historical Data
• Query Result
• Repository Metadata
---
# Allowed Dependencies
✓ DatabaseManager
✓ Database Storage
---
# Forbidden Dependencies
✗ TradeRepository
✗ UserRepository
✗ JournalRepository
✗ AuditLog
✗ CacheManager
✗ BackupManager
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Candle ma'lumotlari vaqt bo'yicha tartiblangan holda saqlanishi shart.
2. Tick Data ketma-ketligi buzilmasligi shart.
3. Indicator va Context yozuvlari tegishli Timeframe bilan bog'lanishi shart.
4. Signal History immutable saqlanishi shart.
5. Query natijalari standart formatda qaytarilishi shart.
6. MarketRepository Business Logic bajarmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Candle saqlanadi.
✓ Tick saqlanadi.
✓ Indicator saqlanadi.
✓ Context saqlanadi.
✓ Signal History saqlanadi.
✓ Query bajariladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
MarketRepository Contract GoldBot Database Layer ichidagi Market Data, Candle, Tick, Indicator, Context va Signal History ma'lumotlarini ishonchli saqlash, yangilash va qidirishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
