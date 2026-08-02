# EventLifecycle Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat EventLifecycle modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
EventPublisher
↓
EventBus
↓
EventDispatcher
↓
EventSubscriber
↓
EventLifecycle
```
---
# Module Architecture
```text
EventLifecycle
        │
        ├── Lifecycle Manager
        ├── State Manager
        ├── Timeout Manager
        ├── Retry Manager
        ├── Completion Manager
        ├── Cleanup Manager
        ├── Metadata Manager
        └── Event Reporter
```
---
# Internal Components
## Lifecycle Manager
Lifecycle boshqaradi.
---
## State Manager
Event holatini boshqaradi.
---
## Timeout Manager
Timeout nazorat qiladi.
---
## Retry Manager
Retry jarayonini boshqaradi.
---
## Completion Manager
Completed Event'larni boshqaradi.
---
## Cleanup Manager
Lifecycle tugagandan keyin resurslarni tozalaydi.
---
## Metadata Manager
Lifecycle Metadata boshqaradi.
---
## Event Reporter
Lifecycle Event'larini yaratadi.
---
# Dependency Map
```text
EventPublisher
↓
EventBus
↓
EventDispatcher
↓
EventSubscriber
↓
EventLifecycle
```
---
# Allowed Dependencies
✓ EventPublisher
✓ EventBus
✓ EventDispatcher
✓ EventSubscriber
✓ Configuration Layer
---
# Forbidden Dependencies
✗ Context Layer
✗ Strategy Layer
✗ Decision Layer
✗ Risk Layer
✗ AI Layer
✗ Platform Layer
✗ Business Layer
---
# Ownership
EventLifecycle egalik qiladi.
✓ Lifecycle State
✓ Retry State
✓ Timeout State
✓ Completion State
✓ Lifecycle Metadata
---
# Module Rules
1. EventLifecycle yagona Canonical Lifecycle Manager.
2. Event State qat'iy kuzatiladi.
3. Retry boshqariladi.
4. Timeout boshqariladi.
5. Circular Dependency taqiqlanadi.
---
# Summary
EventLifecycle GoldBot Event System ichidagi barcha Event'larning Runtime Lifecycle boshqaruvini amalga oshiruvchi yagona Canonical modul hisoblanadi.
