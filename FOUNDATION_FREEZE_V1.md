# Foundation Freeze v1.0
Status: APPROVED — CANONICAL ARCHITECTURE
Sana: 2026-08-03
Qaror: Director Declaration — Foundation Freeze v1.0

> **Nom o'zgarishi (Phase A.5).** Ushbu hujjatda uchraydigan `New_Map/` havolalari tarixiy yozuv hisoblanadi. Foundation Freeze v1.0'dan keyin 17 ta Layer repository root'ga chiqarildi va `New_Map/` nomi bekor qilindi — batafsil `ARCHITECTURE.md`ga qarang.
---
# Maqsad
Ushbu hujjat GoldBot loyihasining arxitektura bosqichi rasman yakunlanganini va 17 ta Layer repository root'ida GoldBot'ning yagona Canonical Architecture'i sifatida qabul qilinganini qayd etadi.
---
# Yakuniy Arxitektura Holati
```text
Layers ....................... 17
Modules ...................... 210
Missing Documents ............ 0
Dependency Conflicts ......... 0
Allowed/Forbidden Conflict ... 0
Broken Runtime Rules ......... 0
Broken Ownership ............. 0
Broken Gateway ............... 0
Critical Findings ............ 0
```
---
# Layer Ro'yxati
```text
01_Data_Layer               09_Risk_Layer
02_Core_Layer               10_Execution_Layer
03_Context_Layer            11_Trade_Monitoring_Layer
04_Indicator_Layer          12_Database_Layer
05_Strategy_Layer           13_Platform_Layer
06_Signal_Layer             14_Media_Layer
07_AI_Layer                 15_Future_Expansion
08_Decision_Layer           16_Chart_Layer
                            17_Backtesting_Layer
```
---
# Freeze Qoidalari
Foundation Freeze v1.0 kuchga kirgan vaqtdan boshlab quyidagilar **taqiqlanadi**:
✗ Yangi Layer qo'shish
✗ Yangi modul qo'shish
✗ Runtime Pipeline'ni o'zgartirish
✗ Ownership'ni o'zgartirish
✗ Public API'ni o'zgartirish
✗ Canonical Contracts'ni o'zgartirish

Quyidagilar **ruxsat etiladi**:
✓ Bug fix
✓ Typo tuzatish
✓ Documentation correction
✓ Implementatsiya

Freeze'ni buzadigan har qanday o'zgarish uchun alohida Director Approval va yangi Version Freeze talab qilinadi.
---
# Canonical Status
Repository root'idagi 17 ta Layer endi GoldBot loyihasining **yagona rasmiy arxitekturasi** hisoblanadi.
`main` va `claude/collaboration` branchlaridagi eski arxitektura hujjatlari faqat tarixiy ma'lumot va referens sifatida saqlanadi.
---
# Arxitektura Qoidalari (ACR)
Barcha Canonical Rule va ACR'lar `Architecture_Audit_Plan.md`'ning §9b bo'limida saqlanadi. Foundation Freeze paytida amal qilayotgan asosiy qoidalar:

| Rule | Qamrov |
|---|---|
| Dependency Source of Truth Rule | Contracts.md ↔ ModuleMap.md mosligi |
| Module Runtime Boundary Rule | Modul o'z chegarasidan tashqariga chiqmaydi |
| Group README Rule | Guruh hujjatlari modul ro'yxati bilan mos |
| Canonical Naming Rule | Yagona nomlash |
| Layer Naming Rule | Layer nomlari izchil |
| Runtime Pipeline Rule | Guruh darajasidagi pipeline ustuvor |
| Parallel Execution Rule | Parallel modullar ketma-ket ko'rsatilmaydi |
| Context Analysis Order Rule | Context tahlil tartibi |
| Context Ownership Rule | Context egaligi |
| Strategy Execution Rule | Strategy bajarilishi |
| Algorithm vs Runtime Rule | Algoritm va Runtime ajratilishi |
| AI Sequential Processing Rule | AI ketma-ketligi |
| Layer Direction Rule | Layer yo'nalishi |
| Knowledge Lifecycle Rule | Knowledge hayot aylanishi |
| Command Interpretation Rule | Buyruq talqini |
| Execution Ownership Rule | Execution Result egaligi |
| Risk Policy Rule | Risk Policy chegaralari |
| Platform Gateway Rule | PlatformService qamrovi |
| Chart Shared State Rule | Chart modullari Shared State orqali ishlaydi |
| Render Loop Rule | Renderer har frame Render State'ni o'qiydi |
| Chart Runtime Rule | Layer_DataFlow execution order, ownership zanjiri emas |
| Canonical Event Bus Rule | Event_System yagona Event Bus |
| Backtesting Isolation Rule | Backtesting real trading'dan ajratilgan |
| Module Reuse Rule | Duplicate modul taqiqlanadi |
| Worker Decision Rule (WDR-001) | Worker mustaqil qaror doirasi |
| Repository Aggregation Rule (RAR-001) | Repository domen bo'yicha guruhlanadi |
---
# Ochiq Known Gaps (Freeze'ni bloklamaydi)
| # | Tavsif | Toifa | Yechim |
|---|---|---|---|
| KG-001 | Maxfiy qiymatlar ikki yo'ldan o'qiladi (`core/secrets.py` va `config.py`) | Minor | RT-001 (implementatsiya bosqichi) |
| KG-003 | `AuditLogRepository.log_action()` hali chaqirilmaydi | Minor | RT-003 (implementatsiya bosqichi) |

KG-002 (Database repository soni) Foundation Freeze'dan oldin **RAR-001** bilan yopilgan.
---
# Keyingi Bosqich — Director Order No. 001
`goldbot-v1` branchi yaratilgandan so'ng implementatsiya quyidagi tartibda bajariladi:
```text
1. New_Map asosida papka strukturasini yaratish
        ↓
2. Eski kodni modulma-modul yangi arxitekturaga migratsiya qilish
        ↓
3. Migratsiya qilingan kodni refaktor qilish
        ↓
4. Yetishmayotgan modullarni implementatsiya qilish
        ↓
5. Testlar va integratsiyani bosqichma-bosqich tiklash
```
---
# Roadmap Holati
```text
15 Layers                    ✅
16_Chart_Layer               ✅
Architecture Gap Review v1.0 ✅
Legacy Packages Review       ✅
17_Backtesting_Layer         ✅
Secrets                      ✅
AuditLog                     ✅
Performance                  ✅
Final Consistency Pass       ✅
Foundation Freeze v1.0       ✅
goldbot-v1                   ▶ keyingi qadam
Implementation               ⏳
```
---
# Summary
GoldBot arxitektura bosqichi yakunlandi. 17 Layer va 210 modul to'liq hujjatlashtirildi, barcha Canonical Rule va ACR'lar belgilandi, yakuniy izchillik tekshiruvi nol kamchilik bilan o'tdi. Canonical Architecture GoldBot'ning yagona rasmiy arxitekturasi sifatida muzlatildi. Loyihaning asosiy e'tibori endi ushbu kanonik arxitektura asosida sifatli implementatsiyaga qaratiladi.
