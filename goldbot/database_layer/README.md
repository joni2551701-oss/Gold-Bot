# 12_Database_Layer

Status: SKELETON (Phase A) — implementatsiya Phase B-E davomida qo'shiladi.

Bu papka `New_Map/` dagi Canonical Architecture'ning importga yaroqli aksi.
Biznes mantiq hali ko'chirilmagan.

## Canonical hujjatlar

- [Layer README](../../New_Map/12_Database_Layer/README.md)
- [Layer Contracts](../../New_Map/12_Database_Layer/Layer_Contracts.md)
- [Layer ModuleMap](../../New_Map/12_Database_Layer/Layer_ModuleMap.md)
- [Layer DataFlow](../../New_Map/12_Database_Layer/Layer_DataFlow.md)
- [Layer SequenceDiagram](../../New_Map/12_Database_Layer/Layer_SequenceDiagram.md)

## Modullar (9)

| Python package | Canonical hujjat |
|---|---|
| `goldbot.database_layer.audit_log` | [AuditLog](../../New_Map/12_Database_Layer/AuditLog/README.md) |
| `goldbot.database_layer.backup_manager` | [BackupManager](../../New_Map/12_Database_Layer/BackupManager/README.md) |
| `goldbot.database_layer.cache_manager` | [CacheManager](../../New_Map/12_Database_Layer/CacheManager/README.md) |
| `goldbot.database_layer.database_manager` | [DatabaseManager](../../New_Map/12_Database_Layer/DatabaseManager/README.md) |
| `goldbot.database_layer.database_service` | [DatabaseService](../../New_Map/12_Database_Layer/DatabaseService/README.md) |
| `goldbot.database_layer.journal_repository` | [JournalRepository](../../New_Map/12_Database_Layer/JournalRepository/README.md) |
| `goldbot.database_layer.market_repository` | [MarketRepository](../../New_Map/12_Database_Layer/MarketRepository/README.md) |
| `goldbot.database_layer.trade_repository` | [TradeRepository](../../New_Map/12_Database_Layer/TradeRepository/README.md) |
| `goldbot.database_layer.user_repository` | [UserRepository](../../New_Map/12_Database_Layer/UserRepository/README.md) |
