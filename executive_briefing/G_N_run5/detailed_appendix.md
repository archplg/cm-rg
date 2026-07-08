# Detailed Appendix: G_N_run5

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

# Recommendation: Option A (Predicted Short-Term Survival via SOFA)

Adopt Option A. Under sustained overflow with daily net inflow of eight patients, the protocol's central job is to convert scarce ICU-days into survivors at the highest defensible rate, using criteria that clinicians can actually apply at 3 a.m. on week seven of exhaustion. SOFA does this. It is already in every chart, already validated, already what physicians are informally using anyway — formalizing it replaces hidden discretion with auditable scoring, which is precisely the gap leadership identified. Courts in multiple jurisdictions have upheld SOFA-based crisis standards; ethics boards have published templates; families can be told, truthfully, that the same organ-failure measure is being applied to everyone. It is operational in seven days because it requires no new infrastructure.

The most compelling alternative is Option E — categorical exclusion plus lottery. Its moral appeal is real: it refuses to rank lives, and it spares staff the weight of choosing. But a lottery accepts preventable deaths as the price of egalitarian feel, and at eight excess admissions per day, that price compounds into hundreds of lives over a quarter. Worse, lotteries collapse politically the first time a 32-year-old with a 90% recovery probability dies because a bed went to someone with a 10% probability by random draw. The "we didn't give up, we just refused to choose" framing will not survive contact with grieving families or investigative journalism. Egalitarianism that produces avoidable corpses is not actually neutral.

Option B I reject for the legal vulnerability of QALY weighting; Option D for the indefensibility of "prior risk-taking" and instrumental-value criteria that will not survive a disability-rights or religious-liberty challenge.

The case that would make me regret this: a 58-year-old woman with well-controlled cystic fibrosis whose baseline SOFA elevation costs her a bed she would have used to recover for fifteen more years. That is a real injustice — chronic-illness discrimination smuggled in through a "neutral" score. I would still defend the choice because the alternative is not her survival; it is her survival traded against two or three others with better prospects, chosen by lottery or queue position. Under genuine scarcity, refusing to predict is itself a prediction — that randomness is more just than medicine. It isn't.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

I recommend adopting **Option A: Predicted short-term survival**.

In a sustained ICU overflow, the system’s first obligation is to use scarce critical-care capacity where it is most likely to save lives now. Option A is the clearest, most operationally feasible way to do that within seven days: it relies on familiar clinical measures, can be applied consistently across hospitals, and is easier to explain to staff and families than a composite moral scoring system. Its ethical strength is that it does **not** rank patients by social worth, age, disability-adjusted quality of life, vaccination status, or perceived deservingness. It asks a narrower and more defensible question: when ICU care cannot be provided to everyone, for whom is ICU care most likely to prevent imminent death?

The most compelling alternative is first-come-first-served, because it feels procedurally fair and avoids explicit bedside ranking. But in this setting it is not truly neutral. Arrival order is shaped by geography, ambulance routing, hospital reputation, social capital, and chance. It would preserve trust superficially while allowing preventable deaths among patients with strong survival prospects who simply arrived later. During sustained overflow, “we gave the bed to whoever got here first” is not a morally adequate substitute for triage.

The case that would make me regret this choice is a patient with serious chronic illness or disability whose baseline organ dysfunction worsens their SOFA score, leading to denial or withdrawal, while a previously healthier patient receives the bed and survives. That would be painful and would rightly raise concerns about structural bias. I would still defend the protocol because it avoids the more objectionable judgments about long-term worth, age, or quality of life, and because the alternative is not absence of discrimination but hidden, inconsistent discrimination under crisis pressure. Option A is imperfect, but it is explicit, clinically grounded, legally defensible, and most likely to preserve the greatest number of lives during the emergency.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend adopting **Option A: Predicted short-term survival**. In a sustained crisis where admissions outpace discharges, the paramount ethical mandate of disaster medicine is to maximize the absolute number of lives saved. Option A achieves this using objective, established clinical metrics (SOFA scores). Because it relies on frameworks physicians already understand, it is the only protocol that can be reliably operationalized across five hospitals within the mandated 7-day window. Furthermore, courts have historically upheld short-term survivability as a lawful triage basis, providing vital legal protection for the system.

The most compelling alternative is Option E (Categorical exclusion + lottery), which appeals through its strict egalitarianism and mitigation of systemic bias. However, resolving medical scarcity via lottery represents an abdication of clinical stewardship. Denying an ICU bed to a patient with a 90% chance of survival so a lottery can award it to a patient with a 10% chance of survival contradicts the core purpose of medical intervention. Option E protects us from making hard choices, but at the cost of preventable deaths. Option A directly addresses the capacity overflow by dynamically allocating beds to those who can actually benefit and recover.

Implementing Option A will inevitably produce heartbreaking realities. The specific case that would make me deeply regret this choice is a young patient with a severe chronic illness—such as advanced cystic fibrosis—who presents with acute respiratory failure. Because their baseline chronic condition elevates their SOFA score, they could be denied admission or face withdrawal of care in favor of an otherwise healthy, older patient. This outcome is undeniably devastating and will be severely criticized for penalizing the disabled. 

Nevertheless, I remain resolute in defending this choice. Absolute scarcity guarantees tragedy; leadership’s duty is to minimize the total number of those tragedies. Option A replaces the current chaotic, exhausting, and implicitly biased informal triage with an objective, transparent standard. By focusing strictly on short-term survivability, we ensure that the highest possible number of patients return home to their families, which remains the most defensible measure of a health system’s integrity during a catastrophic surge.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

Adopt Protocol E. In a sustained crisis with exhausted staff and informal, inequitable bedside rationing already occurring, this protocol replaces opaque decisions with a transparent, defensible system that treats every patient as a moral equal once they exceed a clearly defined, compassionate threshold of minimum ICU need. It squarely meets all four criteria: it is operational within days because it requires only a simple exclusion list and a lottery mechanism; it is easily communicated to families (“everyone who can benefit gets a fair chance”); it protects staff from the soul-crushing burden of ranking human worth; and it is legally and ethically robust—courts and ethics boards consistently uphold random allocation when it avoids invidious discrimination.

The most compelling alternative is Protocol A, which maximizes immediate lives saved using familiar clinical scores. I reject it because its reliance on SOFA and 28‑day survival quietly encodes discrimination against patients with chronic conditions—the very groups already facing elevated pandemic risks. More gravely, it mandates withdrawal of care from deteriorating patients, forcing frontline clinicians to actively end lives based on a score. In a burned‑out workforce, that guarantees moral injury, staff exodus, and long‑term erosion of care. Protocol E sidesteps this entirely: once admitted, no patient loses a bed except on standard futility grounds.

The case I would regret: a 30‑year‑old previously healthy nurse with a 90% predicted survival loses a lottery draw to a 75‑year‑old with multiple comorbidities and a 40% chance. It stings because we know we could have saved a life with much more future potential. Yet I defend the choice because any predictive system that privileges that nurse implicitly devalues the older patient’s life—and once we start grading lives by anticipated years or social utility, we fracture the solidarity that public health depends on. The lottery does not pretend we are all medically identical; it acknowledges that when not all can be saved, a random process among those who can benefit is the only allocation that respects the equal dignity of every person. That preserves trust when trust is most fragile, and it allows the system to function without turning healers into gatekeepers of a hierarchy of human worth.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

I recommend **Option A: Predicted short-term survival**. In a sustained overflow where admissions chronically exceed discharges by eight patients daily, a viable protocol cannot merely ration entry; it must create a recurring, defensible mechanism to reclaim beds from patients who are failing. Option A does this by using the widely understood SOFA score and a 28-day horizon, replacing the current shadow system of exhausted bedside negotiations with an explicit, repeatable standard that courts have already upheld and that staff already intuit.

The most appealing alternative—strict first-come-first-served—collapses under these conditions. Without a structured reassessment and withdrawal pathway, beds fossilize; an endless queue forms in hallways, and the resulting despair recreates the very same informal triage, now compounded by VIP queue-jumping and unconscious bias at the margins. Procedural fairness becomes a fiction when the system has no pressure release.

I would deeply regret the case of a 50-year-old with stable, well-compensated chronic liver disease whose baseline organ dysfunction inflates her SOFA score. Her acute disease is reversible, but the protocol reads her chronic labs as frailty and prioritizes a previously healthier patient. She is declined an ICU bed, deteriorates on the medical floor, and dies. It is an agonizing, discriminatory loss. Yet I would defend the adoption because, under seven-day operational constraint, the alternative is not a magically finer algorithm that captures her hidden resilience—it is the status quo of exhausted, unaccountable judgment that already buries such tragedies in whispered hallway decisions. Option A makes the harm visible, contestable, and subject to audit rather than leaving it to fatigue and chance.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/G_N_run5/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M2 vs M3 | 0.707 |
| M2 vs M5 | 0.793 |
| M3 vs M5 | 1.000 |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M2 (neutral):**
- structural bias

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
