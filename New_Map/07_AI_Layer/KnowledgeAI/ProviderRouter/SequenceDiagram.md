# Provider Router Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ProviderRouter Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
KnowledgeAI
↓
ProviderRouter
↓
Select Provider
↓
External AI
↓
Receive Response
↓
Normalize Response
↓
ValidationEngine
```
---
# Runtime Rules
1. Internal Knowledge avval tekshiriladi.
2. Provider faqat zarurat bo'lsa chaqiriladi.
3. Timeout nazorat qilinadi.
4. Response Normalize qilinadi.
5. ValidationEngine'ga uzatiladi.
---
# State Flow
```text
Idle
↓
Routing
↓
Waiting Response
↓
Normalizing
↓
Completed
or
Provider Failed
↓
Retry / Failover
```
---
# Summary
KnowledgeAI
↓
ProviderRouter
↓
External AI
↓
ValidationEngine
