# OrderBlock Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat OrderBlock modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu OrderBlock modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Data
↓
Read Market Structure
↓
Read Liquidity
↓
Detect Bullish Order Block
↓
Detect Bearish Order Block
↓
Validate Blocks
↓
Detect Mitigation
↓
Detect Invalidation
↓
Generate Order Block State
↓
ContextService
```
---
# Update Sequence
```text
New Candle
↓
Update Order Blocks
↓
Update Mitigation
↓
Update Invalidation
↓
Publish Order Block State
```
---
# Runtime Rules
1. Market Structure avval tayyor bo'lishi kerak.
2. Liquidity Context hisobga olinadi.
3. Validation majburiy.
4. Mitigation va Invalidation uzluksiz kuzatiladi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Collecting
↓
Detecting
↓
Validating
↓
Monitoring
↓
Ready
↓
Completed
or
Failed
```
---
# Summary
Canonical Runtime Sequence
Market Data
↓
OrderBlock
↓
Order Block State
↓
ContextService
