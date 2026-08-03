# 02_Core_Layer

Status: MIGRATING (Phase B) — Configuration ko'chirildi, qolgan modullar davom etmoqda.

Bu papka `New_Map/` dagi Canonical Architecture'ning importga yaroqli aksi.

## Migratsiya holati

| Modul | Holat | Manba |
|---|---|---|
| `configuration` | ✅ MIGRATED | eski `configuration/` paketi |
| qolganlari | SKELETON | — |

## Canonical hujjatlar

- [Layer README](../../New_Map/02_Core_Layer/README.md)
- [Layer Contracts](../../New_Map/02_Core_Layer/Layer_Contracts.md)
- [Layer ModuleMap](../../New_Map/02_Core_Layer/Layer_ModuleMap.md)
- [Layer DataFlow](../../New_Map/02_Core_Layer/Layer_DataFlow.md)
- [Layer SequenceDiagram](../../New_Map/02_Core_Layer/Layer_SequenceDiagram.md)

## Modullar (12)

| Python package | Canonical hujjat |
|---|---|
| `goldbot.core_layer.configuration` | [Configuration](../../New_Map/02_Core_Layer/Configuration/README.md) |
| `goldbot.core_layer.core_engine` | [CoreEngine](../../New_Map/02_Core_Layer/CoreEngine/README.md) |
| `goldbot.core_layer.core_service` | [CoreService](../../New_Map/02_Core_Layer/CoreService/README.md) |
| `goldbot.core_layer.features` | [Features](../../New_Map/02_Core_Layer/Features/README.md) |
| `goldbot.core_layer.health_monitor` | [HealthMonitor](../../New_Map/02_Core_Layer/HealthMonitor/README.md) |
| `goldbot.core_layer.performance` | [Performance](../../New_Map/02_Core_Layer/Performance/README.md) |
| `goldbot.core_layer.pipeline` | [Pipeline](../../New_Map/02_Core_Layer/Pipeline/README.md) |
| `goldbot.core_layer.scheduler` | [Scheduler](../../New_Map/02_Core_Layer/Scheduler/README.md) |
| `goldbot.core_layer.secrets` | [Secrets](../../New_Map/02_Core_Layer/Secrets/README.md) |
| `goldbot.core_layer.service_registry` | [ServiceRegistry](../../New_Map/02_Core_Layer/ServiceRegistry/README.md) |
| `goldbot.core_layer.shutdown` | [Shutdown](../../New_Map/02_Core_Layer/Shutdown/README.md) |
| `goldbot.core_layer.startup` | [Startup](../../New_Map/02_Core_Layer/Startup/README.md) |
