# 01_Data_Layer

Status: SKELETON (Phase A) — implementatsiya Phase B-E davomida qo'shiladi.

Bu papka repository root'dagi Canonical Architecture'ning importga yaroqli aksi.
Biznes mantiq hali ko'chirilmagan.

## Canonical hujjatlar

- [Layer README](../../01_Data_Layer/README.md)
- [Layer Contracts](../../01_Data_Layer/Layer_Contracts.md)
- [Layer ModuleMap](../../01_Data_Layer/Layer_ModuleMap.md)
- [Layer DataFlow](../../01_Data_Layer/Layer_DataFlow.md)
- [Layer SequenceDiagram](../../01_Data_Layer/Layer_SequenceDiagram.md)

## Modullar (38)

| Python package | Canonical hujjat |
|---|---|
| `goldbot.data_layer.data_validation.data_validator` | [Data_Validation/DataValidator](../../01_Data_Layer/Data_Validation/DataValidator/README.md) |
| `goldbot.data_layer.data_validation.integrity_validator` | [Data_Validation/IntegrityValidator](../../01_Data_Layer/Data_Validation/IntegrityValidator/README.md) |
| `goldbot.data_layer.data_validation.quality_validator` | [Data_Validation/QualityValidator](../../01_Data_Layer/Data_Validation/QualityValidator/README.md) |
| `goldbot.data_layer.data_validation.schema_validator` | [Data_Validation/SchemaValidator](../../01_Data_Layer/Data_Validation/SchemaValidator/README.md) |
| `goldbot.data_layer.data_validation.validation_lifecycle` | [Data_Validation/ValidationLifecycle](../../01_Data_Layer/Data_Validation/ValidationLifecycle/README.md) |
| `goldbot.data_layer.data_validation.validation_service` | [Data_Validation/ValidationService](../../01_Data_Layer/Data_Validation/ValidationService/README.md) |
| `goldbot.data_layer.event_system.event_bus` | [Event_System/EventBus](../../01_Data_Layer/Event_System/EventBus/README.md) |
| `goldbot.data_layer.event_system.event_dispatcher` | [Event_System/EventDispatcher](../../01_Data_Layer/Event_System/EventDispatcher/README.md) |
| `goldbot.data_layer.event_system.event_lifecycle` | [Event_System/EventLifecycle](../../01_Data_Layer/Event_System/EventLifecycle/README.md) |
| `goldbot.data_layer.event_system.event_publisher` | [Event_System/EventPublisher](../../01_Data_Layer/Event_System/EventPublisher/README.md) |
| `goldbot.data_layer.event_system.event_service` | [Event_System/EventService](../../01_Data_Layer/Event_System/EventService/README.md) |
| `goldbot.data_layer.event_system.event_subscriber` | [Event_System/EventSubscriber](../../01_Data_Layer/Event_System/EventSubscriber/README.md) |
| `goldbot.data_layer.historical_data.bootstrap` | [Historical_Data/Bootstrap](../../01_Data_Layer/Historical_Data/Bootstrap/README.md) |
| `goldbot.data_layer.historical_data.historical_data_flow` | [Historical_Data/HistoricalDataFlow](../../01_Data_Layer/Historical_Data/HistoricalDataFlow/README.md) |
| `goldbot.data_layer.historical_data.historical_data_service` | [Historical_Data/HistoricalDataService](../../01_Data_Layer/Historical_Data/HistoricalDataService/README.md) |
| `goldbot.data_layer.historical_data.historical_database` | [Historical_Data/HistoricalDatabase](../../01_Data_Layer/Historical_Data/HistoricalDatabase/README.md) |
| `goldbot.data_layer.historical_data.historical_providers` | [Historical_Data/HistoricalProviders](../../01_Data_Layer/Historical_Data/HistoricalProviders/README.md) |
| `goldbot.data_layer.historical_data.recovery` | [Historical_Data/Recovery](../../01_Data_Layer/Historical_Data/Recovery/README.md) |
| `goldbot.data_layer.live_data.candle_builder` | [Live_Data/CandleBuilder](../../01_Data_Layer/Live_Data/CandleBuilder/README.md) |
| `goldbot.data_layer.live_data.current_price_provider` | [Live_Data/CurrentPriceProvider](../../01_Data_Layer/Live_Data/CurrentPriceProvider/README.md) |
| `goldbot.data_layer.live_data.live_data_flow` | [Live_Data/LiveDataFlow](../../01_Data_Layer/Live_Data/LiveDataFlow/README.md) |
| `goldbot.data_layer.live_data.live_data_service` | [Live_Data/LiveDataService](../../01_Data_Layer/Live_Data/LiveDataService/README.md) |
| `goldbot.data_layer.live_data.live_providers` | [Live_Data/LiveProviders](../../01_Data_Layer/Live_Data/LiveProviders/README.md) |
| `goldbot.data_layer.live_data.market_calendar` | [Live_Data/MarketCalendar](../../01_Data_Layer/Live_Data/MarketCalendar/README.md) |
| `goldbot.data_layer.live_data.price_stream_service` | [Live_Data/PriceStreamService](../../01_Data_Layer/Live_Data/PriceStreamService/README.md) |
| `goldbot.data_layer.live_data.stream_validator` | [Live_Data/StreamValidator](../../01_Data_Layer/Live_Data/StreamValidator/README.md) |
| `goldbot.data_layer.market_memory.market_memory_service` | [Market_Memory/MarketMemoryService](../../01_Data_Layer/Market_Memory/MarketMemoryService/README.md) |
| `goldbot.data_layer.market_memory.memory_cache` | [Market_Memory/MemoryCache](../../01_Data_Layer/Market_Memory/MemoryCache/README.md) |
| `goldbot.data_layer.market_memory.memory_lifecycle` | [Market_Memory/MemoryLifecycle](../../01_Data_Layer/Market_Memory/MemoryLifecycle/README.md) |
| `goldbot.data_layer.market_memory.memory_reader` | [Market_Memory/MemoryReader](../../01_Data_Layer/Market_Memory/MemoryReader/README.md) |
| `goldbot.data_layer.market_memory.memory_storage` | [Market_Memory/MemoryStorage](../../01_Data_Layer/Market_Memory/MemoryStorage/README.md) |
| `goldbot.data_layer.market_memory.memory_writer` | [Market_Memory/MemoryWriter](../../01_Data_Layer/Market_Memory/MemoryWriter/README.md) |
| `goldbot.data_layer.providers.bitget` | [Providers/Bitget](../../01_Data_Layer/Providers/Bitget/README.md) |
| `goldbot.data_layer.providers.provider_factory` | [Providers/ProviderFactory](../../01_Data_Layer/Providers/ProviderFactory/README.md) |
| `goldbot.data_layer.providers.provider_flow` | [Providers/ProviderFlow](../../01_Data_Layer/Providers/ProviderFlow/README.md) |
| `goldbot.data_layer.providers.provider_interface` | [Providers/ProviderInterface](../../01_Data_Layer/Providers/ProviderInterface/README.md) |
| `goldbot.data_layer.providers.provider_lifecycle` | [Providers/ProviderLifecycle](../../01_Data_Layer/Providers/ProviderLifecycle/README.md) |
| `goldbot.data_layer.providers.twelve_data` | [Providers/TwelveData](../../01_Data_Layer/Providers/TwelveData/README.md) |
