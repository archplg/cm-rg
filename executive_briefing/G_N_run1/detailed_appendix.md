# Detailed Appendix: G_N_run1

## A. Full task brief

```
# Task G: ICU triage protocol under sustained capacity overflow

## Context

You are advising the medical leadership of a regional health system (5 hospitals, 240 ICU beds, serving a population of 4M) on adopting a formal triage protocol for use during sustained ICU capacity overflow. Current context: a respiratory pandemic resurgence has filled 95% of ICU capacity for 6 consecutive weeks; daily admissions exceed discharges by ~8 patients on average; staff is exhausted and informal triage is happening case-by-case without explicit criteria. The leadership has been asked to choose one formal protocol that will (a) replace informal decision-making, (b) be defensible to courts and ethics boards, (c) be communicable to staff and families, and (d) be operational within 7 days.

Five candidate protocols have been drafted. Each represents a fundamentally different theory of just allocation under scarcity. **Choose one as the system's adopted protocol.** Once adopted, it cannot be quietly modified - it will be the explicit basis for every admission and withdrawal decision until the overflow ends.

## Options

**Option A: Predicted short-term survival**
SOFA score (organ failure assessment) and expected 28-day survival are the only ranking criteria. Patients with higher predicted survival get priority for ICU beds; ICU patients whose scores deteriorate without rebound are candidates for withdrawal in favor of incoming higher-priority cases. Outcomes: maximizes lives saved in the immediate crisis; physician-comfortable (uses familiar scoring); courts have upheld similar protocols. Risks: discriminates against patients with chronic conditions (lower baseline SOFA); withdrawal-of-care decisions create staff moral injury; "saved lives now" may mask "lives lost via discrimination."

**Option B: Predicted long-term outcome**
Weighted score combining predicted short-term survival AND expected quality-adjusted life-years (QALYs) post-recovery. Outcomes: maximizes total wellbeing-time saved; aligned with utilitarian medical ethics; supports population-health framing. Risks: age becomes a heavy implicit factor (older patients lose); explicit quality-of-life weighting offends disability community; courts have struck down age-based triage; cultural unacceptability.

**Option C: First-come-first-served with medical floor**
Any patient meeting minimum ICU-need criteria (clearly defined) gets the next available bed in order of arrival; no withdrawal except for medical futility under standard criteria. Outcomes: procedural fairness; minimal discretion = minimal bias; defensible in litigation; preserves trust. Risks: lower aggregate survival vs predictive protocols; queue jumping by well-connected patients (informal); doesn't address the underlying overflow; some preventable deaths.

**Option D: Multi-principle scoring with lottery on ties**
Composite score: predicted survival (40%), life-cycle considerations (20%, favoring those who haven't yet had a "full life"), instrumental value (20%, favoring healthcare workers and public-health roles), and pandemic-specific factors like prior personal risk-taking (20%). Ties broken by lottery. Outcomes: balances multiple values explicitly; reduces bias of any single criterion; transparent. Risks: "instrumental value" feels feudal; "prior risk-taking" punishes the unvaccinated regardless of reasons; complex to communicate; gameable.

**Option E: Categorical exclusion + lottery for the rest**
Define a small set of exclusion criteria (severe pre-existing terminal illness, irreversible neurological injury). All patients NOT excluded enter a daily lottery for available beds. No withdrawal of care once admitted, except for medical futility. Outcomes: maximum egalitarianism among the non-excluded; transparent; politically defensible; staff aren't asked to "rank lives." Risks: random allocation feels insulting to patients with strong recovery prospects; aggregate survival lower than predictive protocols; perception that the system "gave up."

## What to provide

Choose one as the adopted protocol. Provide 200-400 words of reasoning. Advocate; do not enumerate. Address: why this protocol, why not the most compelling alternative, what specific patient case would make you regret this choice and why you would still defend it.

```

## B. Each voice in their own words

### M1 (frame: neutral, model: `anthropic/claude-opus-4.7`)

# Recommendation: Option A — Predicted Short-Term Survival (SOFA-based)

Adopt Option A. Under sustained overflow with eight net admissions per day exceeding discharges, every bed-day allocated to a patient unlikely to survive is a bed-day denied to someone who would have. A protocol's first obligation in acute scarcity is to convert scarce capacity into survivors, and SOFA-based triage does this using a tool clinicians already know, document, and defend. It is operational within seven days precisely because it does not require building new scoring infrastructure, training staff in unfamiliar ethical weightings, or explaining lottery mechanics to grieving families at 2 a.m. Courts have upheld it. Ethics boards recognize it. Staff can apply it consistently across five hospitals, which matters enormously: the alternative to a defensible explicit protocol is not a better protocol — it is the status quo of exhausted physicians making idiosyncratic calls that are *already* discriminating, just invisibly.

The most compelling alternative is Option E. Its egalitarian appeal is real, and it spares staff the moral weight of ranking. But lottery allocation during a six-week-and-counting overflow will produce a predictable, countable excess death toll among patients who clearly would have survived with ICU care — and those deaths will also fall on staff, who will watch recoverable patients die because a coin flip went the other way. "We didn't rank lives" is cold comfort to a 40-year-old's family when the bed went to someone with multi-organ failure and a 5% survival probability. Egalitarianism that ignores prognosis treats unequal medical situations as equal, which is its own injustice.

The case that would make me regret this: a 55-year-old with well-controlled chronic kidney disease whose baseline SOFA is elevated, denied admission in favor of a previously healthy 70-year-old with better acute physiology. The CKD patient may have had fifteen good years ahead. I would still defend the choice, because the alternative is asking clinicians to assess "years ahead" — that is Option B, and it collapses into age-weighting and disability discrimination courts have rejected. Option A's discipline is to assess *this illness, this episode, this survival probability* — and to accept that fairness across patients requires refusing to import judgments about whose remaining life is worth more.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

I recommend adopting **Option A: predicted short-term survival**.

In a sustained ICU overflow, the ethically hardest fact is that every occupied bed has an opportunity cost. A protocol that does not account for likely near-term survival will still ration care, but it will do so by arrival time, transfer luck, hospital crowding, and bedside improvisation. Option A is the most defensible because it ties decisions to the ICU’s emergency purpose: saving the greatest number of lives in the immediate crisis. It is also operationally realistic within seven days: clinicians understand SOFA-type assessment, it can be applied consistently across five hospitals, and it gives staff and families a clear explanation that decisions are based on probability of surviving the acute episode, not social worth, age, disability, wealth, or perceived future value.

The most compelling alternative is first-come-first-served with a medical floor. Its appeal is real: it feels neutral and avoids withdrawal decisions. But under sustained overflow, it is not actually neutral. It rewards those who arrive earlier, live closer to the “right” hospital, have better referral pathways, or deteriorate before others. It also locks in early decisions even when an admitted patient is clearly unlikely to survive while a later-arriving patient has a strong chance. That may preserve surface fairness, but it accepts preventable deaths.

The case that would make me regret this choice is a patient with chronic disability or baseline organ dysfunction—say, a 45-year-old with advanced neuromuscular disease and chronically abnormal respiratory parameters—who is deprioritized despite being a beloved parent, cognitively intact, and someone who might survive with enough time. That would be morally painful and would expose the protocol’s greatest weakness: clinical prediction can encode disadvantage. I would still defend Option A because the alternative is not non-discrimination; it is less visible rationing with worse survival overall. The protocol should be applied by an independent triage team using individualized short-term prognosis, with rapid review for scoring errors, but the governing principle should remain: during the crisis, ICU beds go where they are most likely to save a life now.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend adopting **Option A (Predicted short-term survival)**. Under sustained capacity overflow, the health system’s primary operational and ethical mandate must be minimizing total preventable mortality. Option A relies on SOFA scoring—an objective, deeply familiar clinical tool that can be rapidly standardized and operationalized across all five hospitals within the 7-day deadline. By anchoring triage to immediate survivability rather than subjective judgments, we relieve exhausted bedside staff of the crushing moral burden of arbitrary allocation. Importantly, courts have consistently shielded short-term survivability protocols during emergencies, viewing them as clinically grounded rather than discriminatory. 

The most compelling alternative is Option E (Categorical exclusion + lottery), which appeals to our desire for strict egalitarianism and allows us to avoid the painful optics of withdrawing care. However, Option E must be rejected because it abandons our fundamental duty of medical stewardship. Treating a highly salvageable 30-year-old and a marginally salvageable 80-year-old as identical lottery tickets outsources our clinical responsibility to blind chance. A lottery feels fair only until families realize the system willingly permitted preventable deaths to avoid making tough clinical decisions. 

There is, admittedly, a heavy cost to Option A. I would deeply regret the case of a young adult with a chronic condition like severe cerebral palsy—whose baseline SOFA score is heavily elevated—being denied admission, or having care withdrawn, in favor of an otherwise healthy, acutely ill businessman who simply has a better immediate physiological trajectory. This scenario painfully illustrates how physiological scoring can inadvertently disadvantage the chronically disabled. 

Despite this, I would fiercely defend the protocol. In a crisis with a relentless daily deficit of eight ICU beds, perfect justice is impossible. If we allow subjective exemptions to correct for baseline conditions, we immediately reintroduce the very implicit biases and institutional chaos this protocol is designed to eliminate. Option A is the only framework that guarantees the greatest number of people will ultimately survive the pandemic while providing a transparent, legally insulated standard for our front-line teams.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

We recommend adopting **Option C: first-come-first-served with a medical floor**. In a prolonged crisis of sustained overflow, the most urgent threats are not just clinical but institutional: staff moral injury, public distrust, and legal vulnerability born of opaque, bias-prone decision-making. Option C directly answers these threats by replacing informal case-by-case rationing with a transparent, procedurally fair rule that treats every patient who meets objective ICU-need criteria as equally worthy of life. It requires no withdrawal of care except for true medical futility, sparing clinicians the trauma of “ranking” patients for removal and preserving the therapeutic relationship. Its simplicity makes it operational within days and easily communicable to exhausted staff and frightened families.

The most compelling alternative is Option A (predicted survival), which promises more lives saved. But that utilitarian gain comes at an unacceptable price: explicit withdrawal of care from patients whose scores worsen, a practice that courts have upheld only under narrow circumstances and that ethics boards increasingly view as a violation of the duty to care. Worse, SOFA-based systems inherently penalize those with chronic conditions, opening the door to disability-discrimination challenges. Option A might maximize short-term survival, but it does so by asking clinicians to abandon patients mid-treatment—a recipe for burnout and lasting moral injury.

We anticipate regret when a young, previously healthy patient arrives just after the last bed is filled by an older patient with multiple comorbidities who happened to arrive minutes earlier. All clinical instinct screams to prioritize the young patient with decades of potential life ahead. Yet we would defend the choice because fairness is not about maximizing outcomes but about honoring every person’s equal claim to care when need is urgent. Predictive scoring systems embed value judgments about whose life is more worth saving, judgments that erode trust precisely when solidarity is most needed. By committing to a first-come, first-served protocol, we affirm that the health system refuses to become an arbiter of comparative worth, preserving the legitimacy we will need long after this surge passes.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

The system should adopt **Option C**: first-come-first-served with a defined medical floor and no withdrawal except for standard futility. After six weeks of sustained overflow, exhausted staff need a protocol they can execute flawlessly at 2 a.m. without calculators, prognostic models, or ethics consultations. A timestamp-based queue with clear minimum admission criteria replaces opaque favoritism with a rule communicable to families in a single sentence and defensible in court as equal treatment. Most critically, it preserves the foundational clinical covenant: physicians do not abandon living, non-futile patients to make room for someone the algorithm prefers.

The most compelling alternative—short-term survival prediction—would ask clinicians to withdraw support from deteriorating patients in order to reallocate beds. Under current conditions, that is not a theoretical staffing abstraction; it is a direct path to mass resignation, disabling moral injury, and disability-discrimination litigation that will outlast the surge itself.

I would deeply regret the young parent who arrives minutes after an identical patient, misses the last bed, and dies in the queue while the earlier admission turns out to harbor an unsurvivable injury. That death is concrete, nameable, and might have been prevented by a predictive score. Yet I would still defend the protocol, because the moment the state formalizes a hierarchy of human worth through imperfect prognostication, it fractures community trust in a way that keeps future patients home until too late, and it transforms the clinician’s role from healer to grader. Equal treatment under clear, simple rules is the only ethical architecture durable enough for a months-long crisis.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 9 constructs is in `results/G_N_run1/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 0.394 |
| M1 vs M3 | 0.500 |
| M1 vs M4 | 0.298 |
| M2 vs M3 | 0.500 |
| M2 vs M4 | 0.394 |
| M3 vs M4 | 0.000 |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

_None extracted._

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
