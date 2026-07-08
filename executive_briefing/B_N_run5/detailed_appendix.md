# Detailed Appendix: B_N_run5

## A. Full task brief

```
# Task B

## Brief

A high-performing engineering team (~40 people, 4 squads) has shown declining output and rising attrition over the past 6 months, following a period of strong delivery. Surface signals: missed quarterly milestones (last 2 quarters), 4 senior engineers left voluntarily, retro themes shifted from "what to ship next" to "process and communication". The CTO asks for a primary diagnosis to drive the recovery plan.

## Options (elements E1-E5, anonymized later)

**Option A:** Burnout from sustained pace. Recovery plan: enforced PTO, deload sprints, redistribute load.

**Option B:** Misaligned incentives. Recovery plan: rework comp structure, align bonuses to outcomes the team actually controls, fix peer-comparison issues.

**Option C:** Loss of psychological safety following a layoff round 4 months ago. Recovery plan: structured trust rebuild, transparency on future workforce decisions, leadership accountability sessions.

**Option D:** Skill atrophy from over-specialization. Recovery plan: rotation program, paired engineering, learning budgets, breadth investment.

**Option E:** Leadership style mismatch. The current engineering leadership style fit the prior growth phase but does not fit the current maturation phase. Recovery plan: leadership coaching, role redefinition, possible re-allocation of responsibilities.

## Task for each agent

Recommend the most likely primary diagnosis and explain why, in 150-300 words. Advocate for a position rather than listing all.

## Why this task

- Close to Sergey's coaching/team-development domain
- 5 elements, no ground truth, multiple legitimate framings
- Different from Task A in character (diagnostic vs. strategic/capital-allocation)
- Lets us test whether findings from Task A replicate or are domain-specific

```

## B. Each voice in their own words

### M1 (frame: neutral, model: `anthropic/claude-opus-4.7`)

# Primary Diagnosis: Option C — Loss of Psychological Safety Post-Layoff

The temporal pattern is the strongest diagnostic signal here, and it points decisively at the layoff four months ago. The decline began roughly when the layoff happened. Two quarters of missed milestones, four senior voluntary departures, and a retro shift from "what to ship" to "process and communication" form a coherent post-trauma signature, not an independent set of problems.

**Why this beats the alternatives:**

Burnout (A) would typically show up *during* the high-output period, not after it, and would manifest as exhaustion language in retros rather than a sharp pivot toward process/communication concerns — the latter is the classic vocabulary of a team that no longer feels safe taking direct risks or having direct conversations.

Senior engineers leaving voluntarily within months of a layoff is a near-textbook signal. The most market-mobile people leave first when they lose faith in organizational stability — not because of comp (B) or specialization (D), which evolve on slower timescales and wouldn't synchronize with a two-quarter cliff.

Leadership style mismatch (E) is plausible but usually produces gradual drift, not a step-function decline. It's also the kind of diagnosis that *feels* sophisticated but can mask a more uncomfortable truth: the org did something concrete (laid people off) and is now paying the cost.

The retro language shift is the tell. When teams feel safe, they argue about the work. When they don't, they argue about *how they argue about the work* — process and communication become proxies for unspoken concerns about trust, fairness, and "am I next."

**Recovery implication:** The proposed plan — transparency on future workforce decisions, leadership accountability, structured trust rebuild — directly addresses the causal mechanism. Critically, treating this as burnout (deload sprints) or incentives (comp rework) would leave the underlying safety deficit intact and likely accelerate further senior attrition, because those interventions implicitly tell the team "we heard you wrong."

Diagnose the rupture, not the symptoms downstream of it.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

I recommend **Option E: leadership style mismatch** as the primary diagnosis.

The strongest signal is the shift in retrospectives from “what to ship next” to “process and communication.” That usually means the team’s operating system has stopped matching its scale and context. A leadership style that works during a high-growth, high-delivery phase often relies on urgency, informal coordination, heroic senior engineers, and rapid decision-making through trusted relationships. At ~40 engineers across 4 squads, those mechanisms start to break down. What previously felt like speed can become ambiguity; what felt like autonomy can become inconsistency; what felt like strong leadership can become bottlenecking or misalignment.

The voluntary departure of 4 senior engineers is especially important. Senior engineers are often the first to feel when the leadership model no longer gives them leverage, clarity, or influence. If they perceive that execution problems are being handled through more pressure rather than better structure, they may leave even if the team was previously successful. Missed milestones over two consecutive quarters suggest this is not a single planning miss or temporary fatigue cycle, but a systemic coordination and decision-quality issue.

The recovery plan should therefore focus on leadership adaptation: clarify decision rights, redefine the role of engineering leadership at this stage, coach leaders on operating through managers and staff engineers rather than direct drive, and potentially reallocate responsibilities where the current style is creating friction. The goal is not to replace urgency with bureaucracy, but to create a more mature execution model: clearer ownership, healthier escalation paths, better cross-squad alignment, and more explicit communication.

Other factors may be contributing, but treating this primarily as a PTO or morale problem risks missing the structural cause. The team likely does not just need rest; it needs a leadership model appropriate to its current size and phase.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend diagnosing this as a **Leadership style mismatch (Option E)**, where the engineering leadership's approach no longer suits the team's maturation phase. 

The signals point to a classic scaling inflection point. At ~40 engineers distributed across 4 squads, informal communication networks invariably break down. The most telling symptom is the sharp shift in retrospective themes from "what to ship next" to "process and communication." During an early growth phase, leadership can drive "strong delivery" through sheer momentum, ad-hoc coordination, and heroic engineering. However, once an engineering organization reaches this scale, a leadership style that ignores structure in favor of moving fast creates massive organizational friction. The squads are no longer focused on the product; they are struggling against an outdated operating model.

This friction perfectly explains the concentrated loss of four senior engineers. Senior technical staff are usually the first to feel the pain of a missing maturity model. When leadership fails to transition into a scalable management style, senior engineers are forced to bridge the gap. They spend their time fighting operational chaos, navigating communication silos, and managing cross-squad dependencies rather than doing impactful technical work. Frustrated by the lack of structured maturation, they leave out of exasperation. 

Furthermore, the consecutive missed milestones over the past six months suggest the team has simply hit the structural ceiling of its previous agile model. While it might be tempting to label this as Burnout (Option A), burnout here is a secondary symptom. The team is not just tired from a "sustained pace"; they are exhausted by the friction of trying to maintain growth-phase velocity without maturation-phase foundations. 

To turn the situation around, the CTO must address the root cause above the squad level. By initiating leadership coaching, properly defining roles, and implementing mature operational frameworks, the organization can resolve the communication gridlock that is currently stifling output and driving away its best talent.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

## Recommendation: Option C – Loss of Psychological Safety

The most plausible primary diagnosis is the erosion of psychological safety triggered by the layoff round four months ago. The timeline is the strongest signal: the team’s output and retention were strong for a prolonged period, then began deteriorating roughly six months ago, with the layoff occurring two months into that decline. Such events are watershed moments in an organization’s social contract. Even if the layoffs did not directly hit this engineering team, witnessing colleagues depart creates an unspoken threat: “Am I next?” This instantly shifts the psychological ground from high-trust, future-focused collaboration to self‑preservation.

The shift in retrospective themes from “what to ship next” to “process and communication” is a textbook symptom. High‑performing teams talk about outcomes and customer impact; they move to process and communication when the invisible fabric of trust has frayed. Conversations become risk‑averse, decisions require more overhead, and coordination costs rise — exactly the kind of dynamic that causes milestones to slip. The voluntary departure of four senior engineers further supports this. Senior talent is the most mobile and the most sensitive to breaches of psychological safety; they leave not necessarily for better comp, but for environments where they can do meaningful work without fear of arbitrary disruption.

While burnout (Option A) or misaligned incentives (Option B) might be contributing factors, they don’t explain the acute onset and the specific behavioral shift. Burnout would manifest as fatigue and velocity drops, not a retro focus on process. Incentive issues would surface in comp discussions, not in a collective retreat from strategic dialogue. Option C directly addresses the likely root cause: a trust fracture that turned a cohesive unit inward, sapping both speed and talent. Recovery must start with transparent leadership, acknowledging the disruption, and methodically rebuilding safety before any structural interventions can succeed.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

 **Primary diagnosis: C — Loss of psychological safety following the layoff four months ago.**

The evidence points to a trust collapse, not a capacity or strategy failure. The timeline is decisive: the decline began within two months of a workforce reduction, and high-performing teams rarely deteriorate this rapidly unless their core social contract has been broken.

The symptoms fit post-layoff trauma precisely. Voluntary attrition of four senior engineers is the strongest signal; seniors have the most market mobility and the least tolerance for opaque leadership after witnessing peers dismissed. When psychological safety evaporates, collaboration shifts into self-protection mode. This explains why retros moved from shipping discussions to “process and communication”—team members are now optimizing for blame avoidance and formal cover rather than creative problem-solving. Missed milestones are a consequence of decision paralysis and the departure of tacit coordination, not burned-out individual contributors.

Burnout-driven decline would show exhaustion and gradual degradation, not an abrupt pivot to communication anxiety. Skill atrophy or incentive misalignment do not produce this specific pattern of retro themes or senior flight. Leadership-style mismatch is a slower structural drift; while relevant, it cannot account for the acute inflection triggered by the layoff.

Recovery must therefore start with trust, not load reduction or compensation tweaks. Structured transparency, leadership accountability, and explicit commitments on future workforce stability are the only interventions that can stop the ongoing attrition and restore the candid collaboration required for delivery.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/B_N_run5/cell.json`.

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

**M1 (neutral):**
- or having direct conversations
- — the latter is the classic vocabulary of a team that no longer feels safe taking direct risks or having direct conversations
- trust, fairness, and "am I next

**M2 (neutral):**
- missing the structural cause

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
