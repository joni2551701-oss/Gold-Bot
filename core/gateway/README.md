# core/gateway — Core Gateway Layer (v1.1 Phase 1, Module 10)

The **single entry point** into Core. Every external client reaches a Core
service through the Gateway, never by importing the service directly.

Full design: [`docs/CORE_GATEWAY_ARCHITECTURE.md`](../../docs/CORE_GATEWAY_ARCHITECTURE.md).

## Quick start

```python
from core.gateway import (
    CoreGateway, ServiceManifest, GatewayRequest,
)

gw = CoreGateway()

def market_memory_handler(ctx, payload):
    # ctx: GatewayContext (request_id, principal, timestamp, versions...)
    return {"asset": payload}

gw.register_service(
    ServiceManifest(name="MarketMemory", capabilities=("MarketMemory",)),
    market_memory_handler)
gw.register_service(
    ServiceManifest(name="Replay", capabilities=("Replay",),
                    dependencies=("MarketMemory",)),
    lambda ctx, payload: ...)

gw.start()                                   # validates deps, brings up READY
resp = gw.dispatch(GatewayRequest(service="Replay", payload="XAUUSD"))
assert resp.ok

gw.find(capability="Replay")                 # capability discovery
gw.health_report(); gw.metrics_snapshot(); gw.version_info()
```

## What it is / is not

- **Is:** service registry + discovery, lifecycle state machine, per-service
  circuit breaker, authentication + authorization + rate limiting, standard
  per-request context, health/metrics/version endpoints.
- **Is not:** trading logic. It holds no Strategy/Decision/Signal/Risk code,
  offers no execution route, and is **not** wired into `core/pipeline.py`.

## Boundaries

Transport-independent (in-process now; HTTP/WS/gRPC/IPC later). Imports
nothing from `data/`, `strategies/`, `signals/`, `decision/`, `risk/`,
`execution/`, `ai/`, `telegram/`, or `database/`. Event emission and the
health source are injected, never imported, to keep the dependency arrow
pointing downward.
