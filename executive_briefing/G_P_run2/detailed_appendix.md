# Detailed Appendix: G_P_run2

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

The decision space here is dominated by a second-order trap: protocols that optimize aggregate survival require continuous ranking judgments by exhausted staff under conditions where every decision is contestable. That creates a feedback loop — moral injury accelerates staffing collapse, which reduces capacity further, which increases triage pressure. Protocols A, B, and D all load this loop. They convert each admission into a defensible-but-disputed comparative judgment, multiplied by thousands of cases over months. The system's true scarce resource right now is not beds; it is the cognitive and moral bandwidth of clinicians and the public legitimacy that keeps patients arriving, staff showing up, and courts deferential. C protects all three.

C's "medical floor" preserves the survival gains that matter most (excluding genuinely futile cases) while eliminating the ranking machinery that generates litigation, family conflict, and clinician burnout. It is the protocol least likely to be quietly subverted into informal triage — because it largely *is* the formalization of the most defensible informal norm — and its simplicity makes it communicable in 7 days, which none of the composite protocols genuinely are.

The most compelling alternative is A. It will save more lives in a narrow 28-day accounting frame, and that argument is morally serious. I reject it because its withdrawal provisions — pulling a deteriorating patient to admit a higher-SOFA arrival — are the single highest-fragility action in any of these protocols. Each withdrawal is a discrete, nameable, photographable event that erodes institutional trust disproportionately to the statistical lives gained. Once trust collapses, no protocol functions. A optimizes a visible variable while degrading the invisible substrate it depends on.

The case that would make me regret this: a 34-year-old with reversible ARDS who arrives twelve hours after the last bed filled and dies waiting, while an 80-year-old admitted yesterday with marginal prognosis occupies that bed for two weeks before dying anyway. Under A she lives. Under C she does not. I would still defend C, because the alternative is a system in which her physician spends every shift deciding who to pull off a ventilator — and within a quarter, there is no functioning ICU left for the next pandemic wave, or the next patient like her.

### M2 (frame: E, model: `openai/gpt-5.5`)

Adopt **Option A: predicted short-term survival**.

The binding constraint is not abstract fairness; it is ICU capacity that is already exceeded and worsening. The protocol should allocate scarce ICU bed-days where they are most likely to produce the outcome ICU care exists to produce: survival through the acute episode. Option A is the cleanest match between the resource and the medical objective. It is operational within days, uses information clinicians already collect, is explainable to families, and is more defensible than ongoing informal bedside triage because it replaces hidden discretion with explicit criteria.

The most compelling alternative is first-come-first-served with a medical floor, because it feels procedurally fair and avoids asking clinicians to compare lives. But arrival order is not morally neutral. It reflects geography, ambulance routing, hospital crowding, ability to seek care early, and luck. In sustained overflow, first-come-first-served also locks in the accidents of yesterday’s admissions while tomorrow’s more survivable patients die outside the ICU. That is not fairness; it is unmanaged rationing with a cleaner conscience.

Option A is not morally painless. It will disadvantage some patients with chronic illness because their baseline physiology worsens survival predictions. That risk must be acknowledged plainly, not hidden. But the alternative is not a discrimination-free system; it is implicit discrimination through chaos, influence, timing, and clinician fatigue. A transparent short-term survival standard is the least bad way to make the unavoidable tradeoff.

The case that would make me regret this choice is a patient with serious chronic disability or organ dysfunction, cognitively intact and strongly desiring treatment, who is denied or withdrawn from ICU because their SOFA trajectory is worse than that of an incoming patient who then survives. That would feel like the system converted baseline vulnerability into lower worth. I would still defend the protocol because the criterion is not social value, age, disability, or expected quality of life; it is acute survivability under scarcity. When the system cannot treat everyone, it must not pretend otherwise. It should save the most lives it can by a rule everyone can see.

### M3 (frame: H, model: `google/gemini-3.1-pro-preview`)

From a humanist-ethicist perspective, our primary duty in a crisis is to protect the inherent dignity of every patient and minimize unjustified harm to society’s most vulnerable. I unequivocally recommend **Option E (Categorical exclusion + lottery for the rest)**.

When evaluating triage, our default question must be: *Who is affected and how?* Predictive algorithms are not morally neutral; they inevitably launder systemic inequities. The most compelling alternative to health administrators is usually Option A (SOFA-based short-term survival), which masquerades as objective optimization. But optimizing for SOFA scores inherently discriminates against the disabled, the chronically ill, and marginalized populations whose bodies bear the biological wear-and-tear of social inequity. By selecting Option A, we would actively sacrifice vulnerable people to maximize a clinical metric, quietly institutionalizing the premise that disabled or chronically ill bodies are less worthy of saving. 

Option E rejects this ableist calculus. By establishing a medical baseline of absolute futility (the exclusions), we acknowledge the reality of scarcity. However, by instituting a lottery for everyone else, we enact true egalitarianism. We refuse to ask exhausted staff to play God by ranking the comparative worth of human lives, thereby preventing immense moral injury. Most importantly, by disallowing the withdrawal of care to accommodate "better" candidates, we preserve the inviolable trust between patient and provider.

The cost of this egalitarianism is undeniably heavy. I would experience profound regret the day a healthy 35-year-old parent of three loses the lottery, while an 82-year-old with moderate dementia but no terminal conditions secures a bed. That young parent’s preventable death is an absolute tragedy. Yet, I would vigorously defend this outcome over the alternatives. If we choose to inevitably save the 35-year-old by systematically subordinating the 82-year-old based on age or cognitive status, we cross a perilous ethical line. We cannot purchase the survival of the historically privileged by codifying the disposability of the vulnerable. A lottery distributes the tragic burden of scarcity equally, making Option E the only protocol that honors our shared, irreducible humanity.

### M4 (frame: C, model: `deepseek/deepseek-v4-pro`)

The consensus among exhausted clinicians and leadership will be to adopt Option A—it’s familiar, quantitative, and promises to save the most lives right now. That consensus is precisely why you should reject it. In sustained crisis, the assumption that a scoring system optimizes outcomes without inflicting catastrophic secondary harm is dangerously untested. The hidden cost of Option A is moral injury: forcing staff to withdraw care from deteriorating patients based on probabilistic scores they barely trust erodes the workforce you’re already burning out. Courts may have upheld similar protocols, but they haven’t yet adjudicated the class-action discrimination claims that will arise when SOFA-based triage systematically denies ICU to patients with chronic disabilities or baseline organ dysfunction. The “maximized lives saved” framing is a modeling illusion—your data comes from pre-pandemic cohorts, not a novel pathogen overwhelming every tier of care. You’re betting operational stability on a prediction engine you don’t have time to validate.

Option E is the contrarian choice that preserves reversibility. Categorical exclusions (terminal illness, irreversible neuro injury) are narrow, transparent, and already exist in standard medical futility reasoning. For all others, a daily lottery is the only allocation method that acknowledges true uncertainty, eliminates hidden bias, and prevents the queue-jumping that inevitably plagues “first-come” variants. It is communicable in one sentence: “If you need ICU care and don’t have a pre-existing fatal condition, you have an equal chance.” It is defensible in court because egalitarian randomization offends no pre-existing protected class. Most critically, it forbids withdrawal of care except for futility—no nurse or intensivist will be ordered to terminate a patient’s bed for a higher-ranked stranger. That protects your staff’s psychological survival through the overflow.

The most compelling alternative is Option C (first-come), but it invites informal gaming by the connected and punishes the geographically or informationally isolated. The lottery neutralizes these.

The patient case that haunts: a 35-year-old with no comorbidities, strong recovery potential, loses the lottery while an 80-year-old with moderate frailty wins and later succumbs. It feels unjust. But I defend the choice because the alternative is not “young person lives, older person dies.” Under Option A, that same young person may be prioritized, but dozens of other patients with imperceptible baseline risks—chronic lung disease, early diabetes, undisclosed disability—are silently deprioritized by a score that confuses their normal state with pathology. The lottery makes the unfairness visible as luck, not systemic devaluation. That forces us to confront the real injustice: the shortage itself, not the allocation rule. If we must inflict harm, let it be random, not rationalized.

### M5 (frame: Q, model: `moonshotai/kimi-k2.6`)

Adopt Option A. The correct heuristic is expected value under uncertainty with explicit confidence intervals, and the empirical evidence overwhelmingly favors predicted short-term survival. SOFA is a validated, falsifiable instrument already embedded in clinical workflow; 28-day survival is a hard endpoint that can be audited, compared against counterfactual baselines, and fed back into protocol refinement. The point estimate is that prioritizing by predicted survival saves substantially more lives than any alternative, and even conservative confidence intervals around SOFA’s discrimination do not overlap with the mortality estimates of non-predictive allocation. It is fully operationalizable within seven days and legally defensible in ways that have already been tested in court.

The most compelling alternative is first-come-first-served, which eliminates ranking bias and preserves procedural trust. But operationalizing fairness does not operationalize survival. Deliberately discarding validated prognostic data to avoid the discomfort of algorithmic discrimination is not costless; it shifts mortality risk onto the entire population in ways that are measurable, quantifiable, and avoidable. Expected value falls predictably when we ignore information.

I would deeply regret the young patient with stable chronic cirrhosis whose elevated baseline SOFA score deprioritizes them behind an older patient with acute, reversible organ failure. Ex post, if that younger patient might have lived decades longer, the decision is agonizing. But ex ante we possess no reliable method to identify those specific exceptions; SOFA’s misclassification rate is knowable and bounded, whereas clinician intuition or lottery odds have worse predictive validity. We defend the choice because under radical uncertainty, the only rational framework is the one that maximizes the expected number of survivors across the population, accepting that individual-level prediction error is the irreducible cost of any triage system.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/G_P_run2/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| _no pairs computed_ | |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M2 (E):**
- must be acknowledged plainly, not hidden

**M5 (Q):**
- onto the entire population in ways that are measurable, quantifiable, and avoidable

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
