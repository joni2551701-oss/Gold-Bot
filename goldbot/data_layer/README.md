# 01_Data_Layer

Status: SKELETON (Phase A) — implementatsiya Phase B-E davomida qo'shiladi.

Bu papka `New_Map/` dagi Canonical Architecture'ning importga yaroqli aksi.
Biznes mantiq hali ko'chirilmagan.

## Canonical hujjatlar

- [Layer README](../../New_Map/01_Data_Layer/README.md)
- [Layer Contracts](../../New_Map/01_Data_Layer/Layer_Contracts.md)
- [Layer ModuleMap](../../New_Map/01_Data_Layer/Layer_ModuleMap.md)
- [Layer DataFlow](../../New_Map/01_Data_Layer/Layer_DataFlow.md)
- [Layer SequenceDiagram](../../New_Map/01_Data_Layer/Layer_SequenceDiagram.md)

## Modullar (38)

| Python package | Canonical hujjat |
|---|---|
| `goldbot.data_layer.data_validation.data_validator` | [Data_Validation/DataValidator](../../New_Map/01_Data_Layer/Data_Validation/DataValidator/README.md) |
| `goldbot.data_layer.data_validation.integrity_validator` | [Data_Validation/IntegrityValidator](../../New_Map/01_Data_Layer/Data_Validation/IntegrityValidator/README.md) |
| `goldbot.data_layer.data_validation.quality_validator` | [Data_Validation/QualityValidator](../../New_Map/01_Data_Layer/Data_Validation/QualityValidator/README.md) |
| `goldbot.data_layer.data_validation.schema_validator` | [Data_Validation/SchemaValidator](../../New_Map/01_Data_Layer/Data_Validation/SchemaValidator/README.md) |
| `goldbot.data_layer.data_validation.validation_lifecycle` | [Data_Validation/ValidationLifecycle](../../New_Map/01_Data_Layer/Data_Validation/ValidationLifecycle/README.md) |
| `goldbot.data_layer.data_validation.validation_service` | [Data_Validation/ValidationService](../../New_Map/01_Data_Layer/Data_Validation/ValidationService/README.md) |
| `goldbot.data_layer.event_system.event_bus` | [Event_System/EventBus](../../New_Map/01_Data_Layer/Event_System/EventBus/README.md) |
| `goldbot.data_layer.event_system.event_dispatcher` | [Event_System/EventDispatcher](../../New_Map/01_Data_Layer/Event_System/EventDispatcher/README.md) |
| `goldbot.data_layer.event_system.event_lifecycle` | [Event_System/EventLifecycle](../../New_Map/01_Data_Layer/Event_System/EventLifecycle/README.md) |
| `goldbot.data_layer.event_system.event_publisher` | [Event_System/EventPublisher](../../New_Map/01_Data_Layer/Event_System/EventPublisher/README.md) |
| `goldbot.data_layer.event_system.event_service` | [Event_System/EventService](../../New_Map/01_Data_Layer/Event_System/EventService/README.md) |
| `goldbot.data_layer.event_system.event_subscriber` | [Event_System/EventSubscriber](../../New_Map/01_Data_Layer/Event_System/EventSubscriber/README.md) |
| `goldbot.data_layer.historical_data.bootstrap` | [Historical_Data/Bootstrap](../../New_Map/01_Data_Layer/Historical_Data/Bootstrap/README.md) |
| `goldbot.data_layer.historical_data.historical_data_flow` | [Historical_Data/HistoricalDataFlow](../../New_Map/01_Data_Layer/Historical_Data/HistoricalDataFlow/README.md) |
| `goldbot.data_layer.historical_data.historical_data_service` | [Historical_Data/HistoricalDataService](../../New_Map/01_Data_Layer/Historical_Data/HistoricalDataService/README.md) |
| `goldbot.data_layer.historical_data.historical_database` | [Historical_Data/HistoricalDatabase](../../New_Map/01_Data_Layer/Historical_Data/HistoricalDatabase/README.md) |
| `goldbot.data_layer.historical_data.historical_providers` | [Historical_Data/HistoricalProviders](../../New_Map/01_Data_Layer/Historical_Data/HistoricalProviders/README.md) |
| `goldbot.data_layer.historical_data.recovery` | [Historical_Data/Recovery](../../New_Map/01_Data_Layer/Historical_Data/Recovery/README.md) |
| `goldbot.data_layer.live_data.candle_builder` | [Live_Data/CandleBuilder](../../New_Map/01_Data_Layer/Live_Data/CandleBuilder/README.md) |
| `goldbot.data_layer.live_data.current_price_provider` | [Live_Data/CurrentPriceProvider](../../New_Map/01_Data_Layer/Live_Data/CurrentPriceProvider/README.md) |
| `goldbot.data_layer.live_data.live_data_flow` | [Live_Data/LiveDataFlow](../../New_Map/01_Data_Layer/Live_Data/LiveDataFlow/README.md) |
| `goldbot.data_layer.live_data.live_data_service` | [Live_Data/LiveDataService](../../New_Map/01_Data_Layer/Live_Data/LiveDataService/README.md) |
| `goldbot.data_layer.live_data.live_providers` | [Live_Data/LiveProviders](../../New_Map/01_Data_Layer/Live_Data/LiveProviders/README.md) |
| `goldbot.data_layer.live_data.market_calendar` | [Live_Data/MarketCalendar](../../New_Map/01_Data_Layer/Live_Data/MarketCalendar/README.md) |
| `goldbot.data_layer.live_data.price_stream_service` | [Live_Data/PriceStreamService](../../New_Map/01_Data_Layer/Live_Data/PriceStreamService/README.md) |
| `goldbot.data_layer.live_data.stream_validator` | [Live_Data/StreamValidator](../../New_Map/01_Data_Layer/Live_Data/StreamValidator/README.md) |
| `goldbot.data_layer.market_memory.market_memory_service` | [Market_Memory/MarketMemoryService](../../New_Map/01_Data_Layer/Market_Memory/MarketMemoryService/README.md) |
| `goldbot.data_layer.market_memory.memory_cache` | [Market_Memory/MemoryCache](../../New_Map/01_Data_Layer/Market_Memory/MemoryCache/README.md) |
| `goldbot.data_layer.market_memory.memory_lifecycle` | [Market_Memory/MemoryLifecycle](../../New_Map/01_Data_Layer/Market_Memory/MemoryLifecycle/README.md) |
| `goldbot.data_layer.market_memory.memory_reader` | [Market_Memory/MemoryReader](../../New_Map/01_Data_Layer/Market_Memory/MemoryReader/README.md) |
| `goldbot.data_layer.market_memory.memory_storage` | [Market_Memory/MemoryStorage](../../New_Map/01_Data_Layer/Market_Memory/MemoryStorage/README.md) |
| `goldbot.data_layer.market_memory.memory_writer` | [Market_Memory/MemoryWriter](../../New_Map/01_Data_Layer/Market_Memory/MemoryWriter/README.md) |
| `goldbot.data_layer.providers.bitget` | [Providers/Bitget](../../New_Map/01_Data_Layer/Providers/Bitget/README.md) |
| `goldbot.data_layer.providers.provider_factory` | [Providers/ProviderFactory](../../New_Map/01_Data_Layer/Providers/ProviderFactory/README.md) |
| `goldbot.data_layer.providers.provider_flow` | [Providers/ProviderFlow](../../New_Map/01_Data_Layer/Providers/ProviderFlow/README.md) |
| `goldbot.data_layer.providers.provider_interface` | [Providers/ProviderInterface](../../New_Map/01_Data_Layer/Providers/ProviderInterface/README.md) |
| `goldbot.data_layer.providers.provider_lifecycle` | [Providers/ProviderLifecycle](../../New_Map/01_Data_Layer/Providers/ProviderLifecycle/README.md) |
| `goldbot.data_layer.providers.twelve_data` | [Providers/TwelveData](../../New_Map/01_Data_Layer/Providers/TwelveData/README.md) |
