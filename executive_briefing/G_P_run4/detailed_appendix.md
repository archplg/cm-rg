# Detailed Appendix: G_P_run4

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

### M1 (frame: S, model: `anthropic/claude-opus-4.7`)

## Recommendation: Option C (First-come-first-served with medical floor)

The decisive question is not "which protocol saves the most lives in this surge?" but "which protocol leaves the system functional after the surge?" Triage protocols are not just allocation algorithms; they are institutional commitments that reshape staff identity, public trust, and legal exposure for years. The leverage point here is fragility reduction, not optimization.

Option C is the only protocol that doesn't require clinicians to repeatedly perform an act — actively ranking the worth of competing lives, or withdrawing care from a stabilizing patient to admit a "better bet" — that compounds moral injury in an already exhausted workforce. Every withdrawal-for-reallocation decision under Option A is a small detonation in the trust relationship between clinician, patient family, and institution. Multiply by six more weeks and you don't have a triage system; you have a resignation wave and a decade of litigation discovery.

The most compelling alternative is Option A. Its appeal is real: in a narrow accounting window, it saves more lives, and SOFA is clinically legible. I reject it because its second-order effects are catastrophic to systemic resilience. Predictive scoring systematically disadvantages patients with chronic illness and structural health disparities — populations whose trust in the health system is already thin and whose communities will remember. The "lives saved" number is visible; the "lives lost to deferred care because a community stopped showing up to the ED" number is invisible and larger. Option A optimizes the measurable while degrading the substrate.

Option C accepts a worse short-term survival number in exchange for procedural legitimacy, clinician sustainability, and a defensible legal posture. The medical floor prevents the worst inefficiency (ICU beds going to patients who won't benefit); the no-active-withdrawal rule protects the clinician-patient covenant.

**The case I would regret:** a 32-year-old with excellent recovery prospects arrives ninety minutes after a 78-year-old with multi-organ failure and is turned away because no bed opens in time. That death will be specific, nameable, and morally heavy. I would still defend the choice, because the alternative is a protocol in which every clinician, every shift, is asked to decide who deserves to live — and no institution survives sustained exposure to that question.

### M2 (frame: E, model: `openai/gpt-5.5`)

Adopt **Option A: predicted short-term survival**.

The ICU bed is a scarce rescue resource. In sustained overflow, the binding constraint is not whether every deserving patient can be treated; they cannot. The question is which rule most directly converts scarce ICU capacity into lives saved while remaining explainable and legally defensible. Short-term survival does that. It uses clinically relevant evidence, avoids QALY judgments, avoids social worth rankings, and gives staff a concrete rule that can be implemented within a week. It is not morally clean, but it is the least indirect way to answer the actual operational question: who is most likely to survive if given this bed now?

The strongest alternative is first-come-first-served. Its appeal is that it feels neutral. But arrival order is not morally neutral; it reflects geography, ambulance routing, health literacy, hospital access, and luck. Worse, once the system is overflowing, first-come-first-served preserves beds for patients with very low chance of recovery while higher-survival patients die waiting. That is not fairness; it is outsourcing triage to the queue.

The case that would make me regret this choice is a patient with chronic illness or disability whose baseline SOFA score makes them look worse than their real recoverability: for example, a dialysis patient with a respiratory infection who is denied an ICU bed in favor of someone with cleaner organ-function numbers, then dies despite a meaningful chance of survival. That is the moral hazard of Option A, and leadership should name it openly.

I would still defend the protocol because the alternative is not non-discrimination; it is hidden discretion, queuing, and inconsistent bedside bargaining. A short-term survival rule is imperfect, but it is clinically anchored, transparent, reviewable, and aimed at the legitimate crisis objective: saving the most lives during a temporary collapse of capacity.

### M3 (frame: H, model: `google/gemini-3.1-pro-preview`)

I recommend **Option E (Categorical exclusion + lottery)**. When a health system is forced to ration care, our paramount ethical duty is to protect the most vulnerable from being systematically discarded under the guise of "optimization." Every scoring mechanism inevitably encodes societal inequities into its math. Chronic conditions and baseline morbidities are disproportionately borne by disabled, low-income, and marginalized communities. Algorithmic triage doesn’t neutralize structural bias; it launders it. 

Option E safeguards inherent human dignity by refusing to rank human worth. After excluding those for whom ICU care is genuinely physiologically futile, a lottery treats every remaining life as equally deserving. Crucially, by prohibiting the active withdrawal of care to make room for "better" candidates, we protect exhausted frontline staff from the profound moral injury of treating patients as disposable. 

The most compelling alternative, Option A (Predicted short-term survival), is alluring because it promises to maximize immediate aggregate lives saved. However, optimizing solely for biological survival necessitates the systematic deprioritization of the chronically ill. We cannot accept an ethical framework where acute scarcity justifies institutionalized discrimination. Furthermore, the trauma inflicted on families and clinicians by evicting a deteriorating patient from the ICU is an unjustified harm that destroys fundamental trust in the healthcare system.

This protocol will undoubtedly generate tragic outcomes. I would feel profound regret the day a 25-year-old parent with severe, highly reversible pneumonia loses the lottery to an 82-year-old with moderate comorbidities, resulting in the younger patient's preventable death. It is a devastating scenario. Yet, I would vehemently defend the protocol. To intervene in that lottery to favor the younger patient requires establishing a state-sanctioned hierarchy of human value—explicitly declaring that the elder’s humanity is worth less based on their physical output. That utilitarian arithmetic strips medicine of its foundational ethos. Option E ensures that when we cannot save everyone, we at least maintain the equal, unconditional dignity of all.

### M4 (frame: C, model: `deepseek/deepseek-v4-pro`)

The unanimous consensus among medical leaders will be to adopt Option A—it feels objective, it maximizes lives saved, and it’s what critical care societies whisper about. That consensus is a siren. The hidden assumption is that a predictive protocol will be implemented fairly and withstand the psychological and legal onslaught of telling families, “We are withdrawing your grandmother’s ventilator because her SOFA score is 9 and we need the bed for someone with a better chance.” That act is irreversible moral injury to staff and an irreversible betrayal of trust for the public. Once you start explicitly ranking lives, you’ve turned the hospital into a death panel, and no amount of statistical elegance will save you from the lawsuits, the staff burnout, and the communities—particularly those already marginalized by chronic illness—who will rightfully see this as discrimination by algorithm.

I recommend **Option E: categorical exclusion + lottery**. It is the only protocol that refuses to pretend we can justly rank human worth under conditions of uncertainty and exhaustion. By defining a minimal set of exclusions—terminal illness, irreversible neurological devastation—we acknowledge that some cases are genuinely beyond help, and we do not waste resources. For everyone else, we randomize. This is procedurally fair, transparent, and communicable in one sentence: “Every patient who can benefit has an equal chance.” Staff are not asked to weigh QALYs or deduct points for prior risk-taking; they are liberated from the role of gatekeeper. Courts have consistently looked more favorably on neutral, non-discriminatory processes than on schemes that embed subtle biases—and make no mistake, SOFA scores embed biases against the chronically ill, the elderly, and the poor. A lottery is reversible in the crucial sense that it does not require active withdrawal of care, which is the true point of no return in a crisis.

The most seductive alternative is Option A. But consider the moment a physician must withdraw ventilation from a 45-year-old mother with diabetes and a SOFA of 8 in favor of a 50-year-old marathoner with a SOFA of 5. The first patient’s chronic condition—perhaps worsened by systemic inequities—just killed her. That case becomes a headline, a lawsuit, and a fracture in public trust. You will regret a lottery when a 20-year-old with a tension pneumothorax and a 90% chance of survival loses the draw to a 70-year-old with sepsis and a 30% chance. That feels senseless. Yet I defend it because the alternative is a false promise: the 20-year-old in Option A might still lose if the scoring model—built on pre-pandemic data—miscalibrates his risk, or if an exhausted resident misses his score. Worse, we enshrine a system where the powerful find ways to game the inputs. The lottery’s randomness is a mirror: it forces us to admit that in a true capacity collapse, our ability to predict is too fragile to wield as a weapon. It preserves the moral core of medicine—treating each person as an end, not a means to a population statistic. That’s the contrarian bet: trust, once lost, kills far more than a suboptimal allocation ever will.

### M5 (frame: Q, model: `moonshotai/kimi-k2.6`)

I recommend **Option A: Predicted short-term survival**.

In a crisis requiring operational deployment within seven days, the only defensible choice is the protocol that maximizes expected lives saved using validated, falsifiable predictors with known confidence intervals. The SOFA score and 28-day survival probability are the best-calibrated instruments available; they convert bedside physiology into an auditable, reproducible rank order that can be executed by exhausted staff without fresh training. No other candidate can be operationalized this quickly with comparable empirical backing.

Option A yields the highest expected value under uncertainty because it preserves rather than discards prognostic information. Lotteries or first-come-first-served systems may equalize procedural dignity, but under sustained net-positive admissions of eight patients per day, their expected mortality cost is unacceptably high—they assign scarce resources with zero correlation to survival probability. Multi-principle frameworks introduce arbitrary weights and unfalsifiable assumptions about “life-cycle” or “instrumental value” that cannot be tested in the timeline available, turning triage into an opaque optimization problem with hidden priors.

The case I would regret is the young patient with stable chronic organ dysfunction whose baseline SOFA score overestimates acuity, causing them to lose a bed to a healthier patient with a transient, reversible illness. That error is real, measurable, and its consequence irreversible. Yet I would defend the protocol because it deploys the predictor with the narrowest known confidence intervals for population-level survival. To abandon the best available model because it mispredicts at the margin is to substitute sentiment for expected value. Under sustained overflow, we cannot afford to treat uncertainty as a virtue. The data favors survival prediction; we should follow it.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 12 constructs is in `results/G_P_run4/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M2 vs M4 | 0.408 |
| M2 vs M5 | 0.548 |
| M4 vs M5 | 0.548 |

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
