# Translation Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat Translation ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).

---

# Internal Architecture (Planned)

Translation

├── TranslationManager

├── LanguageRegistry

└── UICatalog

---

# Module Position

Content / UI Text

↓

Translation

↓

Platform Layer / Media Layer

---

# Processing Pipeline (Planned)

TranslationManager → LanguageRegistry → UICatalog

---

# Dependency Map

Content / UI Text

↓

Translation

↓

Platform Layer / Media Layer

---

# Allowed Dependencies

✓ AI_Content_Studio

✓ Content_Manager

---

# Forbidden Dependencies

✗ Signal Layer

✗ Decision Layer

✗ Risk Layer

✗ Execution Layer

✗ Database Layer

---

# Runtime Flow

Receive Input

↓

Process (Translation)

↓

Emit Output

↓

Platform Layer / Media Layer

---

# Summary

Translation Translation Media Layer ichidagi Canonical tarjima moduli hisoblanadi. U GoldBot interfeysi va kontentini UZ / RU / EN tillari o'rtasida tarjima qiladi — hech qachon market tahlili yoki savdo qarori bilan shug'ullanmaydi.
