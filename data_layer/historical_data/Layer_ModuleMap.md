# Historical Data Layer Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat Historical Data bo'limi tarkibidagi barcha modullar, ularning vazifalari va o'zaro bog'lanishlarini tavsiflaydi.

Bu hujjat Historical Data bo'limining rasmiy modul xaritasi (Module Architecture Blueprint) hisoblanadi.

---

# Historical Data Module Map

```text
                HistoricalDataService
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
      Bootstrap                     Recovery
          │                             │
          └──────────────┬──────────────┘
                          ▼
                 HistoricalProviders
                          │
                          ▼
                 HistoricalDatabase
                          │
                          ▼
                  Data Validation
                          │
                          ▼
                   Market Memory
```

---

# Module Dependencies

## HistoricalDataService

Purpose

Historical Data bo'limining markaziy Orchestrator komponenti.

Dependencies

None (Configuration'dan tashqari)

Outputs

• Bootstrap
• Recovery

---

## Bootstrap

Purpose

Tizim birinchi ishga tushganda tarixiy ma'lumot bilan Market Memory'ni to'ldirish.

Reads

• HistoricalProviders

Writes

• HistoricalDatabase

---

## Recovery

Purpose

Data Gap aniqlanganda yetishmayotgan tarixiy ma'lumotni tiklash.

Reads

• HistoricalProviders

Writes

• HistoricalDatabase

---

## HistoricalProviders

Purpose

Tashqi tarixiy ma'lumot manbalari bilan ishlash.

Reads

• External Provider

Writes

• HistoricalDatabase

---

## HistoricalDatabase

Purpose

Tarixiy market ma'lumotlarini saqlash va o'qish uchun taqdim etish.

Reads

• HistoricalProviders

Writes

• Data Validation

---

## HistoricalDataFlow

Purpose

Historical Data bo'limi ichidagi ma'lumot oqimini hujjatlashtirish (Documentation-only, runtime komponent emas).

---

# Allowed Dependencies

```text
HistoricalDataService
        │
        ▼
Bootstrap / Recovery
        │
        ▼
HistoricalProviders
        │
        ▼
HistoricalDatabase
        │
        ▼
Data Validation
```

---

# Forbidden Dependencies

Historical Data

✗ Context
✗ Strategy
✗ Decision
✗ AI
✗ Live Data (to'g'ridan-to'g'ri)

---

# Module Communication Rules

1. Bootstrap va Recovery bir-birini chaqirmaydi.
2. Barcha ma'lumot HistoricalDatabase orqali o'tadi.
3. Data Validation'dan o'tmagan ma'lumot Market Memory'ga yozilmaydi.
4. HistoricalDataService barcha ichki modullarni muvofiqlashtiradi.
5. Historical Data ichida Circular Dependency taqiqlanadi.

---

# Summary

Historical Data Layer Module Map bo'lim ichidagi barcha modullar va ularning bog'lanishlarini rasmiy ravishda belgilaydi.

Har bir modul faqat o'z vazifasini bajaradi va faqat ruxsat etilgan yo'nalish bo'yicha boshqa modullar bilan ishlaydi.
