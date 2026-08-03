# 05_Strategy_Layer

Status: SKELETON (Phase A) — implementatsiya Phase B-E davomida qo'shiladi.

Bu papka `New_Map/` dagi Canonical Architecture'ning importga yaroqli aksi.
Biznes mantiq hali ko'chirilmagan.

## Canonical hujjatlar

- [Layer README](../../New_Map/05_Strategy_Layer/README.md)
- [Layer Contracts](../../New_Map/05_Strategy_Layer/Layer_Contracts.md)
- [Layer ModuleMap](../../New_Map/05_Strategy_Layer/Layer_ModuleMap.md)
- [Layer DataFlow](../../New_Map/05_Strategy_Layer/Layer_DataFlow.md)
- [Layer SequenceDiagram](../../New_Map/05_Strategy_Layer/Layer_SequenceDiagram.md)

## Modullar (17)

| Python package | Canonical hujjat |
|---|---|
| `goldbot.strategy_layer.strategy_engine` | [StrategyEngine](../../New_Map/05_Strategy_Layer/StrategyEngine/README.md) |
| `goldbot.strategy_layer.strategy_library.amd` | [StrategyLibrary/AMD](../../New_Map/05_Strategy_Layer/StrategyLibrary/AMD/README.md) |
| `goldbot.strategy_layer.strategy_library.breakout` | [StrategyLibrary/Breakout](../../New_Map/05_Strategy_Layer/StrategyLibrary/Breakout/README.md) |
| `goldbot.strategy_layer.strategy_library.ict` | [StrategyLibrary/ICT](../../New_Map/05_Strategy_Layer/StrategyLibrary/ICT/README.md) |
| `goldbot.strategy_layer.strategy_library.liquidity_sweep` | [StrategyLibrary/LiquiditySweep](../../New_Map/05_Strategy_Layer/StrategyLibrary/LiquiditySweep/README.md) |
| `goldbot.strategy_layer.strategy_library.mean_reversion` | [StrategyLibrary/MeanReversion](../../New_Map/05_Strategy_Layer/StrategyLibrary/MeanReversion/README.md) |
| `goldbot.strategy_layer.strategy_library.smc` | [StrategyLibrary/SMC](../../New_Map/05_Strategy_Layer/StrategyLibrary/SMC/README.md) |
| `goldbot.strategy_layer.strategy_library.trend_following` | [StrategyLibrary/TrendFollowing](../../New_Map/05_Strategy_Layer/StrategyLibrary/TrendFollowing/README.md) |
| `goldbot.strategy_layer.strategy_library.wyckoff` | [StrategyLibrary/Wyckoff](../../New_Map/05_Strategy_Layer/StrategyLibrary/Wyckoff/README.md) |
| `goldbot.strategy_layer.strategy_manager` | [StrategyManager](../../New_Map/05_Strategy_Layer/StrategyManager/README.md) |
| `goldbot.strategy_layer.strategy_profiles.filters` | [StrategyProfiles/Filters](../../New_Map/05_Strategy_Layer/StrategyProfiles/Filters/README.md) |
| `goldbot.strategy_layer.strategy_profiles.presets` | [StrategyProfiles/Presets](../../New_Map/05_Strategy_Layer/StrategyProfiles/Presets/README.md) |
| `goldbot.strategy_layer.strategy_profiles.risk_profiles` | [StrategyProfiles/RiskProfiles](../../New_Map/05_Strategy_Layer/StrategyProfiles/RiskProfiles/README.md) |
| `goldbot.strategy_layer.strategy_profiles.sessions` | [StrategyProfiles/Sessions](../../New_Map/05_Strategy_Layer/StrategyProfiles/Sessions/README.md) |
| `goldbot.strategy_layer.strategy_profiles.timeframes` | [StrategyProfiles/Timeframes](../../New_Map/05_Strategy_Layer/StrategyProfiles/Timeframes/README.md) |
| `goldbot.strategy_layer.strategy_profiles.trading_styles` | [StrategyProfiles/TradingStyles](../../New_Map/05_Strategy_Layer/StrategyProfiles/TradingStyles/README.md) |
| `goldbot.strategy_layer.strategy_service` | [StrategyService](../../New_Map/05_Strategy_Layer/StrategyService/README.md) |
