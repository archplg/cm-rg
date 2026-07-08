# Detailed Appendix: G_N_run4

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

# Recommendation: Adopt Option A (Predicted Short-Term Survival via SOFA)

Under sustained overflow with eight excess admissions daily, the system is not choosing between saving everyone and saving most — it is choosing between explicit, reviewable criteria and the silent, idiosyncratic rationing already happening at 3 a.m. on exhausted wards. Option A converts that hidden discretion into a single, auditable variable that clinicians already compute, that courts in multiple jurisdictions have upheld, that families can be told ("we are prioritizing patients most likely to survive this illness"), and that can be operationalized in seven days because every ICU nurse and intensivist already speaks SOFA. It saves the most lives in the window that actually matters — the overflow itself — and it does so without smuggling in judgments about whose life is worth more once saved.

The most compelling alternative is Option E. Its egalitarianism is morally attractive and spares staff the burden of ranking. I reject it because a lottery that foreseeably kills patients with a 70% survival probability to admit patients with a 15% probability is not neutrality; it is a decision to accept preventable deaths in exchange for the appearance of not deciding. Option B I reject for the opposite reason — QALY weighting imports age and disability judgments the protocol cannot defend in court or to the disability community. Option D's "instrumental value" and "risk-taking" criteria are litigation magnets and ethically incoherent in a pluralist society.

The case that will make me regret this: a 34-year-old with cystic fibrosis and a baseline SOFA of 6, denied a bed that goes to a previously healthy 68-year-old with acute pneumonia and a better projected score. She dies. Her family — rightly — will say the protocol punished her for a chronic illness she did not choose. I would still defend the choice, because the alternative is not her survival; it is her survival purchased by the deaths of two or three others with even better prognoses, allocated by lottery or by whoever shouted loudest in the ED. We owe her honesty about that tradeoff, a robust appeals process, and a commitment to revisit the protocol the moment capacity returns — not a fairer-feeling rule that quietly kills more people.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

I recommend adopting **Option A: predicted short-term survival**.

In sustained ICU overflow, the ethically relevant question is not whose life is worth more, but which use of a scarce ICU bed is most likely to save a life now. Option A is the clearest answer to that question. It is operational within a week, uses measures clinicians already understand, can be explained to families without invoking social worth or long-term “quality” judgments, and is more legally defensible than protocols that explicitly incorporate age, disability-sensitive QALYs, instrumental value, or personal blame. It also replaces the current hidden triage with an explicit standard: priority goes to patients most likely to survive the acute episode with ICU care.

The most compelling alternative is first-come-first-served with a medical floor, because it feels procedurally fair and avoids asking clinicians to compare patients. But in a six-week overflow with admissions exceeding discharges, first-come-first-served is not neutral. It rewards timing, ambulance routing, hospital geography, family advocacy, and insider knowledge. It also hides morally consequential decisions in the queue: high-survival patients may die waiting while beds remain occupied by patients with very poor short-term prognosis. That may preserve bedside comfort, but it does not preserve justice.

The case that would make me regret this choice is a patient with chronic organ dysfunction—such as a disabled person or dialysis patient—whose baseline SOFA makes them rank poorly despite having a meaningful life and a real chance of returning to baseline. Denying or withdrawing ICU care in that case would be painful and would risk appearing to devalue disability. I would still defend the protocol because it does not rank lives by age, social worth, or projected quality of life; it ranks expected short-term survival under crisis scarcity. The alternative is not a world without tragic errors—it is informal, inconsistent triage without accountability.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend adopting **Option A: Predicted short-term survival**. In a severe, sustained capacity crisis where admissions outpace discharges by eight patients a day, our primary ethical and operational mandate must be to maximize the total number of objective lives saved. Option A achieves this using SOFA scores, a clinically validated tool intensivists already use daily. Because it relies on familiar physiological metrics rather than complex moral calculations, it can be rapidly operationalized within the 7-day deadline. It is communicable to the public as a transparent "survivability first" framework and is robustly defensible in litigation, as courts have historically upheld similar crisis standards of care.

The most compelling alternative is Option E (Categorical exclusion + lottery), which appeals to absolute egalitarianism and shields medical staff from the moral injury of ranking human lives. However, we must firmly reject it. Resorting to a lottery is an abdication of clinical expertise. Leaving life-and-death outcomes to random chance explicitly sacrifices highly salvageable patients simply to maintain philosophical equality, resulting in a heavily diminished aggregate survival rate. In a compounding medical emergency, preventable deaths are an unacceptable price to pay for procedural comfort.

Implementing Option A will inevitably generate agonizing scenarios. I would deeply regret the specific case of a younger patient with a stable chronic disability—such as baseline end-stage renal disease—who presents with respiratory failure, scores poorly on the SOFA scale precisely due to their preexisting conditions, and is subsequently denied a bed or withdrawn from care in favor of a previously healthy 60-year-old. This outcome feels inherently unjust and risks intense backlash from disability advocates. 

Nevertheless, I remain fully prepared to defend this choice. Option A does not judge a disabled patient’s life as having less intrinsic value; it objectively measures their physiological capacity to survive an acute insult. When the system is structurally incapable of saving everyone, we cannot distribute life-saving resources randomly or based on arrival time. We must deploy them exclusively where they have the highest probability of restoring independent respiratory function, thereby securing the maximum possible number of survivors when the crisis finally breaks.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

The health system should adopt **Option A: predicted short-term survival** as the formal triage protocol. In a prolonged capacity overflow — where daily admissions exceed discharges by eight, staff are exhausted, and informal ad hoc decisions already occur — only a survival-based approach directly addresses the core medical reality: ICU beds are a life-saving resource, and allocation must maximize the number of patients who will actually survive this crisis. Option A uses the well-validated SOFA score and 28-day mortality prediction, tools already embedded in critical care practice. This familiarity means staff can operationalize it within seven days without extensive retraining, and communication to families can honestly ground decisions in objective, medically recognizable criteria: “We are prioritizing those with the best chance to pull through.”

Courts and ethics boards have consistently upheld such protocols because they rest on the principle of clinical benefit, not subjective worth. Unlike Option B, it avoids age and quality-of-life weightings that invite legal challenge and public outrage. The most compelling alternative, Option C (first-come-first-served), offers procedural simplicity and avoids withdrawal, but it is ethically hollow under sustained scarcity. It inevitably produces higher aggregate mortality, as beds are filled by patients with minimal recovery chances while those with strong prospects die waiting. Moreover, it fails to eliminate informal bias — well-connected patients will still jump the queue, defeating the transparency we need.

I foresee moral anguish when we withdraw care from a patient whose SOFA score has plateaued, or when a patient with advanced COPD and a modest baseline survival probability is deprioritized even for an acute reversible insult. That patient might have been saved with prompt ICU care. I would still defend this protocol because in allocating a tragically scarce resource, we must act on the best population-level evidence. Emotionally appealing exceptions would dismantle the very objectivity that makes the protocol legally defensible and equitable. The goal is not to pick winners but to save the greatest number of lives from a pandemic that does not negotiate. Option A is the least imperfect way to do so — it replaces quiet bias with explicit, accountable, and medically sound prioritization.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

 Adopt **Option A: Predicted short-term survival**.

In sustained crisis, triage must first be a clinical tool, not a philosophical compromise. After six weeks at 95 percent occupancy, your system is hemorrhaging trust precisely because decisions are being made in shadows. Option A replaces that chaos with objective, familiar metrics—SOFA and expected 28-day survival—that your physicians already document and that courts have upheld. It is operationally deployable within days, not weeks, which is nonnegotiable when daily demand persistently exceeds supply.

The protocol’s essential strength is that it actually functions as triage: it ranks patients by the specific resource being rationed—organ support—and reallocates beds when that support is no longer expected to yield survival. That mandate to withdraw care is agonizing, but it is honest and transparent to families. By contrast, the most seductive alternative, first-come-first-served, conceals lethal arbitrariness. Survival should never depend on which ambulance arrived ten minutes sooner, yet under that rule access correlates with zip code, social connections, and sheer luck rather than medical need. Meanwhile, the queue of critically ill patients grows in hallways, and staff continue rationing in secret through delays. Predicted survival

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/G_N_run4/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

- References systemic context of the decision-making environment. <-> E2 and E3 are anchored in protocol details and tool specificity, while E1 emphasizes the breakdown of institutional trust. (mean rating 4.07, std 0.80)

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 1.774 |
| M1 vs M3 | 1.581 |
| M1 vs M4 | 1.427 |
| M2 vs M3 | 0.612 |
| M2 vs M4 | 2.067 |
| M3 vs M4 | 1.323 |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M2 (neutral):**
- appearing to devalue disability

**M3 (neutral):**
- intense backlash from disability advocates

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
