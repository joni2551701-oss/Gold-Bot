# decision/

## Purpose
Signal confidence, HTF bias, (inverted) AI risk score va AI
confidence'ni bitta yakuniy trade verdict'ga birlashtiradi: APPROVE,
REJECT yoki NO_TRADE. Phase A3 ("Decision Engine v2") holatiga ko'ra,
bu A3'dan oldingi flat ikki-input average'ni almashtiruvchi weighted
to'rt-input formula hisoblanadi.

## Flow
```
Signal Candidate + AI Analysis + (optional) HTF Bias Result
      |
      v
Decision Engine   -- DecisionInput -> weighted score -> threshold logic
      |
      v
Risk Manager
```

## Decision v2: Input flow

`DecisionEngine.evaluate(signal, ai_analysis, htf_bias=None)`
allaqachon qabul qilgan uch obyektdan `DecisionInput` quradi
(`_build_decision_input()`) — hech qanday yangi fetch, hech qanday
yangi pipeline stage yo'q:

| `DecisionInput` maydoni | Manba | Eslatmalar |
|---|---|---|
| `signal_confidence` | `SignalCandidate.confidence` | A3'dan oldingi holatdan o'zgarmagan. |
| `htf_bias` | `HTFBiasResult.bias` (yoki `htf_bias=None` bo'lsa `HTFBias.UNKNOWN`) | `context_layer/trend/htf_bias.py`, Phase A2. |
| `htf_quality_score` | `HTFBiasResult.quality_score` (yoki `htf_bias=None` bo'lsa `0.0`) | Step-5 quality dampening'ni boshqaradi — quyida qarang. |
| `risk_score` | `1.0 - AIAnalysisResult.risk_score` | **Inverted** — `AIAnalysisResult.risk_score` `0.0`=risk yo'q .. `1.0`=maksimal risk (`ai_layer/ai_engine/ai_analyzer.py`); `DecisionInput.risk_score` teskari qilingan, shunda "yuqoriroq doim yaxshiroq" bo'ladi, boshqa uch input bilan mos. E'tibor bering, bu `risk_layer.risk_engine.risk_manager.RiskResult` *emas* — bu obyekt Decision Engine vaqtida hali mavjud emas (Risk pipeline'da Decision'dan *keyin* ishlaydi). |
| `ai_score` | `AIAnalysisResult.confidence` | A3'dan oldingi holatdan o'zgarmagan. |

`htf_bias`ni o'tkazib yuboradigan chaqiruvchi (har qanday
pre-Phase-A2/A3 call site) o'zgarmagan holda ishlashda davom etadi —
quyidagi "Backward compatibility"ga qarang.

## Weight system

`DecisionWeights` (frozen dataclass, `DecisionConfig` xuddi avvalgidek
`DecisionEngine.__init__`ga inject qilinadigan) to'rt weight'ni nomli
konstantalar sifatida saqlaydi — `evaluate()` ichida hech qachon
hardcoded emas:

| Komponent | Weight |
|---|---|
| Signal Confidence | 40% |
| HTF Bias | 25% |
| Risk (inverted AI risk score) | 20% |
| AI Confidence | 15% |

```
final_confidence = 0.40*signal_score + 0.25*htf_score
                  + 0.20*risk_score  + 0.15*ai_score
```

To'rt komponent score va `final_confidence` mavjud 0.0–1.0 shkalasida
qoladi — bu `DecisionConfig.min_confidence`/`approve_confidence`,
`SignalCandidate.confidence`, va `AIAnalysisResult.confidence` Phase
A3'dan oldin ham ishlatgan bir xil shkala, shuning uchun hech qanday
mavjud threshold yoki downstream consumer shkalani o'zgartirishga
muhtoj emas.

## HTF integration

`HTF_BIAS_SCORE_MAP` (`decision_engine.py`da module-level konstanta)
`HTFBias`ni base score'ga moslaydi, Phase A3 brief'ining 0–100
misolidan GoldBot'ning mavjud 0.0–1.0 confidence shkalasiga
moslashtirilgan:

| `HTFBias` | Base score |
|---|---|
| `BULLISH` | `1.0` |
| `NEUTRAL` | `0.5` |
| `BEARISH` | `0.0` |
| `UNKNOWN` | `0.5` (`NEUTRAL` bilan bir xil — hal qilinmagan HTF o'qish natijani hech qaysi tomonga itarmasligi kerak) |

**Quality handling** (past HTF ma'lumot sifati contribution'ni neytral
tomon susaytiradi — u hech qachon avtomatik rejection'ga sabab
bo'lmaydi):

```
htf_score = base_score * htf_quality_score + 0.5 * (1 - htf_quality_score)
```

`quality_score=1.0` (100%) → to'liq weight (base score o'zgarishsiz
o'tadi). `quality_score=0.0` (0%) → base score to'liq neytral o'rta
nuqta `0.5` bilan almashtiriladi, asosdagi bias qanday bo'lishidan
qat'i nazar. Oradagi har qanday qiymat — chiziqli blend.

## Explainability

`TradeDecision` (Phase A3) formula ishlatgan har bir komponentni,
oldindan mavjud `action`/`confidence`/`reason`/`signal`/`ai_analysis`
maydonlariga qo'shimcha ravishda, ochib beradi:

| Maydon | Ma'nosi |
|---|---|
| `signal_score` | `DecisionInput.signal_confidence`, weight qo'llanmagan. |
| `htf_score` | Quality bilan susaytirilgan HTF hissasi (yuqoriga qarang). |
| `risk_score` | `DecisionInput.risk_score` (inverted AI risk score), weight qo'llanmagan. |
| `ai_score` | `DecisionInput.ai_score`, weight qo'llanmagan. |
| `final_score` | To'liq weighted blend — doim `confidence`ga teng; alohida nomlangan maydon faqat formula'ning besh komponentidan biri bo'lgani uchun, boshqacha ma'lumot olib yurgani uchun emas. |

Bu faqat data exposure — buni ko'rsatish uchun hech qanday UI/Telegram
o'zgarishi qilinmagan (`platform_layer/telegram/signal_formatter.py`ga
tegilmagan).

## Backward compatibility

- `DecisionEngine.evaluate(signal, ai_analysis)` — uchinchi argumentsiz
  — xuddi avvalgidek ishlaydi: `htf_bias` `None`ga default bo'ladi,
  buni `_build_decision_input()` `htf_quality_score=0.0` bilan
  `HTFBias.UNKNOWN` sifatida ko'radi, buni yuqoridagi quality formula
  doim aynan `0.5`ga hal qiladi — aniq `UNKNOWN` natijasi bilan bir xil
  neytral hissa, hech qachon xato emas.
- `DecisionEngine()` — argumentsiz — hali ham ishlaydi: `config` ham,
  yangi `weights` ham o'z standart qiymatlariga default bo'ladi.
- `DecisionConfig.min_confidence`/`approve_confidence`ga qarshi
  uch-tarmoqli APPROVE/REJECT/NO_TRADE threshold logikasi, va
  AI-approval hard gate (`if not ai_analysis.approved: REJECT`, har
  qanday threshold'dan oldin tekshiriladi) — bayt-ba-bayt
  o'zgarmagan — faqat `final_confidence`ga uzatiladigan narsa
  o'zgargan.
- `TradeDecision`'ning besh yangi maydoni hammasi `0.0`ga default
  bo'ladi, shuning uchun uni to'g'ridan-to'g'ri quruvchi har qanday
  gipotetik chaqiruvchi (bu kodbazada bugun bunday hech kim yo'q —
  `DecisionEngine.evaluate()` yagona qurilish nuqtasi) ham buzilmaydi.

**Ataylab o'zgargan narsa**: berilgan `(signal, ai_analysis)` jufti
uchun `confidence`ning aniq raqamli qiymati, chunki formula'ning o'zi
almashtirilgan (Phase A3'ning aniq brief'iga muvofiq) — shu sababli
`tests/unit/test_decision_engine.py`'ning formula'ga bog'liq ikki
assertion'i yangi formula'ning haqiqiy natijasiga yangilangan, har bir
behavioral kafolat esa (AI-reject doim REJECT qiladi, threshold
kesishmalari hali ham to'g'ri action ishlab chiqaradi, `TradeDecision`
hali ham asl signal/AI analysis'ni olib yuradi) shunchaki
faraz qilinmagan, qayta tasdiqlangan.

## Input
`SignalCandidate` (`signals/`dan) + `AIAnalysisResult` (`ai/`dan) +
ixtiyoriy ravishda `HTFBiasResult` (`context/`dan, Phase A2).

## Output
`TradeDecision` (`action`, `confidence`, `reason`, `signal`,
`ai_analysis`, plus yuqoridagi besh explainability maydoni).

## Dependencies
`ai/` (`AIAnalysisResult` uchun) va `signals/` (`SignalCandidate`
uchun) — ikkisi ham hali `TYPE_CHECKING`-only, A3'dan oldingi holatdan
o'zgarmagan. `context/` (`HTFBias` uchun, haqiqiy runtime import — enum
module load vaqtida `HTF_BIAS_SCORE_MAP`ning dict key'lari sifatida
ishlatiladi; `HTFBiasResult`ning o'zi `TYPE_CHECKING`-only qoladi).
Hali ham `database/`, `telegram/` yoki `risk/`ga dependency yo'q.

## Future Expansion
Confidence-threshold qiymatlari (`DecisionConfig`) va weight
qiymatlari (`DecisionWeights`) ikkisi ham `CLAUDE.md`'ning Trading
Safety qoidalarida har qanday keyingi o'zgarishdan oldin tasdiq talab
qilinadigan deb aniq nomlangan — Phase A3'ning o'zi shunday aniq
tasdiqlangan o'zgarish edi. Bir xil weighted-formula shakliga tabiiy
kelajakdagi input'lar (bu fazada implementatsiya qilinmagan): Signal
Quality Score, Market Regime, Session Intelligence — qarang
`docs/v0.3.5_SPECIFICATION.md` va
`docs/FOUNDATION_GAP_ANALYSIS.md`.

---

## STEP-09 business-decision layer (TASK-CORE-009)

Yuqoridagi hammasi **live, FROZEN** yo'lni tasvirlaydi:
`DecisionEngine.evaluate()` → `DecisionAction` (APPROVE / REJECT /
NO_TRADE) bilan `TradeDecision`. Bu yo'l tegilmagan.

STEP-09 **additive, parallel** business-decision layer qo'shadi
(Director qarori: *"Additive parallel + reuse-first"*), bu
`SignalCandidate` + `AIAnalysisResult` o'rniga **canonical signal**ni
(`signal_layer.signal_builder.schema.SignalSchema`) iste'mol qiladi va
roadmap talab qilgan boyroq verdict lug'atini ishlab chiqaradi:
**APPROVE / REJECT / HOLD / EXPIRE**. U frozen engine'ning verdict'ini
**qayta ishlatadi** — confidence blend'ni qayta hisoblamaydi.

### Entry point
`decision_layer.decision_service.decision_manager.DecisionManager.decide(signal, *, now=None,
trade_decision=None)` → `DecisionOutcome`. Stateless, hech qachon
ko'tarmaydi (signal duck-typed tarzda o'qiladi, shuning uchun
None/qisman signal ham aniqlangan natija beradi).

`decision_manager.py` deb nomlangan — `decision_engine.py` **emas**,
bu mavjud va frozen — bu xuddi STEP-08 frozen `signal_engine.py` bilan
bir qatorda `signal_layer/signal_service/manager.py`da qo'llagan bir
xil intizom.

### Reuse mapping (fork nuqtasi)
Base status — frozen verdict'ning **reuse**'i, boyroq lug'atga
map qilingan:

| Manba | Qiymat | → `DecisionStatus` |
|---|---|---|
| frozen `DecisionAction` (`trade_decision` orqali) | `APPROVE` | `APPROVE` |
| | `REJECT` | `REJECT` |
| | `NO_TRADE` | **`HOLD`** |
| canonical `SignalSchema.decision` (default manba) | `APPROVED` | `APPROVE` |
| | `REJECTED` | `REJECT` |
| | `PENDING` / `None` | **`HOLD`** |

`EXPIRE` — STEP-09 qo'shgan **yangi** vaqtga asoslangan status (eskirgan
canonical signal); frozen engine bu haqda tushunchaga ega emas.

### STEP-09 fayllari
| Fayl | Nima qiladi | Nima qilmaydi |
|---|---|---|
| `decision_status.py` | `DecisionStatus` lug'ati + reuse mapping'lari (`from_decision_action`, `from_signal_decision`) | verdict'ni qayta hisoblamaydi |
| `decision_model.py` | `DecisionOutcome` frozen dataclass (+ `to_dict`/`to_json`) | risk ko'rsatkichini saqlamaydi |
| `decision_rules.py` | sof decision qoidalari (reject-invalid, expire-stale, hold-low-confidence) | risk/stop'larni o'lchamaydi |
| `decision_router.py` | consumer route metadata (faqat APPROVE uchun `RISK`) | hech narsa yubormaydi |
| `decision_manager.py` | STEP-09 pipeline'ni orkestratsiya qiladi | frozen engine'ni o'zgartirmaydi |

### Boundary
STEP-09 **qilmaydi**: risk hisoblamaydi, position o'lchamaydi, order
yubormaydi, platform xabarini formatlamaydi, yoki
`decision_engine.py` / `models.py`ni o'zgartirmaydi. U faqat verdict va
uning asoslanishini qayd etadi; risk sizing — STEP-10. To'liq map uchun
`docs/PHASE_DECISION.md`ga qarang.
