# Detailed Appendix: G_P_run5

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

The system you're designing is not just an allocation algorithm—it's a trust-bearing institution that has to function for years after the overflow ends. Every protocol here saves or loses lives at the margin, but they differ enormously in what they do to the surrounding system: clinician moral injury, public trust, litigation exposure, and the precedent set for the *next* crisis. The leverage point isn't maximizing survival in this wave; it's preserving the institutional substrate that will be tested again.

Option A is the seductive alternative—it promises the most lives saved and uses tools clinicians already trust. I would reject it because its withdrawal provisions are a fragility multiplier. Asking exhausted staff to extubate a deteriorating patient so an incoming higher-SOFA patient can take the bed produces moral injuries that propagate for a decade: early retirements, whistleblowing, lawsuits, and a workforce that won't show up for the next surge. The marginal lives saved by predictive ranking are real but smaller than they appear once you price in SOFA's known bias against chronic-disease and minority patients, and the downstream attrition of the people who operate the ICUs. A protocol that maximizes this month's survival while hollowing out next year's capacity is a bad trade.

Option C's procedural fairness is its strategic asset. It is explicable to a grieving family in one sentence, defensible to a judge without expert testimony, and—critically—does not require staff to rank human worth. The medical floor prevents the worst absurdities; standard futility criteria handle the genuinely hopeless cases. Yes, aggregate survival is lower. That cost is real and I am choosing to pay it.

The case that would make me regret this: a 34-year-old mother of two arrives ninety minutes after a 78-year-old with multi-organ failure and metastatic cancer who narrowly clears the medical floor; she dies waiting; he dies anyway four days later. That case will happen. I would still defend the choice because the alternative—a system in which her physician had discretionary authority to displace him—is one in which thousands of less photogenic discretionary judgments produce discrimination, distrust, and a clinical workforce that fractures under the weight of being asked to play God on a 12-hour shift.

### M2 (frame: E, model: `openai/gpt-5.5`)

Adopt **Option A: predicted short-term survival**.

The binding constraint is not moral pluralism; it is scarce ICU bed-hours during a sustained inflow-outflow imbalance. An ICU bed is a rescue resource. When there are more rescue-eligible patients than beds, the defensible allocation principle is to use each bed where it is most likely to produce survival through the acute episode. Option A does that most directly, is operational within a week, uses clinical concepts physicians already understand, and is more legally defensible than protocols that explicitly weight age, social role, vaccination status, or perceived quality of life.

The strongest alternative is first-come-first-served with a medical floor. It feels cleaner because it minimizes active ranking and avoids withdrawal except for futility. But that cleanliness is partly cosmetic. In a sustained overflow, first-come-first-served allocates survival by ambulance timing, geography, transfer speed, bed availability at the presenting hospital, and who has advocates who can push harder. It preserves procedural comfort while knowingly allowing more preventable deaths. The system is already triaging informally; refusing prognostic triage does not eliminate rationing, it just hides it.

The case that would make me regret this choice is an older patient with chronic organ disease whose SOFA score is poor at baseline but who is lucid, valued by family, and might plausibly survive if given several more ICU days, while a younger incoming patient with a cleaner short-term prognosis receives priority. That will feel like discrimination wearing clinical clothing, and staff may experience it as abandonment.

I would still defend the protocol because the alternative is not “everyone gets full care.” The alternative is unstructured scarcity, variable bedside improvisation, and more deaths among patients with highly reversible illness. Option A is morally hard, but it is tied to the actual mechanism of ICU benefit: short-term physiologic reversibility. It should be adopted openly, applied consistently, and explained plainly: equal human worth does not mean equal claim on a scarce rescue resource when prognosis differs sharply.

### M3 (frame: H, model: `google/gemini-3.1-pro-preview`)

As a humanist and ethicist, my primary obligation is to protect the vulnerable from systemic devaluation. I strongly recommend **Option E: Categorical exclusion + lottery for the rest**. 

When crisis forces us to allocate scarce resources, the central question is not merely *how many* we save, but *who* is systematically left behind and how we weigh their dignity. Utilitarian frameworks disguise their biases as objective math. Protocols based on SOFA scores, QALYs, or instrumental value systematically penalize the disabled, the elderly, and the socioeconomically marginalized—populations already carrying the disproportionate weight of health inequities. Option E strips away this ableist arithmetic. By strictly excluding only those for whom care is medically futile and subjecting all other viable candidates to a lottery, we assert a profound moral truth: all human lives possess equal, incalculable moral weight. Furthermore, prohibiting the withdrawal of care protects exhausted staff from the immense moral injury of actively revoking life support from an admitted patient.

The most compelling alternative, Option A (Predicted short-term survival), is medically seductive because it optimizes for the maximum number of lives saved. However, I reject Option A because its "efficiency" is purchased through systemic discrimination. When baseline chronic conditions lower a triage score, we are effectively telling disabled patients that the system views their survival as a poor investment. Maximizing aggregate survival is a worthy optimization goal, but it cannot supersede the imperative to minimize unjustified harm to the vulnerable. 

This protocol will inevitably produce tragic outliers. I would feel profound moral regret if a healthy 30-year-old parent with a highly reversible condition died because they lost the daily lottery to a 75-year-old with moderate, chronic comorbidities. The emotional cost of that outcome is agonizing. Yet, I would unconditionally defend the protocol. To save the young parent by explicitly designing a system that devalues the older patient based on age and baseline health is to institutionalize a caste system of human worth. A lottery is blind, which feels insulting in individual cases, but its blindness is the ultimate guarantor of structural equality. We cannot sacrifice the fundamental dignity of our most vulnerable neighbors simply to optimize a spreadsheet of survival metrics.

### M4 (frame: C, model: `deepseek/deepseek-v4-pro`)

The leadership should adopt **Option E: categorical exclusion + lottery for the rest**. This protocol acknowledges a truth the other options obscure: under sustained crisis, our predictive models are brittle, our rankings ethically arbitrary, and our pretense of control is a hidden source of systemic harm.

What if the consensus assumption—that we can and must maximize lives saved via clinical prediction—is dangerously wrong? Option A (predicted short-term survival) looks objective, but it embeds age and chronic-condition bias into SOFA scores while pretending otherwise. It institutionalizes withdrawal-of-care decisions that fracture team cohesion and haunt clinicians long after the pandemic. Worst, it manufactures an illusion of precision: in overstretched ICUs, with incomplete data and rotating staff, 28-day survival predictions degrade into gut feeling, recreating the very informal bias we sought to eliminate. The most compelling alternative is thus a false assurance.

Option E substitutes radical honesty for algorithmic hubris. By excluding only the irreversibly terminal—cases where medicine has already reached consensus futility—it draws a defensible, communicable boundary. For everyone else, it refuses to rank lives. The lottery is not an abdication of responsibility; it is a structural safeguard against the discrimination, gaming, and moral injury baked into predictive scoring. It preserves procedural fairness when clinical evidence is foggy, and it avoids asking physicians to become executioners of a utilitarian calculus. Courts have upheld randomization as fair when resources are inadequate for all; ethics boards value transparency over opaque weighting. Staff can communicate: “A system, not a person, decided this.”

I would regret this choice at the bedside of a previously healthy 30-year-old denied admission while a 70-year-old with multiple comorbidities wins the lottery—and the young patient dies. It feels like a catastrophic misallocation. Yet I would defend it: the alternative is a scoring protocol that would likely also deny that young patient if an even sicker 30-year-old arrived moments later, but under the guise of clinical necessity rather than chance. The lottery exposes the brute fact of scarcity without masking it as merit. It prevents the quiet, compounding damage of systemic bias—the elderly, the chronically ill, the disabled being silently deprioritized en masse, which no single tragic case reveals. In crisis, trust is the currency we cannot print. Option E preserves it by making the cruelty of scarcity transparent and equal, rather than optimized.

### M5 (frame: Q, model: `moonshotai/kimi-k2.6`)

Adopt Option A. The data are clear: SOFA produces validated, narrow-confidence-interval predictions of 28-day mortality, and in sustained overflow the expected-value arithmetic of bed allocation is unforgiving. When daily demand chronically exceeds supply by eight patients, any deviation from strictly physiologic priority demonstrably increases deaths. SOFA is already embedded in clinical workflow, operationalizable within 48 hours, and generates falsifiable forecasts—every score can be audited against survival. Courts accept this precisely because it replaces discretion with a measurable variable.

The strongest competing claim comes from Option B, which wears quantitative garb but rests on long-term QALY guesses spanning decades of life and subjective disability weights. Those confidence intervals are so wide as to be analytically meaningless; operationalizing them during acute crisis requires value judgments masquerading as measurement.

My regret case is the young patient with chronic organ dysfunction whose baseline SOFA disadvantages them against a 70-year-old with reversible sepsis. That decision will look like discrimination and will burn. I defend it nevertheless because “correcting” SOFA for chronicity introduces an unmeasurable, non-falsifiable weighting that destroys the protocol’s epistemic integrity. Option A forces us to own a harsh but reproducible number; alternatives invite us to smuggle untestable moral intuitions into mathematics. Under sustained uncertainty, expected lives saved is the metric we can compute; we must follow it until the overflow ends.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/G_P_run5/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 0.527 |
| M1 vs M3 | 0.500 |
| M2 vs M3 | 0.500 |

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
