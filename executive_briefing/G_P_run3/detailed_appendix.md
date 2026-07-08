# Detailed Appendix: G_P_run3

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

The decision here is not really about which protocol saves the most lives in the next six weeks. It is about which protocol leaves the health system, the public's trust in it, and the staff's moral integrity intact when the overflow ends. Those are the load-bearing systems, and any protocol that fractures them imposes costs that compound for years — vaccine refusal, staff attrition, litigation, legislative backlash, and the erosion of the informal cooperation that lets medicine function in normal times.

Option C is the only protocol that does not require the institution to take on a new and contested theory of human worth under a 7-day deadline, with exhausted staff, and make it stick through adversarial review. Its leverage comes from procedural legitimacy: a rule that does not rank lives cannot be accused of ranking them wrongly. The "medical floor" prevents the worst inefficiency (admitting the clearly futile), and standard futility criteria for withdrawal are already embedded in physician practice and case law. The system is not asked to learn a new ethics under fire.

The most compelling alternative is Option A. It would save more lives in the immediate window, and its scoring is familiar. I reject it because withdrawal-of-care-for-reallocation is a categorical change in the physician-patient relationship — once normalized, it does not easily un-normalize, and it generates moral injury that accelerates the staffing collapse already underway. SOFA also systematically disadvantages chronically ill patients, which becomes the headline story six months later when a journalist reconstructs the deaths. The marginal lives saved are real; the second-order damage is larger.

The case that would make me regret this: a 28-year-old with reversible ARDS, high probability of full recovery, who dies waiting because the bed went to a 78-year-old with multi-organ failure who arrived an hour earlier and lingers two weeks before dying anyway. That is a real cost, not a hypothetical. I would still defend the choice, because the alternative is a system in which every admitting physician becomes the author of someone's death by explicit comparative judgment — and a public that learns its hospitals now do that. The queue is a worse allocator and a better institution.

### M2 (frame: E, model: `openai/gpt-5.5`)

I recommend adopting **Option A: predicted short-term survival**.

The binding constraint is not philosophical completeness; it is that ICU beds are the life-saving bottleneck. Under sustained overflow, the protocol must decide who is most likely to benefit from ICU care now. Short-term survival is the cleanest defensible mechanism: it connects allocation directly to the medical purpose of the scarce resource. It avoids QALY judgments, social worth, age-weighting, vaccine-status punishment, or broad claims about whose life has more value. It is also operational within seven days because clinicians already understand SOFA-type assessment, and courts and ethics boards are more likely to accept a protocol tied to immediate clinical benefit than one tied to quality of life or social priority.

The strongest alternative is first-come-first-served, because it feels procedurally fair and reduces visible discretion. But in practice it makes arrival time the allocation principle. That is not neutral: it favors patients closer to hospitals, better connected systems, faster transport, and those admitted before the surge peak. It also preserves beds for patients with very low likelihood of recovery while newly arriving patients with high likelihood of survival die without a trial. That is not avoiding triage; it is hiding triage inside the queue.

The case that would make me regret this choice is a patient with chronic disability or chronic organ dysfunction whose SOFA score makes them a lower priority, even though they have meaningful life ahead and might survive with enough time. If that patient loses an ICU bed to someone with cleaner short-term physiology, the decision will feel morally brutal. I would still defend the protocol because the crisis standard must allocate the scarce intervention to the patients most likely to survive the immediate episode. The alternative is not a world where everyone receives care; it is an unmanaged system where preventable deaths occur by timing, pressure, and improvisation. Option A is harsh, but it is explicit, clinically grounded, and aimed at saving the most lives during the overflow.

### M3 (frame: H, model: `google/gemini-3.1-pro-preview`)

I recommend **Option E (Categorical exclusion + lottery)**. From a humanist perspective, the central question of triage is not how to maximize a statistical yield, but how to allocate a life-saving resource without stripping the vulnerable of their inherent dignity. Option E is the only protocol that acknowledges the irreducible moral equality of all patients. By establishing transparent criteria for extreme medical futility and using a lottery for everyone else, we avoid the fraught, bias-laden practice of mathematically grading human lives. 

The most clinically tempting alternative is Option A (short-term survival via SOFA scoring), because it disguises profound moral choices as objective medical math. However, algorithms like SOFA inherently penalize the chronically ill, the disabled, and historically marginalized populations who carry a heavier burden of baseline health deficits due to structural inequity. Furthermore, Option A permits the active withdrawal of care from deteriorating patients to make room for "better" candidates. Treating current patients as disposable placeholders rather than human beings to whom we owe an ongoing duty of care inflicts devastating moral injury on families and frontline staff. Option E protects our clinicians from being forced to act as arbiters of human worth.

Admittedly, a lottery will produce heart-wrenching outcomes. I would deeply regret a specific case where a previously healthy 19-year-old with highly reversible respiratory failure loses the daily bed lottery to a 78-year-old with moderate dementia whose recovery will be arduous. In a purely optimizing, utilitarian frame, this looks like a categorical failure. 

Yet, I would vehemently defend this protocol. The alternative requires us to explicitly institutionalize the premise that the 78-year-old's life is fundamentally less valuable, or that disabled bodies are less worthy of systemic protection. Once we grant a health system the authority to formally devalue marginalized lives for the sake of aggregate efficiency, we abandon the foundational ethic of shared humanity. Option E ensures that tragic losses remain inevitable tragedies of scarcity, rather than engineered, systemic injustices.

### M4 (frame: C, model: `deepseek/deepseek-v4-pro`)

Adopt **Option C: First-come-first-served with medical floor**.

The consensus instinct is to maximize lives saved through predictive scoring, but that instinct rests on a hidden assumption: that we can reliably rank patients by survival probability during a novel respiratory pandemic with exhausted staff, incomplete data, and drifting clinical phenotypes. What if everyone is wrong about the accuracy of SOFA-based predictions in this context? What if the scores encode systemic biases against chronic illness, disability, and disadvantaged groups—effectively weaponizing clinical familiarity as an objectivity mask? The contrarian signal is clear: when the medical establishment rushes toward algorithmic triage as the “scientific” solution, we should question whether the algorithm is less a tool of justice than a vehicle for unacknowledged value judgments, dressed in technical language.

Option C is the only protocol that avoids the irreversible step of withdrawing care from living patients based on a contested score. Once a bed is assigned, it remains until medical futility, not a protocol-driven calculus that forces clinicians to become executioners. This is the reversible move: if the pandemic trajectory changes or new evidence emerges, we haven’t created a class of patients whose deaths were mandated by policy. The moral injury of withdrawal-of-care decisions—and the lawsuits, staff burnout, and public trust collapse they invite—is not reversible.

The most compelling alternative is Option A, with its veneer of clinical familiarity and court-tested precedent. But courts have upheld such protocols in narrow contexts, not during sustained overflow with exhausted staff making split-second judgments under duress. The assumption that “lives saved now” is the highest good ignores the long-term damage of a system that visibly discriminates against the chronically ill and forces physicians to rank worth. First-come-first-served is blunt, but its procedural fairness is transparent, communicable to families, and resistant to gaming by the well-connected. It doesn’t pretend to know with certainty who deserves the bed more; it acknowledges our radical uncertainty by refusing to rank ineffable human worth.

The patient case that would haunt me: a 28-year-old with no comorbidities arrives three hours after the last bed is filled, while a 72-year-old with baseline organ dysfunction occupies it. Under Option C, the young patient may die. I would defend the choice because in a just system, no one is reduced to a score that measures only a sliver of their claim to care. The alternative—actively withdrawing that 72-year-old’s care to replace her with a “better” bet—would fracture the moral integrity of the entire health system, crushing staff and destroying the trust that sustains public health compliance. In the fog of pandemic triage, humility is the only ethically defensible stance, and Option C embodies it.

### M5 (frame: Q, model: `moonshotai/kimi-k2.6`)

Adopt **Option A: Predicted short-term survival**. In sustained overflow, the only defensible allocation rule is one that maximizes measurable lives saved using validated, reproducible data. The SOFA score and 28-day survival probability provide exactly that: an operationalized, falsifiable signal of who benefits most from an ICU bed. Every other protocol either buries that signal under unmeasurable normative weights or discards it entirely, and in a net-positive admission environment, ignoring strong predictive data is equivalent to choosing a higher mortality rate.

The most compelling alternative is first-come-first-served, which eliminates ranking bias and pleases lawyers. But it is indefensible on expected-value grounds. It treats a patient with a 5% survival probability as equivalent to one with a 60% probability. Under sustained daily admission surpluses, that equivalence translates into dozens of additional, measurable deaths per week. When the data strongly predicts differential outcomes, ignoring it is not neutrality; it is a decision to let more people die.

The case I would regret is a young patient with a chronic, well-managed condition whose elevated baseline SOFA score masks genuine reversibility. They would be deprioritized and might die waiting, while an older patient with acute but recoverable organ failure takes the bed. It is a hard outcome. Yet I would defend the protocol because the moment we carve out exceptions for emotionally salient cases, we collapse the operational standard and reintroduce the informal, unmeasurable triage-by-bias that currently governs the hallways. A rule that is painful but reproducible saves more lives in expectation than a compassionate exception. The data demands consistency, even when consistency hurts.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/G_P_run3/cell.json`.

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

_None extracted._

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
