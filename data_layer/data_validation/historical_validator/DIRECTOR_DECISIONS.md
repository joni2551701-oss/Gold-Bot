# DIRECTOR_DECISIONS.md -- data_layer/data_validation/historical_validator

Append-only. Only Director-approved decisions are recorded here. The Worker
does not edit this file independently.

Decision ID: GEL-001
Date: 2026-08-03
Module: data_layer/data_validation/historical_validator
Issue: Flat canonical module file (one module must be one package).
Director Decision: Every canonical module MUST be a Python package
  (GoldBot Engineering Law GEL-001).
Reason: Code + docs + tests + history co-located as one Module Unit; code
  and documentation never separate; extensible without architecture change.
Status: Applied.
Applied Commit: (this Development v1 GEL-001 commit)
Worker: Development v1 autonomous execution.
Result: Module converted to package; public import path preserved; tests green.
