# GBA-002 — TASK-02: Git Divergence Report (GBA-001 raqamlarini qayta tekshirish)

## GBA-001'ning original da'vosi

`16_DIRECTOR_RECOMMENDATIONS.md` va `18_VPS_READINESS_VERDICT.md`:

```
$ git diff origin/main..origin/goldbot-v1 --stat
5768 files changed, 186912 insertions(+), 43351 deletions(-)
```

## GBA-002'ning mustaqil qayta o'lchovi (2026-08-07, `git fetch origin` dan keyin)

```
$ git diff origin/main..origin/goldbot-v1 --shortstat
5786 files changed, 188132 insertions(+), 43351 deletions(-)
```

```
$ git diff origin/main..origin/goldbot-v1 --name-only | wc -l
5786
```

### Solishtirish

| Metrika | GBA-001 (eski) | GBA-002 (yangi, 2026-08-07) | Farq |
|---|---|---|---|
| O'zgargan fayllar | 5768 | 5786 | +18 |
| Qo'shilgan qatorlar | 186912 | 188132 | +1220 |
| O'chirilgan qatorlar | 43351 | 43351 | 0 (o'zgarmagan) |

**Xulosa: GBA-001'ning raqamlari asosan to'g'ri edi (bir xil tartibda,
~5.7-5.8 ming fayl, ~187-188 ming qo'shilgan qator), farq faqat vaqt
o'tishi bilan `goldbot-v1`ga 2026-08-01 (GBA-001 sanasi) dan
2026-08-07 (GBA-002 sanasi)gacha qo'shilgan yangi commit'lar
hisobiga.** Bu — audit natijasining eskirishi emas, balki ikkala
audit orasidagi haqiqiy vaqt farqi (`origin/goldbot-v1`ning oxirgi
commiti — 2026-08-07 20:25:45 — GBA-001dan keyingi).

## Commit-darajasidagi divergence (GBA-001'da o'lchanmagan, GBA-002'da yangi)

```
$ git log origin/main..origin/goldbot-v1 --oneline | wc -l
396   # goldbot-v1'da bor, main'da yo'q

$ git log origin/goldbot-v1..origin/main --oneline | wc -l
144   # main'da bor, goldbot-v1'da yo'q

$ git merge-base origin/main origin/goldbot-v1
ed6a5e995d3d07febf8e6fd4a130fcd3750649fc
```

Bu — GBA-001 hujjatlashtirmagan **yangi topilma**: `main`ning ham
o'ziga xos, `goldbot-v1`da yo'q 144 ta commiti bor. Ya'ni munosabat
oddiy "goldbot-v1 = main + qo'shimcha ish" emas, balki **haqiqiy
ikki tomonlama divergence** (ikkala tomon ham umumiy ajdoddan keyin
mustaqil rivojlangan).

### `main`ning noyob 144 commitining tarkibi

```
$ git log origin/goldbot-v1..origin/main --name-only --format='' | grep '\.py$' | wc -l
0
```

**Muhim dalil: `main`ning 144 ta noyob commitining birortasi ham bitta
`.py` faylga tegmagan.** Ularning barchasi hujjat fayllari
(`README.md` — 44 marta, `SequenceDiagram.md` — 24, `Contracts.md` —
24, `ModuleMap.md` — 23, va boshqa `New_Map/`-uslubidagi fayllar).
Barcha 144 commit bitta muallif — **"Gold Bot"** — tomonidan qilingan
(`git log origin/goldbot-v1..origin/main --format='%an' | sort |
uniq -c` -> `144 Gold Bot`), commit mesajlari uslubi ("Create X.md",
"Delete Y directory", "Rename Z") GitHub veb-muharriridagi qo'lda
fayl operatsiyalariga xos ko'rinishga ega.

**Xulosa:** `main`ning kod (`.py`) tarkibi `goldbot-v1`ga nisbatan
**faqat orqada qolgan**, hech qanday yangi/muqobil kod o'zgarishi
yo'q — GBA-001'ning asosiy xulosasini ("main eski pre-refactor
strukturani saqlaydi") to'liq tasdiqlaydi va aniqlashtiradi: orqada
qolish sof ravishda kod darajasida (`.py`), main'ning o'ziga xos
144 commiti esa faqat hujjat-qatlamli, ular bilan `goldbot-v1`
o'rtasida haqiqiy "raqib" kod o'zgarishi yo'q.

## Fast-forward tekshiruvi (qayta tasdiqlangan)

```
$ git merge-base --is-ancestor origin/main origin/goldbot-v1 ; echo $?
1   # NO — main goldbot-v1'ning ajdodi emas

$ git merge-base --is-ancestor origin/goldbot-v1 origin/main ; echo $?
1   # NO — goldbot-v1 main'ning ajdodi emas
```

Ikkala yo'nalishda ham fast-forward **mumkin emas** — bu GBA-001'da
tekshirilmagan qo'shimcha dalil, endi rasmiy tasdiqlangan.

## Yakuniy tasdiqlash

GBA-001'ning fayl/qator raqamlari **to'g'ri edi va tasdiqlanadi**
(kichik farq — faqat vaqt o'tishi natijasi, xato emas). GBA-002
qo'shimcha ravishda commit-darajasidagi tahlilni qo'shdi: divergence
bir tomonlama emas (main ham 144 ta noyob commitga ega), lekin bu 144
commit sof hujjat-darajasida bo'lgani uchun, **kod jihatidan
`goldbot-v1` `main`dan hech narsani yo'qotmaydi** — faqat oldinga
ketgan.
