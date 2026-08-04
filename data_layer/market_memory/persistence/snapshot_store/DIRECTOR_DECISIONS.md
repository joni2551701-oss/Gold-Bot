# DIRECTOR_DECISIONS.md — data_layer/market_memory/persistence/snapshot_store

Append-only. Only Director-approved decisions.

Decision ID: GEL-001-STRICT
Date: 2026-08-04
Module: data_layer/market_memory/persistence/snapshot_store
Director Decision: Strict interpretation — every canonical module MUST be a package; flat modules forbidden.
Reason: One Module = One Package = One Responsibility.
Status: Applied.
Result: Package form; import path preserved; tests green.
