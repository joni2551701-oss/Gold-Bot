# 10_Execution_Layer

Status: SKELETON (Phase A) — implementatsiya Phase B-E davomida qo'shiladi.

Bu papka `New_Map/` dagi Canonical Architecture'ning importga yaroqli aksi.
Biznes mantiq hali ko'chirilmagan.

## Canonical hujjatlar

- [Layer README](../../New_Map/10_Execution_Layer/README.md)
- [Layer Contracts](../../New_Map/10_Execution_Layer/Layer_Contracts.md)
- [Layer ModuleMap](../../New_Map/10_Execution_Layer/Layer_ModuleMap.md)
- [Layer DataFlow](../../New_Map/10_Execution_Layer/Layer_DataFlow.md)
- [Layer SequenceDiagram](../../New_Map/10_Execution_Layer/Layer_SequenceDiagram.md)

## Modullar (7)

| Python package | Canonical hujjat |
|---|---|
| `goldbot.execution_layer.broker_gateway` | [BrokerGateway](../../New_Map/10_Execution_Layer/BrokerGateway/README.md) |
| `goldbot.execution_layer.execution_engine` | [ExecutionEngine](../../New_Map/10_Execution_Layer/ExecutionEngine/README.md) |
| `goldbot.execution_layer.execution_monitor` | [ExecutionMonitor](../../New_Map/10_Execution_Layer/ExecutionMonitor/README.md) |
| `goldbot.execution_layer.execution_service` | [ExecutionService](../../New_Map/10_Execution_Layer/ExecutionService/README.md) |
| `goldbot.execution_layer.order_manager` | [OrderManager](../../New_Map/10_Execution_Layer/OrderManager/README.md) |
| `goldbot.execution_layer.order_router` | [OrderRouter](../../New_Map/10_Execution_Layer/OrderRouter/README.md) |
| `goldbot.execution_layer.order_validator` | [OrderValidator](../../New_Map/10_Execution_Layer/OrderValidator/README.md) |
