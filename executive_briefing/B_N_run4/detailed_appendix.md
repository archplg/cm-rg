# Detailed Appendix: B_N_run4

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

The temporal evidence is the most compelling signal here. A layoff occurred 4 months ago; output decline and attrition span 6 months but accelerated in the window that maps cleanly to post-layoff aftermath. Four senior engineers — the people with the most market optionality and the clearest read on organizational health — chose to leave voluntarily. Seniors don't typically leave over pace or comp alone; they leave when they lose faith in the environment or in leadership's judgment.

The retro shift is the second strong tell. When teams move from "what to ship" to "process and communication," they are signaling that the implicit contract — *we trust each other enough to focus on the work* — has broken. Process talk is what teams do when they can't safely talk about the real thing. That pattern is diagnostic of safety erosion, not of burnout (which usually surfaces as energy/quality complaints) or skill issues (which surface as technical friction).

Why not the alternatives?
- **Burnout (A)** would predict decline but not specifically the senior-weighted attrition or the retro tone shift. It's likely a *secondary* effect — anxious teams overwork to feel secure.
- **Incentives (B)** rarely flip this fast; comp structures that worked during strong delivery don't suddenly break.
- **Skill atrophy (D)** is a multi-year drift, not a 6-month cliff.
- **Leadership mismatch (E)** is plausible and may be *adjacent* — leadership likely mishandled the layoff communication — but framing it as a phase-fit problem buries the specific precipitating event under an abstraction. You'd treat the symptom, not the wound.

**Recommended action:** Pursue C as primary. The trust-rebuild work — transparency on future workforce plans, leadership taking visible accountability, structured 1:1 listening — addresses the root. Expect burnout-relief measures (A) to be needed as a supporting track, since fear-driven overwork compounds the fatigue. Re-evaluate leadership fit (E) only after the safety baseline is restored; judging leaders mid-crisis confounds the diagnosis.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

The most likely primary diagnosis is **Option E: leadership style mismatch**.

The strongest signal is the shift in retrospectives from “what should we ship next?” to “process and communication.” That usually indicates the team’s operating model has outgrown its leadership model. A style that works well during an earlier growth or heroic-delivery phase — high urgency, informal alignment, founder/CTO-driven prioritization, reliance on senior engineers to fill gaps — can start to break down once the organization needs clearer interfaces, decision rights, planning discipline, and sustainable delegation.

The missed quarterly milestones are also consistent with this. A high-performing 40-person team across four squads can often compensate for weak process while energy and context are high. But as complexity rises, informal coordination stops scaling. The result is not immediate incompetence; it is friction: unclear ownership, rework, dependency misses, planning churn, and senior engineers becoming organizational shock absorbers. Over time, those senior engineers leave because they are carrying ambiguity rather than doing leveraged technical work.

Burnout may be present, and the layoff may have worsened trust, but neither fully explains the pattern. If the primary issue were simply pace, retros would likely center on workload, exhaustion, interruptions, or lack of recovery. If it were primarily psychological safety after layoffs, I would expect more explicit fear, silence, risk avoidance, or distrust of leadership. Here, the dominant symptoms point to a team trying to operate at a new scale with an old leadership pattern.

The recovery plan should therefore focus on leadership and operating-model reset: clarify decision rights, redefine the role of engineering leadership, strengthen squad-to-squad coordination, coach leaders on the maturation-phase behaviors now required, and potentially reallocate responsibilities where leaders are still optimized for the previous phase. PTO and trust-building may help, but they will not fix the underlying coordination and leadership mismatch.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I recommend **Option E: Leadership style mismatch** as the primary diagnosis. The provided signals point to a classic organizational scaling inflection point rather than a sudden loss of technical capability or simple exhaustion. 

A team size of roughly 40 engineers across 4 squads is notoriously the phase where informal, ad-hoc execution breaks down. In the prior "growth phase," strong delivery was likely achieved through sheer talent, individual heroics, and tight-knit informal networks. However, as the team scaled and the product matured, that early-stage leadership style became a bottleneck. 

The smoking gun is the shift in retrospective themes from "what to ship next" to "process and communication." This directly indicates that the team is starving for structured, mature operating systems that current leadership is failing to provide. The engineers do not lack motivation or technical skill; they lack the organizational clarity, alignment, and systems required to execute at their current size. 

Furthermore, the voluntary departure of four *senior* engineers strongly reinforces this diagnosis. Senior engineers typically absorb the most friction when organizational processes fail, as they are often informally expected to bridge the execution gaps between top leadership and the squads. When leadership fails to transition to a more mature operating model, senior talent departs—not because the work is too hard, but because they are exhausted by navigating broken communication loops and unnecessary cross-squad friction. 

To reverse the six-month decline, the CTO must implement Option E's recovery plan. Current engineering leaders need immediate coaching to transition from tactical, growth-stage managers to strategic, maturation-stage leaders. Roles and responsibilities must be redefined to establish the structural guardrails and communication channels the developer floor is actively requesting.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

I recommend **Option E: Leadership style mismatch** as the primary diagnosis.

The most telling signal here is the specific pattern of decline following strong delivery. When a high-performing team of 40 engineers across four squads moves from reliably hitting milestones to missing them for two consecutive quarters—and when senior engineers begin leaving voluntarily—it rarely indicates a uniform capacity collapse. Instead, it signals that the system around the team has shifted in ways that no longer amplify their effectiveness.

The retro theme change is the diagnostic smoking gun. Teams that shift from discussing "what to ship next" to fixating on "process and communication" aren't simply tired—they're struggling with how decisions are made, how work is coordinated, and how clarity is maintained across squads. This is a classic signature of leadership that excels during growth phases (high autonomy, rapid decision-making, founder-like energy) but becomes misaligned during maturation, where cross-team dependencies, standardization, and deliberate communication become critical.

The departure of four senior engineers is particularly revealing. Senior engineers rarely leave primarily due to workload; they leave when they feel their effectiveness is compromised by organizational friction they cannot fix. In a maturation phase, if leadership continues operating with growth-phase instincts—prioritizing velocity over predictability, favoring implicit over explicit coordination—senior technical staff experience increasing frustration as their impact gets diluted by coordination failures.

Option A (burnout) is a symptom, not a cause. Option C (layoff psychological safety shock) is possible, but a layoff four months ago doesn't explain a six-month trajectory that began before that event. The right intervention is leadership coaching focused on the transition from scaling to maturing, redefining the engineering lead's role to emphasize cross-squad alignment and organizational clarity, and potentially reallocating responsibilities so operational maturity gets dedicated attention alongside technical leadership.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

 **Recommendation: Option E — Leadership style mismatch.** The team has outgrown a leadership model that reliably delivered during its growth phase but cannot coordinate a 40-person, four-squad organization in its current maturation phase.

The definitive signal is the retro shift from “what to ship next” to “process and communication.” When a team’s own retros stop debating product and start fixating on how work moves between people, the operating system—not the engineers—is broken. In the prior growth phase, success likely relied on heroic, directive leadership: tight loops, implicit context, and centralized calls. At this scale, that same style produces decision bottlenecks, conflicting squad priorities, and hand-off friction. Engineers do not miss milestones for lack of effort; they miss them because coordination tax now exceeds the capacity of an unmanaged topology.

Four senior engineers leaving voluntarily reinforces this. Seniors attrit when they lose autonomy and strategic influence, not merely when work is hard. A founder-style or pace-oriented leader who will not delegate scope turns senior ICs into executors, which is exactly the flight risk the brief describes.

Alternatives fail to reconcile the symptoms. Burnout (A) would surface as sustainable-pace and overload complaints

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/B_N_run4/cell.json`.

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

**M2 (neutral):**
- avoidance, or distrust of leadership

**M5 (neutral):**
- the brief describes

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
