# Detailed Appendix: B_N_run2

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

# Primary Diagnosis: Option C — Loss of Psychological Safety

The timeline is the strongest signal here, and it points unambiguously to the layoff. A team that was high-performing turned sour roughly 4-6 months ago — precisely synchronized with the workforce reduction. When effect tracks cause that tightly, alternative explanations need to clear a high bar.

The qualitative signals corroborate it. Retro themes shifting from "what to ship" to "process and communication" is the classic fingerprint of a team that no longer feels safe taking risks. Engineers stop volunteering for ambitious work, start over-documenting decisions, escalate ambiguity rather than absorbing it, and route around perceived political risk. Output declines not because capacity is gone but because the team has shifted from offense to defense. Voluntary senior attrition reinforces this: senior engineers have the most market optionality and are the first to leave when they sense the implicit contract has broken. They also read organizational tea leaves better than juniors.

Why not the others? **Burnout (A)** would more typically produce sick leave, quality defects, and exhaustion complaints — not a thematic shift toward process. **Incentive misalignment (B)** is rarely a 6-month-onset problem; comp structures usually predate the decline. **Skill atrophy (D)** doesn't explain attrition of *senior* engineers, who are the least vulnerable to it, nor does it appear suddenly. **Leadership mismatch (E)** is the most plausible alternative and may well be a secondary factor — leadership style that worked pre-layoff may now be inadequate to the repair work required — but it's a slower-moving structural issue that doesn't explain the sharp inflection.

The recovery plan in Option C is also the most leveraged: trust and transparency about future workforce decisions directly addresses the unspoken question every remaining engineer is asking ("am I next?"). Until that question is answered credibly, interventions on pace, incentives, or skills will underperform because they don't touch the root cause.

**Recommendation:** Treat C as primary; revisit E as a likely secondary diagnosis once safety is restored and residual performance issues can be assessed cleanly.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

The most likely primary diagnosis is **loss of psychological safety following the layoff round**.

The strongest signal is the timing and the change in the team’s conversational texture. A team that previously oriented around “what to ship next” has shifted toward “process and communication.” That often happens when people no longer feel safe making decisions, challenging priorities, surfacing risks early, or trusting leadership intent. In that environment, “process” becomes a proxy complaint: people ask for clearer rules because informal trust has degraded.

The voluntary departure of four senior engineers is also consistent with this diagnosis. Senior people are often the first to leave when they perceive leadership as opaque, unstable, or unwilling to own hard decisions. They usually have the most external options and the clearest read on whether the team’s operating environment is improving or deteriorating. If their exits followed a layoff, it suggests the layoff may have damaged confidence in the organization’s direction and leadership compact.

Missed milestones are then a downstream symptom. Teams with low psychological safety do not necessarily stop working hard; they stop communicating honestly. Risks get hidden until late. People avoid disagreement. Decision-making slows because no one knows what is safe to say. Cross-squad coordination deteriorates. Retros become procedural because the real issues feel too charged to name directly.

I would not start with PTO, compensation, or skill programs as the primary recovery lever. Those may help at the margin, but they will underperform if the core issue is trust. The recovery plan should begin with leadership transparency: what happened, why the layoff occurred, what conditions would trigger future workforce changes, and what commitments leadership can credibly make. The CTO and engineering leaders should run structured listening sessions, acknowledge specific leadership misses, and create visible mechanisms for escalation without retaliation.

The goal is to restore the belief that speaking candidly is both safe and useful. Until that is repaired, process fixes will likely look like motion without recovery.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend **Option E: Leadership style mismatch** as the primary diagnosis for the engineering team's decline. 

The surface signals brilliantly describe a classic organizational scaling fracture. A 40-person engineering department distributed across four squads represents a critical inflection point. At this size, the informal, high-autonomy leadership style that drives early "growth phase" success—where everyone shares a single context and the focus is purely on "what to ship next"—inevitably breaks down. 

The most telling signal is the shift in retrospective themes from product delivery to "process and communication." This is a smoking gun for an organization that has outgrown its operational infrastructure. When leadership fails to adapt from managing *code and individuals* to managing *systems and structures*, inter-squad dependencies become chaotic. Engineers find themselves spending more time navigating unclear workflows and communication gaps than actually building software, directly causing the missed quarterly milestones. 

Furthermore, this perfectly contextualizes the voluntary exit of the four senior engineers. Senior staff possess a low tolerance for the friction of a growing organization that lacks mature leadership. They are accustomed to high productivity; when they are suddenly bogged down by operational chaos and a lack of clear organizational design, they vote with their feet. 

While burnout (Option A) might cause dips in output, exhausted teams typically complain about workload, not process. The root cause of this sudden friction is a leadership team applying an early-stage playbook to an increasingly complex, mid-sized organization. Implementing Option E’s recovery plan—centered on leadership coaching, establishing mature operational frameworks, and redefining structural roles—is the most effective way to unblock the team, fix the communication breakdowns, and halt further senior attrition.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

The primary diagnosis is a **leadership style mismatch** (Option E). While the layoff four months ago likely accelerated the damage, the team’s decline began roughly six months ago—two months before that event—ruling it out as the initial cause. The critical clue is the retro shift from “what to ship next” to “process and communication.” This signals a team that has lost its external momentum and is now consuming its energy on internal mechanics, a classic symptom of leadership that fails to adapt when a team moves from a high-growth phase to a maturation phase.

The prior strong delivery suggests the engineering leader excelled at driving execution under ambiguity, likely through hands-on, directive, or vision-driven leadership that worked well when speed and entrepreneurial energy were paramount. As the team scaled to 40 people across four squads, the demands changed: the team now needs clearer delegation, cross-squad alignment, strategic context, and empowered decision-making. If the leader continued in the earlier mode—either micromanaging, failing to provide adequate structure, or communicating inconsistently—senior engineers would feel stifled, misdirected, or disconnected from purpose. Their voluntary departures become a rational response to frustration, not just burnout or pay issues.

The missed quarterly milestones further reinforce this: it’s not that the team can’t execute, but that they are wrestling with priorities, handoffs, and conflicting expectations—all hallmarks of a leadership gap in navigating complexity. A recovery plan centered on leadership coaching, role redefinition, or reallocating responsibilities directly addresses the root cause. Restoring trust after the layoff will be essential, but that trust will remain fragile if the underlying leadership style isn’t recalibrated to meet the team’s current needs. Fix the leadership operating system, and psychological safety, alignment, and output will follow.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

I recommend **Option E — leadership style mismatch** — as the primary diagnosis. The symptom pattern points to a classic organizational inflection point: the team has outgrown the leadership operating model that produced its earlier strong delivery, and the resulting friction is now masquerading as execution failure.

At roughly 40 people across four squads, the group has clearly transitioned from a growth phase into a maturation phase. The prior success proves the talent is strong; the sudden decline over six months suggests the system around them has broken, not the individuals. The retro theme shift from “what to ship next” to “process and communication” is especially telling — it signals that the team is stuck in meta-work, struggling with decision rights, information flow, and cross-squad coordination. That is the sound of a leadership model failing to scale. Meanwhile, voluntary attrition among senior engineers is a canary-in-the-coal-mine: experienced talent departs first when they lose confidence in direction-setting and perceive political overhead replacing technical progress.

This diagnosis better integrates the evidence than the alternatives. Burnout would center on exhaustion and workload, not organizational mechanics. Misaligned incentives rarely cause a simultaneous collapse in culture and delivery velocity within half a year. Skill atrophy would surface as technical capability gaps, not communication breakdowns. And while psychological safety is plausible, the brief emphasizes a phase transition rather than a discrete traumatic event, making a leadership-model misfit the more parsimonious root cause.

Option E’s recovery plan — leadership coaching, role re

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/B_N_run2/cell.json`.

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
- early, or trusting leadership intent
- get hidden until late

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
