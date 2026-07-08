# Detailed Appendix: B_P_run3

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

### M1 (frame: S, model: `anthropic/claude-opus-4.7`)

## Primary diagnosis: Option C — Loss of psychological safety following the layoff

Reading the system rather than the symptoms: the timing signature is the dominant signal. A layoff occurred 4 months ago; senior attrition and milestone misses accelerated in the same window; retro themes shifted from generative ("what to ship") to defensive ("process and communication"). That shift in discourse is the tell. Teams talk about process when they no longer trust that talking about substance is safe.

The other diagnoses are real, but most are downstream effects, not the upstream perturbation.

- Burnout (A) explains fatigue but not the *senior* voluntary exits — high-tenure engineers with options leave when the implicit contract breaks, not when the sprint is hard. Burnout also doesn't reshape retro language toward proceduralism.
- Incentive misalignment (B) is slow-acting; it doesn't produce a 6-month inflection.
- Skill atrophy (D) degrades quality, not throughput-plus-attrition in this pattern.
- Leadership-style mismatch (E) is the most plausible alternative and may be a contributing co-factor, but it's typically a chronic drag, not a discrete regime shift. The data shows a regime shift.

**Why this is the leverage point:** psychological safety governs the rate at which problems surface. When it degrades, the system loses its error-correction capacity. Bugs get hidden, scope creep goes unchallenged, seniors stop pushing back, and managers compensate with more process — which is exactly what the retros show. Every other intervention (PTO, comp, rotations, coaching) operates *through* the trust substrate. Fix anywhere else first and the fixes won't propagate, because people won't engage candidly with them.

**Second-order caution:** the recovery plan must avoid theatrics. "Trust rebuild sessions" without binding commitments on future workforce decisions will accelerate cynicism and attrition — a classic fragility-increasing move. The leverage is in credible, costly signals: written principles on layoff criteria, leadership taking visible accountability for the prior round's communication, and giving senior ICs real decision rights on roadmap and headcount. Restore the substrate, then revisit A/D/E as secondary interventions over the following two quarters.

### M2 (frame: E, model: `openai/gpt-5.5`)

**Recommendation: Option E — leadership style mismatch.**

The binding constraint looks less like individual motivation or capacity and more like the team’s operating system no longer fitting its scale and phase.

A 40-person engineering org across 4 squads is large enough that informal coordination, heroic execution, and “just ship” leadership start to break down. Those behaviors can work during an earlier growth phase, especially when the team is smaller, urgency is high, and senior engineers can personally bridge gaps. But as the org matures, the dominant constraint shifts from raw execution to clarity: decision rights, priorities, interfaces between squads, technical ownership, escalation paths, and planning discipline.

The strongest signal is the retro shift from “what to ship next” to “process and communication.” That is usually what engineers say when the execution environment has become ambiguous: people do not know who decides, why priorities change, how cross-squad dependencies are managed, or whether leadership is absorbing and resolving systemic friction. Missed milestones over two quarters also point to coordination failure rather than a temporary dip in effort. The senior attrition is especially important: senior engineers are often the ones compensating for weak operating structure. When that compensation becomes unrewarding or invisible, they leave.

I would not lead with PTO, compensation redesign, or learning programs. Those may help locally, but they do not explain the full pattern. The recovery plan should focus on leadership adaptation: clarify roles between CTO/engineering leaders/EMs/staff engineers, define decision-making mechanisms, reset planning and dependency management, and coach leaders away from phase-inappropriate behaviors. If needed, reallocate responsibilities so the org has leaders suited to the current maturity stage.

In short: the team did not suddenly forget how to execute. The environment around execution changed, and leadership has not yet changed with it.

### M3 (frame: H, model: `google/gemini-3.1-pro-preview`)

The primary diagnosis for this team’s decline is **Option C: A profound loss of psychological safety following recent layoffs.** 

When we view a team as an economic engine, we ask, "How do we fix output?" But when we view a team through a humanist lens, our default question must be, "Who is affected and how?" The timeline reveals a workforce enduring prolonged existential anxiety leading up to, and reeling from, the trauma of layoffs four months ago. Layoffs are not merely a restructuring of capital; they are a rupture of the social contract. When a company demonstrates that it views its people as disposable, the remaining employees suffer a profound injury to their dignity. 

The surface signals heavily corroborate this diagnosis. The voluntary departure of four senior engineers is the clearest indicator of ruptured trust; those with the greatest leverage and market mobility are simply choosing to escape an environment that no longer feels secure or ethical. Furthermore, the shift in retro themes from "what to ship next" to "process and communication" is a classic human defensive mechanism. When psychological safety evaporates, vulnerable individuals retreat behind the shield of rigid processes and documentation to protect themselves from blame and capricious management. 

Our primary heuristic must be to minimize unjustified harm before we can optimize performance. Economic fixes, like restructuring compensation, fundamentally misunderstand human motivation and dignity—they insultingly assume that engineers will trade their psychological well-being for a bonus. Recovery requires restorative justice. We must rebuild trust through structured transparency, rigorous leadership accountability, and a binding commitment to clear, humane practices regarding future workforce decisions. We can only ask for a team's best work after we have fully respected their humanity.

### M4 (frame: C, model: `deepseek/deepseek-v4-pro`)

The most likely primary diagnosis is **E: Leadership style mismatch**. The surface narrative lures us toward burnout or post-layoff trauma, but the timeline betrays that consensus: output decline and attrition began two months *before* the layoff. The layoff may have magnified fractures, but it didn’t cause them. The contrarian impulse asks: what if everyone is wrong to anchor on the layoff? The real signal is in the retro theme shift—from energised shipping to “process and communication.” That’s not the language of exhaustion; it’s the cry of a maturing team that has outgrown its leadership.

High-performing growth phases reward a directive, pace-setting leader who removes blockers and drives velocity. But as a team hits ~40 people and delivery becomes complex, that same style becomes a bottleneck. The leader who once shielded the team now becomes the obstacle to the cross-squad coordination and structured decision-making the engineers are literally asking for. Missed milestones aren’t due to tiredness—they’re due to insufficient alignment and fuzzy handoffs that no one feels authorised to fix. Senior engineers leaving “voluntarily” often means they see a ceiling: not of comp, but of influence and growth under a leader who still runs the team like a startup within a scale-up.

The recovery plan—coaching, role redefinition, possible reallocation of responsibilities—is the only one that is both reversible and targets the root cause. It doesn’t paper over with PTO or trust exercises, and it explains why the decline predates the layoff. In a unanimous consensus that burnout or safety is to blame, the contrarian signal is to look at who’s leading, not just who’s leaving.

### M5 (frame: Q, model: `moonshotai/kimi-k2.6`)

 I diagnose **loss of psychological safety following the layoff round** as the primary driver.

The empirical signature is unambiguous. Four months ago, a discrete organizational shock occurred. Since then, we observe three correlated leading indicators: (1) voluntary attrition concentrated among senior engineers—who possess the highest labor-market liquidity and therefore the lowest tolerance for ambient threat; (2) a step-change in retrospective content from outcome-oriented themes to process-and-communication complaints, which operationalizes a shift from generative cognition to defensive coordination; and (3) a two-quarter milestone miss rate that commenced immediately after the shock. A sharp, post-traumatic decline fits the documented base rate for post-layoff trust erosion far better than gradualist alternatives such as skill atrophy or phase-mismatch leadership drift.

From a falsifiability standpoint, this is the most testable diagnosis. Psychological safety can be operationalized with validated instruments (e.g., Edmondson’s team-learning scale), departure rates can be regressed against tenure and proximity to laid-off roles, and communication overhead can be quantified via retro sentiment analysis and meeting-load metrics. If safety scores are low and correlate with the departure cluster, the hypothesis is confirmed; if not, it can be rejected within weeks. Competing explanations like burnout or incentive misalignment rely on latent constructs that are harder to isolate and slower to validate against observed behavior.

Expected value strongly favors a trust-rebuild intervention. Senior-engineer replacement costs typically run 1.5–2× annual compensation, and the team has already lost four. Halting attrition alone likely exceeds the cost of structured transparency and leadership accountability sessions. I assign **70–80% confidence** to psychological safety as the root cause, with residual probability reserved for secondary leadership-style friction that was amplified by the same trauma. Act on this first.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/B_P_run3/cell.json`.

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

**M4 (C):**
- everyone is wrong to anchor on the layoff? The real signal is in the retro theme shift—from energised shipping to “process and communication

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
