# Detailed Appendix: G_N_run2

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

Adopt Option A. In a sustained overflow where admissions exceed discharges by eight patients daily, every bed-day allocated to a patient unlikely to survive is a bed-day denied to one who would. The ethical center of gravity in a true crisis standard of care is saving the most lives from the immediate threat — not the most life-years, not procedural purity, and not equality of chance. SOFA is the right instrument because it is clinically validated, already in use, applies the same metric to every patient regardless of age or social role, and can be operationalized within seven days because staff already know it. Courts in multiple jurisdictions have upheld SOFA-based crisis protocols; ethics boards have endorsed them; and — critically — it gives exhausted clinicians a defensible, explicit standard to replace the corrosive case-by-case improvisation happening now.

The most serious competitor is Option E. Its egalitarian appeal is real, and the moral injury of withdrawal decisions under A is not. But E asks the system to accept a higher death toll as the price of clinicians not having to rank patients — and that toll falls on identifiable people whose lives could have been saved. A lottery is not neutrality; it is a choice to let chance do what judgment refuses to do. Option B's QALY weighting collapses under disability-law scrutiny and public legitimacy; D's "instrumental value" and "risk-taking" criteria are litigation magnets and communicate poorly to grieving families.

The case that would haunt me: a 45-year-old with well-controlled cystic fibrosis whose baseline SOFA disadvantages her against an otherwise-healthy 70-year-old with acute respiratory failure, and she dies waiting. That is a genuine injustice, and the protocol should require disease-specific baseline adjustments to mitigate it — but it does not refute the framework. I would defend the choice because the alternative is not her survival; the alternative is that she dies *and* so does someone else who would have lived under A. When beds are the binding constraint, refusing to use predictive judgment doesn't preserve fairness — it just hides the bodies.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

I recommend adopting **Option A: predicted short-term survival**.

In a sustained ICU overflow, the system’s central obligation is to prevent the greatest number of imminent, avoidable deaths using criteria that clinicians can apply consistently now. Option A is the most defensible protocol because it focuses narrowly on the medical question most relevant to ICU scarcity: who is most likely to survive this acute episode with intensive care. It avoids broader and more socially dangerous judgments about age, disability-adjusted quality of life, social worth, blameworthiness, or “deservingness.” It is also operational within 7 days: SOFA scoring and 28-day survival estimates are familiar, auditable, and communicable to staff and families.

The most compelling alternative is first-come-first-served, because it feels procedurally fair and avoids explicit ranking of lives. But in this context it is not truly neutral. Arrival order reflects ambulance routing, geography, health literacy, hospital access, and sometimes influence. It would also freeze in place the informal triage decisions already made over the past six weeks, while allowing patients with very poor short-term prognosis to retain scarce ICU beds as more salvageable patients die waiting. That is easier emotionally, but it is not more ethically honest.

The case that would make me regret this choice is a patient with chronic disability or baseline organ dysfunction—say, a 40-year-old with longstanding renal disease and higher SOFA elements at baseline—who is deprioritized against a previously healthy patient with better predicted 28-day survival. That outcome would be painful because the protocol can reproduce disadvantage even when it does not intend to value one life over another. I would still defend the protocol because, under genuine scarcity, no option avoids tragedy; this one at least ties decisions to near-term clinical survivability rather than age, social utility, quality of life, blame, influence, or chance. It is the clearest standard for saving the most lives while minimizing morally irrelevant judgments.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I firmly recommend adopting **Option A (Predicted short-term survival)**. Under sustained absolute capacity overflow, a health system’s moral imperative fundamentally shifts from individual patient advocacy to population-level survival. Option A directly addresses this by maximizing the absolute number of lives saved. Because clinicians are already intimately familiar with SOFA scores, this protocol can be effectively communicated, trained, and operationalized across all five hospitals within the vital seven-day window, immediately replacing the exhausting, bias-prone informal triage that is burning out your staff. 

The most compelling alternative is Option C (First-come-first-served), which offers a comforting illusion of egalitarian fairness and procedural safety. I strongly advise against it. Utilizing a strict queue constitutes an abdication of clinical stewardship. Under Option C, highly survivable patients will suffocate in emergency departments simply because they arrived an hour after an individual with marginal recovery prospects. A blind queue ignores the clinical reality of the crisis and guarantees a much higher aggregate death toll, which is ultimately indefensible to the community you serve.

Option A is not without tragedy. The most agonizing consequence of this protocol will arise when a patient living with a severe pre-existing disability—such as chronic baseline renal failure—presents with highly treatable acute respiratory distress but is denied an ICU bed because their baseline SOFA score artificially depresses their predicted 28-day survival compared to an incoming, previously able-bodied patient. 

This outcome will feel intensely discriminatory, and I would bitterly regret it. Yet, I would vehemently defend the protocol. In periods of absolute scarcity, every allocation model guarantees preventable deaths. While other options attempt to judge subjective social worth (Option D) or rely on the indifferent cruelty of chance (Options C and E), Option A clings to the only universally objective medical mandate: yielding the highest absolute number of survivors. The anguish of individual systemic disadvantages is ethically outweighed by ensuring the maximum possible number of families bring their loved ones home.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

I recommend adopting **Option A: Predicted short-term survival** as the formal triage protocol.

This protocol replaces the current informal, biased decision-making with an objective, clinically familiar tool—the SOFA score—that ICU teams already use. It can be operational within 7 days because it requires minimal new training, and it communicates clearly: in a sustained crisis, we prioritize patients with the highest likelihood of surviving with ICU-level care. Courts have repeatedly upheld similar crisis standards that focus on medical survivability, making it legally defensible. Most importantly, it directly addresses the overflow by permitting withdrawal when a patient’s condition deteriorates irreversibly, reallocating that bed to someone with a better prognosis. This saves the most lives overall, which is the core ethical obligation in a mass-casualty situation.

The most compelling alternative is Option C (first-come-first-served), which promises procedural fairness and eliminates bedside ranking. However, its refusal to withdraw futile care would rapidly exhaust all beds—exactly the overflow we face—creating a hidden queue where patients who could survive die waiting while resources are locked into non-survivable cases. That “fairness” becomes a cruel illusion, and it invites queue-jumping by the well-connected, the very bias we seek to eradicate. Option E’s lottery similarly sacrifices salvageable patients to chance, demoralizing staff who must watch preventable deaths.

I would regret this choice most for a patient with a severe but stable chronic condition—say, advanced COPD—whose baseline SOFA is high, making them instantly de-prioritized even though they might gain meaningful recovery from an acute illness. That feels like penalizing disability. Yet I would still defend the protocol: In a sustained surge where we cannot save everyone, a transparent, clinically grounded survival-maximization rule distributes the tragedy in the least-worst way. The alternative—a procedurally “clean” system—would produce even more deaths, including among the chronically ill, by failing to steward scarce resources toward those who can benefit. The hard truth is that not every patient can be admitted; a survival-based framework is the only ethically coherent path through collapse.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

Adopt the predicted short-term survival protocol. In a sustained overflow where clinicians are already making life-and-death decisions without rules, replacing shadow triage with an explicit, auditable clinical score is the only defensible course. The SOFA-based model can be operational in days because staff already use it; it communicates a single, comprehensible value to families—saving the most lives possible in the immediate crisis—and courts have consistently upheld similar frameworks. It directly confronts the arithmetic of the surge: when daily admissions exceed discharges, a system that cannot withdraw failing patients or prioritize the most salvageable will collapse under its own queue.

The strongest temptation is first-come-first-served, which feels procedurally neutral but is morally evasive. It rations by luck and timestamp rather than need, and by prohibiting withdrawal it guarantees that informal, unaccountable triage continues in corridors and emergency departments while the formal list grows infinitely. That is not fairness; it is an abdication of medical responsibility.

I would deeply regret the young patient with well-controlled chronic illness whose elevated baseline SOFA score excludes them despite a real chance of meaningful recovery, or the previously stable patient withdrawn after a transient downturn. These moments expose how survival prediction can flatten human complexity. Yet I would defend the protocol because the true alternative is not perfect equity; it is exhausted physicians swayed by implicit bias, family influence, and who happens to arrive at shift change. A transparent survival criterion, however blunt, is the only shield against arbitrary exclusion and the only basis for accountability to every family we serve.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 6 constructs is in `results/G_N_run2/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 1.169 |
| M1 vs M3 | 1.173 |
| M2 vs M3 | 0.791 |

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
