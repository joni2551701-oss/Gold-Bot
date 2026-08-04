# WORK_LOG.md -- core_layer/features

Append-only. Earlier entries are never deleted or rewritten -- only new
entries are appended below.

---

Issue ID: N/A
Date: 2026-08-03
Severity: N/A
Problem: N/A
Cause: N/A
Decision: N/A
Implementation: Module created. Migration completed. Engineering Standard
  initialized (Director Order No. 012/013).
Validation: N/A
Lessons Learned: N/A

---

Issue ID: GFL-001-FLOW-007
Date: 2026-08-04
Severity: N/A
Problem: FLOW-007 (Indicator Engine) audit bo'yicha aniqlandiki, real
  indicator hisoblash hech qayerda mavjud emas edi. `indicator_layer/`
  (blueprint tarkibida ko'rsatilgan Consumer) va `chart_layer/indicators/`
  Foundation Freeze v1.0/MIR-001 skeleton bo'lib, GFL-001 doirasidan
  tashqarida -- ularga yangi business logic yozish taqiqlanadi.
  `core_layer/features/feature_engine.py` va `feature_model.py` esa
  Phase A10'dan beri `atr=None`ni aniq "future phase" hook sifatida
  hujjatlashtirgan edi, lekin `feature_model.py`ning o'z docstringi
  bu hookni "separately-approved phase" deb belgilagan edi. Owner/
  Director'dan aniq tasdiq so'raldi (AskUserQuestion); Director Decision:
  Approve -- GFL Flow-by-Flow metodologiyasi eski "separately-approved
  phase" cheklovini almashtiradi, FLOW-007 tarkibida qo'shimcha ruxsat
  talab qilinmaydi.
Cause: `feature_engine.py`da haqiqiy ATR hisoblash yo'q edi -- faqat
  hujjatlashtirilgan hook.
Decision: Yangi modul yaratish o'rniga (Module Reuse Principle),
  mavjud `core_layer/features/` paketi ichida yangi `atr/` sub-modul
  qo'shildi (GEL-001 Strict konvensiyasi bo'yicha). `feature_engine.py`
  va `feature_model.py`ning mavjud `atr` maydoni/hook'i to'ldirildi --
  boshqa hech qanday API o'zgarmadi.
Implementation: `core_layer/features/atr/atr.py` (`compute_atr()`,
  Wilder's smoothing) + `__init__.py`. `feature_engine.py`da
  `atr=None` -> `atr=compute_atr(context.candles)`. `feature_model.py`
  atr maydoni docstringi yangilandi. `tests/features/test_atr.py`
  (yangi) + `tests/features/test_feature_engine.py`ga real hisoblash
  testi qo'shildi.
Validation: pyflakes/compileall/pytest/main.py -- barchasi PASS.
Lessons Learned: Bir necha bosqich (Phase A10, keyin GFL-001) davomida
  qoldirilgan "future phase" hook'lar ba'zan o'zlarining docstringida
  qo'shimcha tasdiq talabini ham hujjatlashtirishi mumkin -- bunday
  holatda Worker avtomatik davom etmasdan, aniq Owner/Director
  tasdig'ini so'rashi kerak, hatto GFL-004 Lightweight Loop intermediate
  Director Review'ni bekor qilgan bo'lsa ham.

---
