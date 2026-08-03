# OrderBlock Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat OrderBlock modulining rasmiy Architecture Contract hujjati hisoblanadi.
OrderBlock GoldBot Context Layer ichidagi Institutional Order Block'larni aniqlovchi yagona Canonical modul hisoblanadi.
---
# Module Responsibility
OrderBlock quyidagilar uchun javobgar.
✓ Bullish Order Block Detection
✓ Bearish Order Block Detection
✓ Order Block Validation
✓ Mitigation Detection
✓ Invalidation Detection
✓ Order Block State Management
✓ Order Block Event Generation
OrderBlock bajarmaydi.
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
MarketStructure
↓
Liquidity
↓
OrderBlock
↓
ContextService
↓
Boundary End
---
# Input Contract
• OHLC Data
• Candle Stream
• Market Structure
• Liquidity State
---
# Output Contract
• Bullish Order Blocks
• Bearish Order Blocks
• Mitigation Events
• Invalidation Events
• Order Block State
---
# Allowed Dependencies
✓ ContextEngine
✓ MarketStructure
✓ Liquidity
✓ ContextService
✓ Event System
---
# Forbidden Dependencies
✗ Indicator Layer
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# State Contract
• Initializing
• Detecting
• Validating
• Monitoring
• Ready
• Failed
---
# Runtime Contract
1. Order Block faqat tasdiqlangan Market Structure asosida aniqlanadi.
2. Liquidity Context hisobga olinishi shart.
3. Validation majburiy.
4. Mitigation va Invalidation Runtime davomida kuzatiladi.
5. Signal yaratish taqiqlanadi.
6. Indicator hisoblash taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
OrderBlock:
✓ Order Block aniqlaydi.
✓ Validation bajaradi.
✓ Mitigation kuzatadi.
✓ Invalidation kuzatadi.
✓ Order Block State yaratadi.
OrderBlock:
✗ Strategy bajarmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Bullish Order Block aniqlanadi.
✓ Bearish Order Block aniqlanadi.
✓ Validation ishlaydi.
✓ Mitigation Detection ishlaydi.
✓ Invalidation Detection ishlaydi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
OrderBlock Contract GoldBot Context Layer ichidagi Institutional Order Block Analysis modulining rasmiy arxitektura shartnomasi hisoblanadi.
OrderBlock Market Context uchun Institutional Point of Interest (POI) yaratadigan yagona Canonical komponent hisoblanadi.
