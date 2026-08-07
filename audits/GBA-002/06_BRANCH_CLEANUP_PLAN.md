# GBA-002 — Branch Cleanup Plan

Bu hujjat faqat **reja** — Order GBA-002ning konstitutsiyaviy
cheklovi ("Do NOT delete any branch") bo'yicha ushbu auditda hech
qanday branch o'chirilmagan. Har bir tavsiya Director tasdig'idan
keyin bajarilishi kerak.

## O'chirish uchun nomzodlar (Director tasdig'idan keyin)

| Branch | Sabab | Xavf |
|---|---|---|
| `origin/claude/code-analysis-optimization-pwfo3q` | `git merge-base --is-ancestor` -> YES, `goldbot-v1`ga 100% singib ketgan (0 ahead) | Yo'q — hech qanday commit yo'qolmaydi |
| `origin/claude/collaboration` | `git merge-base --is-ancestor` -> YES, `goldbot-v1`ga 100% singib ketgan (0 ahead) | Yo'q |
| `origin/claude/goldbot-data-layer-architecture-f8dx8j` | `git merge-base --is-ancestor` -> YES, `goldbot-v1`ga 100% singib ketgan (0 ahead) | Yo'q |
| Local `claude/code-analysis-optimization-pwfo3q`, `claude/collaboration`, `claude/goldbot-data-layer-architecture-f8dx8j` | Local nusxalar origin bilan bir xil commit'ga ishora qiladi, xuddi shu sabab | Yo'q |

Ushbu 3 (+ 3 local nusxa) branch — **texnik jihatdan xavfsiz o'chirish
nomzodi**, chunki ularning har bir commiti allaqachon `goldbot-v1`
tarixida mavjud (fast-forward ekvivalenti holatda). O'chirish hech
qanday ishni yo'qotmaydi.

## Arxiv branch'lari — hozircha saqlanadi

`origin/Arxiv/main`, `origin/Arxiv/claude/*` (3 ta) — bular allaqachon
"arxiv" deb nomlangan va tarixiy referens vazifasini bajaradi. Ushbu
audit ularni o'chirishni **tavsiya qilmaydi** — ular allaqachon aktiv
ish oqimidan ajratilgan (nom prefiksi orqali) va saqlanishi zarari
yo'q, faqat foydasi bor (tarixiy audit/rollback uchun referens).

## O'chirilmasligi kerak bo'lganlar

- `origin/main` — production reference sifatida hujjatlashtirilgan
  (`production_deploy.yml`), Director qarori (Variant A/B/C, quyida
  `09_DIRECTOR_RECOMMENDATION.md`da) qabul qilinmaguncha, o'chirilmaydi.
- `origin/goldbot-v1` — joriy faol development branch.

## Bosqichma-bosqich Cleanup tartibi (Director tasdig'idan keyin bajariladigan)

1. Director TASK-02 va Director Recommendation (`09_...md`)ni ko'rib
   chiqib, Variant A/B/C'dan birini tanlaydi.
2. Tanlangan Variant amalga oshirilgandan keyin (masalan Variant A:
   `goldbot-v1 -> main` promote qilingandan keyin), 3 ta `claude/*`
   ish branch'i (va ularning local nusxalari) `git branch -d` /
   `git push origin --delete` bilan o'chiriladi — **faqat** Director
   aniq tasdig'idan so'ng, bu audit doirasida emas.
3. Arxiv branch'lari o'z holicha qoldiriladi, alohida arxivlash
   siyosati talab etilmasa.

## Ushbu Cleanup Plan'ning o'zi ushbu auditda bajarilmadi

Order GBA-002'ning "No merge, no delete, no force-push" cheklovi
bo'yicha yuqoridagi barcha amallar **faqat reja** sifatida qoldi —
hech biri bajarilmadi. Bajarish alohida, Director tasdiqlangan keyingi
bosqich hisoblanadi.
