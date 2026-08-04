# GFL-001 — Flow Progress

## Maqsad

Ushbu hujjat GoldBot Data Flow rivojlanishining rasmiy holatini yuritadi.

Har bir Flow quyidagi statuslardan biriga ega bo'ladi va Development davomida muntazam yangilanadi.

**V3 qayta ko'rib chiqish (GFL-002, Director Order):** Flow ID'lar V3
Architecture asosida qayta tashkil qilindi. Hech bir bajarilgan ish
yo'qolmadi -- faqat mapping yangilandi (eski FLOW-001 "Current Price"
endi FLOW-002, statusi va 100% progress'i saqlanib qoldi). Old -> New
mapping jadvali shu buyruqqa javoban yozilgan Director Review chat
xabarida keltirilgan.

---

# Status

🟦 Blueprint

Flow hali boshlanmagan.

---

🟨 In Progress

Flow ustida Development davom etmoqda.

---

🟪 Review

Flow yakunlandi va Director Review kutilmoqda.

---

🟩 Completed

Flow to'liq yakunlandi.

Barcha testlar muvaffaqiyatli o'tgan.

Documentation yangilangan.

WORK_LOG yozilgan.

---

🟥 Blocked

Flow davom eta olmaydi.

Director Review talab qilinadi.

---

# Flow Progress

| Flow | Nomi | Layer / Subsystem | Status | Progress | Owner | Izoh |
|------|------|--------------------|--------|----------|-------|------|
| FLOW-001 | System Bootstrap / Configuration | Foundation Layer | 🟦 | 0% | Worker | Yangi (V3 refactor, GFL-002) -- avval alohida Flow sifatida mavjud emas edi |
| FLOW-002 | Current Price | Data Layer | 🟩 | 100% | Worker | Eski FLOW-001. Yakunlandi -- 2026-08-04. Audit shuni ko'rsatdi: barcha modullar allaqachon mavjud edi, faqat ulanmagan (Price Stream `tick()`ni hech kim chaqirmasdi, `CurrentPriceProvider` default holatda har safar yangi/alohida instance qurar edi). Tuzatildi: shared singleton + default StreamValidator + default MarketMemoryRegistry + polling.py'da tick driver. 5411 test PASS, E2E test qo'shildi. |
| FLOW-003 | Market Memory | Data Layer | 🟦 | 0% | Worker | Eski FLOW-002. GFL-003 (Sequential Flow Rule) bo'yicha navbatdagi Flow -- eng kichik raqamli bajarilmagan Flow ID. |
| FLOW-004 | Market Engine | GoldBot > GoldBot Core | 🟦 | 0% | Worker | Eski FLOW-003. Kutmoqda. |
| FLOW-005 | Context Engine | GoldBot > GoldBot Core | 🟦 | 0% | Worker | Eski FLOW-004. Kutmoqda. |
| FLOW-006 | Analysis Engine | GoldBot > GoldBot Core | 🟦 | 0% | Worker | Eski FLOW-005. Kutmoqda. |
| FLOW-007 | Indicator Engine | GoldBot > GoldBot Core | 🟦 | 0% | Worker | Eski FLOW-006. Kutmoqda. |
| FLOW-008 | Strategy Engine | GoldBot > GoldBot Core | 🟦 | 0% | Worker | Eski FLOW-007. Kutmoqda. |
| FLOW-009 | Confluence Engine | GoldBot > GoldBot Core | 🟦 | 0% | Worker | Eski FLOW-008. Kutmoqda. |
| FLOW-010 | Decision Engine | GoldBot > GoldBot Core | 🟦 | 0% | Worker | Eski FLOW-009. Kutmoqda. |
| FLOW-011 | Risk Engine | GoldBot > GoldBot Core | 🟦 | 0% | Worker | Eski FLOW-010. Kutmoqda. |
| FLOW-012 | Signal Engine | GoldBot > GoldBot Core | 🟦 | 0% | Worker | Eski FLOW-011. Kutmoqda. |
| FLOW-013 | Execution Engine | GoldBot > GoldBot Core | 🟦 | 0% | Worker | Eski FLOW-012. Kutmoqda. |
| FLOW-014 | Trade Monitoring | GoldBot > GoldBot Core | 🟦 | 0% | Worker | Eski FLOW-013. Kutmoqda. |
| FLOW-015 | GoldBot Core API | GoldBot > GoldBot Core | 🟦 | 0% | Worker | Eski FLOW-014. Kutmoqda. |
| FLOW-016 | Chart Service | GoldBot > Chart Service | 🟦 | 0% | Worker | Yangi (V3 refactor, GFL-002) -- `chart_layer/` mavjud, lekin GFL Flow sifatida hali audit qilinmagan. Sub-Status: Blueprint (Design boshlanmagan). |
| FLOW-017 | Personal AI Core | GoldBot > Personal AI Core | 🟦 | 0% | Worker | Yangi (V3 refactor, GFL-002) -- `ai_layer/` mavjud, lekin GFL Flow sifatida hali audit qilinmagan. Sub-Status: Blueprint (Design boshlanmagan). |
| FLOW-018 | Backtesting Engine | GoldBot > Backtesting Engine | 🟦 | 0% | Worker | Yangi (V3 refactor, GFL-002) -- `backtesting_layer/` mavjud, lekin GFL Flow sifatida hali audit qilinmagan. Sub-Status: Blueprint (Design boshlanmagan). |
| FLOW-019 | Application Services | Application Services | 🟦 | 0% | Worker | Eski FLOW-015. Kutmoqda. |
| FLOW-020 | Telegram | Platform Layer | 🟦 | 0% | Worker | Eski FLOW-016. Kutmoqda. |
| FLOW-021 | Mini App | Platform Layer | 🟦 | 0% | Worker | Eski FLOW-017. Kutmoqda. |
| FLOW-022 | Android | Platform Layer | 🟦 | 0% | Worker | Eski FLOW-018. Kutmoqda. |
| FLOW-023 | iOS | Platform Layer | 🟦 | 0% | Worker | Eski FLOW-019. Kutmoqda. |
| FLOW-024 | Desktop | Platform Layer | 🟦 | 0% | Worker | Eski FLOW-020. Kutmoqda. |
| FLOW-025 | Web | Platform Layer | 🟦 | 0% | Worker | Eski FLOW-021. Kutmoqda. |

---

# Development Rules

Worker faqat bitta Flow ustida ishlaydi.

**GFL-003 -- Sequential Flow Rule (Director qarori):** navbatdagi
ishlanadigan Flow -- ushbu jadvalda yuqoridan pastga qarab birinchi
🟩 Completed bo'lmagan Flow (eng kichik raqamli bajarilmagan Flow ID).
Har bir Flow faqat o'zidan oldingi Flow Approved + Completed + CI
Passed bo'lgandan keyingina boshlanadi. Tartibdan tashqariga chiqib
(masalan FLOW-010'dan FLOW-005'ga) qaytish taqiqlanadi. To'liq ta'rif:
`GFL-001_FLOW_FIRST_STANDARD.md`.

Flow statusi ushbu hujjatda darhol yangilanadi.

---

# Status Lifecycle

Blueprint

↓

In Progress

↓

Review

↓

Completed

yoki

Blocked

↓

Director Review

↓

In Progress

↓

Completed

---

# Progress Rules

Progress faqat:

- Audit
- Development
- Testing
- Validation
- Documentation
- WORK_LOG

yakunlangandan keyin o'zgartiriladi.

---

# Blocked Rules

Agar Flow:

- Input ololmasa
- Output ishlamasa
- End-to-End test o'tmasa
- Director Review talab qilsa

Status:

🟥 Blocked

bo'ladi.

---

# Completion Rules

Flow Completed bo'lishi uchun:

✓ Audit yakunlangan

✓ Kod ishlaydi

✓ Input ishlaydi

✓ Output ishlaydi

✓ Consumer ishlaydi

✓ Barcha Consumer'lar PASS (Fan-Out Rule)

✓ End-to-End Test PASS

✓ Producer→Consumer latency o'lchangan va yozilgan (Latency Rule)

✓ Documentation yangilangan

✓ WORK_LOG yozilgan

✓ Director Review yopilgan (agar talab qilingan bo'lsa)

---

# Final Principle

Flow Progress — GoldBot Development holatini aks ettiruvchi yagona rasmiy hujjat hisoblanadi.

Worker har bir Flow holatini ushbu hujjatda doimiy ravishda yangilab borishi shart.
