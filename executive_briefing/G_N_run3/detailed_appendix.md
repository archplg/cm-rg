# Detailed Appendix: G_N_run3

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

# Recommendation: Option A (Predicted Short-Term Survival)

Adopt SOFA-based short-term survival as the explicit protocol. Under sustained overflow with eight net admissions per day, every bed-day is a life-or-death allocation, and the protocol that saves the most lives in the actual crisis we face is the one that best honors medicine's core obligation. SOFA is clinically validated, already in our physicians' hands, auditable, and — critically — has been upheld by courts reviewing pandemic triage. It can be operationalized in seven days because staff already compute it. It replaces the worst feature of our current state: idiosyncratic case-by-case judgments where the loudest family or the most senior attending wins.

The most compelling alternative is Option E's categorical-exclusion-plus-lottery. Its egalitarianism is genuinely attractive and it spares staff the moral weight of ranking. But equality of *chance* is not the same as equality of *concern*, and in a six-week sustained overflow, a lottery will predictably kill patients we could have saved — patients whose 28-day survival probability was 85% — to give a bed to someone whose probability was 10%. That is not humility before human equality; it is a refusal to use information we possess. Lotteries are defensible when prognostic differences are small; here they are large and measurable. Option B's QALY weighting collapses into age discrimination courts have rejected. Option D's instrumental and behavioral criteria are ungovernable. Option C accepts preventable deaths as the price of procedural purity.

The case that would haunt me: a 34-year-old mother with well-controlled cystic fibrosis whose baseline SOFA disadvantages her against a 60-year-old with acute single-organ failure and a better predicted trajectory. She loses the bed. Her chronic disease, not her acute illness, decided it. I would still defend the choice — but only by being honest that SOFA is a tool for predicting *this* admission's survival, not a judgment about her life's worth, and by insisting leadership publicly name this harm rather than launder it through clinical language. Pair adoption with a mandatory review committee, daily transparency reporting, and a sunset clause tied to capacity returning below 85%. The protocol must be defended, not hidden behind.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

I recommend adopting **Option A: Predicted short-term survival**.

In sustained ICU overflow, the system’s ethical obligation is to use scarce critical-care capacity to save the most lives that can realistically be saved now. Option A is the clearest, most operationally feasible protocol for doing that within seven days: clinicians understand SOFA and short-term survival estimates, the rule is communicable, and it avoids explicitly ranking patients by age, disability, social worth, or projected quality of life. It is not morally comfortable, but it is the most defensible crisis standard because it ties allocation to the clinical purpose of the ICU: likelihood of surviving the acute episode with intensive care.

The most compelling alternative is first-come-first-served. It feels fair because it avoids ranking lives and reduces visible discretion. But in practice it rewards accidents of timing, geography, ambulance routing, hospital crowding, and social access. It also accepts preventable deaths among patients with strong chances of survival simply because they arrived after lower-benefit patients occupied beds. In a six-week overflow with admissions exceeding discharges, that is not neutrality; it is an unacknowledged rationing system.

The case that would make me regret this choice is a patient with chronic disability or baseline organ dysfunction—say, a middle-aged dialysis patient or someone with advanced neuromuscular disease—whose SOFA score makes them lower priority despite a life they and their family value deeply, while a less chronically ill patient receives the bed. That would feel painfully close to discrimination, and the staff will feel it too. I would still defend the protocol because it does not ask whether that patient’s life is less worthy, less productive, or less valuable. It asks only whether ICU treatment is more likely to produce short-term survival for one patient rather than another under emergency scarcity. That is a tragic standard, but it is a clinically relevant and publicly explainable one.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend adopting **Option A (Predicted short-term survival)**. In a catastrophic overflow where daily admissions outpace discharges by a net of eight patients, the health system is mathematically guaranteed to run out of beds. The primary ethical imperative must therefore shift from individual patient advocacy to maximizing aggregate lives saved. Option A achieves this using SOFA scoring—a standardized, objective tool already familiar to intensivists. This familiarity is crucial: we can operationalize Option A within the 7-day mandate without requiring staff to learn complex new sociological or prognostic composite rubrics. It effectively replaces current ad-hoc, bias-prone decisions with a legally defensible, strictly clinical framework.

The most compelling alternative is **Option C (First-come-first-served)**, because it preserves procedural fairness, avoids subjective bias, and protects staff from the moral injury of actively withdrawing care. However, Option C is a dereliction of clinical triage under absolute scarcity. FCFS does not solve the underlying math of our capacity crisis; it merely displaces it. If we adopt FCFS, the ICU will fill with slowly recovering or chronically declining patients, and we will watch highly salvageable patients die in emergency departments simply because they contracted the virus a week too late. 

The most painful consequence of Option A is that it inherently disadvantages patients with underlying comorbidities. I would deeply regret the case of a 45-year-old patient with chronic kidney disease and baseline organ dysfunction who has care withdrawn in favor of a previously healthy 60-year-old with a moderately better SOFA score. This outcome exacerbates existing structural inequities by penalizing the chronically ill for their baseline health. Yet, I would fiercely defend the decision. During a sustained crisis, introducing qualitative judgments about "fairness," "instrumental value," or "quality of life" (as in Options B and D) invites insurmountable legal risk, public outrage, and subjective bias. Option A relies on a grim but unassailable biological calculus: allocating a fundamentally scarce resource to the patient physiologically most likely to survive the immediate viral insult. When we cannot save everyone, our uncompromising baseline duty is to save the most lives possible.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

In adopting a triage protocol for sustained ICU overflow, we must prioritize a framework that is clinically grounded, maximizes lives saved, and can be implemented with transparency and legal defensibility. Option A—predicted short-term survival based on SOFA score and 28-day survival probability—is the only choice that meets these imperatives.

This protocol directly confronts the reality of scarcity: when not all can be saved, we should save the most. By using validated, objective measures of acute physiology, it removes the arbitrariness of informal, case-by-case decisions and replaces it with a uniform, reproducible process. Physicians are already familiar with SOFA, making it operational within days, and courts have consistently upheld similar prognostic-based frameworks during public health emergencies. Crucially, it avoids the ethical quicksand of Options B and D, which incorporate quality-adjusted life-years or social worth—criteria that invite constitutional challenges, discriminate explicitly against the elderly and disabled, and shatter public trust.

The most compelling alternative is Option C, which appeals to procedural fairness by eliminating withdrawal of care and using a first-come, first-served queue. Yet this approach sacrifices aggregate survival, as too-ill patients who occupy beds for weeks prevent access for those with better odds. More insidiously, it invites queue jumping by the well-connected, recreating the very bias we seek to eliminate. In a sustained crisis with eight excess admissions daily, a no-withdrawal queue becomes a slow triage mechanism that condemns salvageable patients to die waiting—hardly more ethical than explicit prioritization.

I acknowledge the deep regret this protocol will cause. Consider a 50-year-old with moderate COPD who presents with severe pneumonia. Her baseline SOFA is elevated from chronic disease, reducing her priority score even though she might have years of meaningful life ahead. She might be passed over for a previously healthy 70-year-old. In that moment, the protocol will feel mechanistic and unjust. But I would defend it by emphasizing that we are not judging her worth—only her immediate physiological reserve and probability of surviving the ICU stay. The alternative is a covert rationing that cloaks bias in clinical discretion, or a lottery that abandons the duty to direct resources where they can do the most good. Option A is the least imperfect balance: it saves the most lives now, is defensible in court, and provides a clear, teachable rule that protects both clinicians and families from the moral chaos of ad hoc triage.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

 I recommend adopting Option C, first-come-first-served with medical floor. After six weeks at ninety-five percent capacity, your staff are exhausted and informal triage is already corroding trust within the community and the workforce. The imperative is not to perfect an actuarial calculus but to replace hidden bias with a rule that can be explained in a sentence and defended in a courtroom. Option C meets that need. By establishing a transparent minimum-threshold criterion and allocating beds by arrival time, it removes exhausted clinicians from the impossible role of ranking human worth. It is operational tomorrow, legible to frightened families, and defensible to courts because it minimizes discretion and avoids the discrimination inherent in survival scoring.

The most compelling alternative, Option A, offers the seductive promise of maximizing short-term lives saved through SOFA-based priority. But that gain is purchased at a price this system cannot pay: it penalizes patients with chronic conditions, and—more dangerously—it requires staff to participate in systematic withdrawal of existing patients based on score trends. During sustained surge, forcing caregivers to repeatedly remove patients from life support to make space for the “more salvageable

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 12 constructs is in `results/G_N_run3/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M2 vs M3 | 0.612 |
| M2 vs M4 | 0.655 |
| M3 vs M4 | 1.369 |

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
