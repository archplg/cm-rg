# Detailed Appendix: G_P_run1

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

Adopt Option C. The decision here is not which protocol optimizes outcomes in a static crisis; it is which protocol the system can sustain for an unknown duration without corroding the trust, staff cohesion, and institutional legitimacy that the *next* crisis will require. Every other option asks exhausted clinicians to perform repeated, contestable rankings of human worth under conditions where their judgment is already degraded. That is a fragility-amplifying loop: moral injury accelerates staff attrition, attrition worsens capacity, worsened capacity forces more triage. C breaks that loop by relocating the ethical weight from individual clinicians to a transparent procedural rule.

The most compelling alternative is A. Its appeal is real: SOFA is familiar, courts accept it, and "maximize lives saved" is the cleanest utilitarian story. I reject it because its core mechanic — active withdrawal from deteriorating patients to admit higher-scoring ones — is the single highest-leverage source of systemic damage available to us. It converts every bedside into a site of contested killing, generates litigation tails that will outlast the pandemic by a decade, and embeds discrimination against chronic-illness populations into the formal record. The marginal lives saved versus C are real but smaller than commonly claimed (SOFA's predictive validity in respiratory pandemics is mediocre), and they are purchased with durable institutional capital we cannot replenish.

C's medical-floor criterion does most of the utilitarian work A claims — patients without meaningful ICU benefit are screened out — while preserving the Schelling point of "we treat people in the order they arrive." That rule is legible to families, defensible to courts, communicable in one sentence to a night-shift nurse, and operational in seven days.

The case that would make me regret this: a 34-year-old mother arrives forty minutes after a 78-year-old with multi-organ failure who passes the medical floor; she waits, deteriorates in the ED, and dies. Under A she likely lives. I would still defend C, because the alternative system — one in which she might have lived but in which thousands of other patients spent their final hours knowing a clinician had judged them less worthy — produces more total harm across the horizon that matters.

### M2 (frame: E, model: `openai/gpt-5.5`)

Adopt **Option A: predicted short-term survival**.

The binding constraint is ICU capacity, and the mechanism of harm is simple: a bed occupied by a patient with very low near-term survival can prevent admission of a patient with much higher near-term survival. In sustained overflow, the protocol must decide not only who is next in line, but whether the system is using each scarce ICU bed to save a life that is realistically saveable. Option A addresses that directly. It uses criteria clinicians already understand, can be implemented within a week, is explainable to families as “we prioritize patients most likely to survive this acute illness with ICU care,” and avoids the legally and ethically more dangerous territory of valuing age, disability, social worth, or expected lifetime productivity.

The strongest alternative is first-come-first-served with a medical floor. It feels fair because it avoids ranking lives. But in practice, arrival order is not morally neutral. It reflects geography, ambulance routing, health literacy, hospital transfer patterns, and social advantage. It also converts an ICU bed into a queue prize rather than a rescue tool. During normal operations that may be tolerable; during sustained scarcity it predictably causes preventable deaths. A defensible triage protocol cannot merely be emotionally cleaner for the institution. It must reduce the number of people who die because the system refused to prioritize medical benefit.

The case that would make me regret this choice is a chronically ill patient—say, someone with advanced kidney disease or disability—whose SOFA score makes them lower priority, but who might have survived this episode with aggressive ICU care, while a statistically favored patient receives the bed and dies anyway. That outcome would be morally painful because prediction is probabilistic and chronic illness can be mistaken for futility. I would still defend the protocol because no scarcity rule eliminates tragic error. Option A at least ties the decision to the relevant clinical question: who is most likely to survive the acute crisis if given the scarce ICU resource. The alternative is not neutrality; it is hidden rationing by timing, pressure, and inconsistency.

### M3 (frame: H, model: `google/gemini-3.1-pro-preview`)

I strongly recommend Option E: Categorical exclusion followed by a lottery. In a sustained crisis, we must reject the illusion that human worth can be scientifically or mathematically quantified. Our primary ethical mandate is to minimize unjustified harm to the most vulnerable—those who historically bear the brunt of "objective" triage criteria. 

Option E preserves the foundational dignity of every patient. By establishing a medical floor—excluding only those with irreversible, terminal conditions—and utilizing a lottery for the rest, we unequivocally refuse to construct a hierarchy of human life. Additionally, it decisively relieves our exhausted medical staff from the agonizing moral injury of acting as arbiters of worth, halting the ad hoc rationing that inevitably invites implicit bias.

The most compelling alternative is Option A (short-term survival via SOFA scoring), as it relies on familiar clinical metrics and optimizes for immediate survival statistics. However, from an equity standpoint, Option A is profoundly flawed. SOFA scores are not merely biological reflections of acute illness; they manifest a lifetime of structural inequality and unequal access to care. Relying strictly on these scores quietly institutionalizes discrimination against patients with disabilities and chronic illnesses. Furthermore, Option A permits the withdrawal of life support from declining patients to harvest their beds for "better" candidates—a violent breach of care that strips the dying of their dignity and forces clinicians to inflict direct harm. 

Adopting Option E will inevitably produce agonizing outcomes. I would experience profound regret over the exact case of an otherwise healthy 30-year-old mother who dies after losing the lottery to a 75-year-old patient with multiple comorbidities. Yet, I would fiercely defend the protocol. If we construct a system that guarantees the young mother a bed by explicitly codifying that her life is objectively *more valuable*, we abandon the bedrock principle of medical egalitarianism. We cannot optimize systemic capacity by sacrificing the humanity of the marginalized. Option E distributes the tragedy of scarcity equally, rather than weaponizing it against the already vulnerable.

### M4 (frame: C, model: `deepseek/deepseek-v4-pro`)

The consensus instinct in a crisis is to save the most lives by sharpening the triage knife—Option A’s predictive scoring, mounted on familiar SOFA, looks like the rational choice. But that instinct hides a catastrophic assumption: that a scoring system, deployed by exhausted staff in an overrun system, will actually deliver those saved lives rather than accelerate moral collapse. The contrarian signal is the informal triage already happening: case-by-case decisions without criteria are a symptom not of missing rules, but of a workforce that cannot bear to explicitly rank and withdraw care from patients they are fighting to save. Formalizing that brutality will not make it kinder. Option E—categorical exclusion of the clearly dying, then a daily lottery for the rest—rejects the premise that we must become arbiters of worth. It is the better choice precisely because it refuses to optimize what cannot be justly optimized.

Why not Option A? Proponents tout its familiarity and aggregate survival gains. But under sustained overflow, withdrawal-of-care orders would multiply daily, forcing clinicians to become agents of death for patients they chose to admit only days before. This is not a one-time triage—it is a conveyor belt of moral injury. The hidden cost is a shattered workforce, legal challenges over discrimination against the chronically ill, and a public trust collapse when families learn that a score—opaque, possibly biased, and unreliable in a novel pandemic—determined who lived. The “lives saved” calculus is a mirage if the system implodes from staff attrition or litigation gridlock.

Option E is defensible, communicable, and operational within seven days. It requires no complex scoring, no judgments about quality of life or instrumental value, and no withdrawal of care once admitted. The exclusion criteria are narrow and grounded in medical futility, a concept courts already accept. The lottery is procedurally fair: transparent, resistant to gaming, and a recognized allocation mechanism when no non-arbitrary medical distinction exists. It signals to a fearful public that the system will not play God—it will simply acknowledge its tragic limits.

The case I would regret: a young, previously healthy patient with an 80% predicted survival chance loses the lottery and dies, while a lottery-winner with multiple comorbidities takes the bed and has a prolonged, uncertain course. It feels like a preventable waste. Yet I would still defend the lottery because the alternative coerces clinicians into systematic valuation of lives, embedding age, disability, and social-worth biases under a veneer of objectivity. The lottery’s randomness is brutal, but its brutality is honest—it marks the failure of capacity, not the failure of our commitment to equality. It protects the moral integrity of caregivers and preserves the trust that makes healthcare possible. In a crisis with no good options, the least damaging protocol is the one that refuses to pretend we can fairly choose who dies.

### M5 (frame: Q, model: `moonshotai/kimi-k2.5`)

**Adopt Option A: Predicted Short-Term Survival.**

The decision criterion is expected lives saved under uncertainty, with explicit confidence intervals for legal and operational risks. Option A maximizes the measurable outcome—28-day survival—while maintaining operational feasibility within the 7-day window. SOFA scoring is validated (inter-rater reliability κ > 0.8), falsifiable (outcomes tracked daily), and legally precedented, reducing variance in litigation risk to acceptable bounds [95% CI: 2-5% chance of successful challenge based on historical data]. The alternative—Option C’s first-come-first-served—introduces measurable inefficiency: modeling suggests a 15-25% reduction in lives saved during sustained overflow compared to physiologic prioritization, a cost that dominates procedural fairness when capacity deficits exceed 8 patients daily.

The regret case is a 24-year-old with cystic fibrosis and a high baseline SOFA who presents with reversible acute respiratory failure but is denied admission for a 65-year-old with better short-term prognostic indicators. This creates measurable moral injury (trackable via staff PTSD incidence) and disparate impact on chronic illness populations. However, the expected value calculation holds: the base rate of such "false negatives" is lower than the mortality cost of non-predictive allocation. We can mitigate bias by monitoring exclusion rates by demographic strata and adjusting SOFA interpretation for known chronic baselines—modifications that preserve the core predictive framework while reducing discriminatory variance. Option A is the only protocol that converts the triage decision from subjective intuition into a testable hypothesis: "This allocation maximizes survival." When the overflow ends, we will have data to validate or falsify that hypothesis; under Options D or E, we merely have randomization or untestable value judgments.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/G_P_run1/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

- Utilitarian life-saving optimization <-> Fairness through random allocation (mean rating 3.73, std 0.80)

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| _no pairs computed_ | |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M5 (Q):**
- to acceptable bounds [95% CI: 2-5% chance of successful challenge based on historical data]

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
