# Features Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Features ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
Features
├── FeatureEngine
├── FeatureModel
└── FeatureNormalizer
```
---
# Module Position
```text
Analysis Results (Context, Signal Quality, Explainability)
↓
Features
↓
AI Layer / Backtesting Layer / ML Export
```
---
# Processing Pipeline (Planned)
```text
FeatureEngine → FeatureModel → FeatureNormalizer
```
---
# Dependency Map
```text
Analysis Results (Context, Signal Quality, Explainability)
↓
Features
↓
AI Layer / Backtesting Layer / ML Export
```
---
# Allowed Dependencies
✓ CoreEngine
✓ Configuration
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer (to'g'ridan-to'g'ri)
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Flow
```text
Receive Input
↓
Process (Features)
↓
Emit Output
↓
AI Layer / Backtesting Layer / ML Export
```
---
# Summary
Features Features GoldBot Core Layer ichidagi Canonical Feature Standardization moduli hisoblanadi. U AI, Strategy, Backtesting va ML Export uchun umumiy Feature obyektlarini tayyorlaydi — hech qachon yangi tahlil bajarmaydi.
