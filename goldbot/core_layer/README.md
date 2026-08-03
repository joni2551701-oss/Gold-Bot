# 02_Core_Layer

Status: MIGRATING (Phase B) — Configuration ko'chirildi, qolgan modullar davom etmoqda.

Bu papka repository root'dagi Canonical Architecture'ning importga yaroqli aksi.

## Migratsiya holati

| Modul | Holat | Manba |
|---|---|---|
| `configuration` | ✅ MIGRATED | eski `configuration/` paketi |
| `secrets` | ✅ MIGRATED | eski `core/secrets.py` |
| `pipeline` | ✅ MIGRATED | eski `core/pipeline.py` |
| qolganlari | SKELETON | — |

## Canonical hujjatlar

- [Layer README](../../02_Core_Layer/README.md)
- [Layer Contracts](../../02_Core_Layer/Layer_Contracts.md)
- [Layer ModuleMap](../../02_Core_Layer/Layer_ModuleMap.md)
- [Layer DataFlow](../../02_Core_Layer/Layer_DataFlow.md)
- [Layer SequenceDiagram](../../02_Core_Layer/Layer_SequenceDiagram.md)

## Modullar (12)

| Python package | Canonical hujjat |
|---|---|
| `goldbot.core_layer.configuration` | [Configuration](../../02_Core_Layer/Configuration/README.md) |
| `goldbot.core_layer.core_engine` | [CoreEngine](../../02_Core_Layer/CoreEngine/README.md) |
| `goldbot.core_layer.core_service` | [CoreService](../../02_Core_Layer/CoreService/README.md) |
| `goldbot.core_layer.features` | [Features](../../02_Core_Layer/Features/README.md) |
| `goldbot.core_layer.health_monitor` | [HealthMonitor](../../02_Core_Layer/HealthMonitor/README.md) |
| `goldbot.core_layer.performance` | [Performance](../../02_Core_Layer/Performance/README.md) |
| `goldbot.core_layer.pipeline` | [Pipeline](../../02_Core_Layer/Pipeline/README.md) |
| `goldbot.core_layer.scheduler` | [Scheduler](../../02_Core_Layer/Scheduler/README.md) |
| `goldbot.core_layer.secrets` | [Secrets](../../02_Core_Layer/Secrets/README.md) |
| `goldbot.core_layer.service_registry` | [ServiceRegistry](../../02_Core_Layer/ServiceRegistry/README.md) |
| `goldbot.core_layer.shutdown` | [Shutdown](../../02_Core_Layer/Shutdown/README.md) |
| `goldbot.core_layer.startup` | [Startup](../../02_Core_Layer/Startup/README.md) |
