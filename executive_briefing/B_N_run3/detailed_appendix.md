# Detailed Appendix: B_N_run3

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

# Primary Diagnosis: Option C — Loss of Psychological Safety Following the Layoff

The temporal evidence is the most compelling signal here. A layoff occurred four months ago; the decline in output, the senior departures, and the shift in retro themes all post-date that event and cluster tightly around it. When a high-performing team suddenly stops talking about "what to ship" and starts talking about "process and communication," that is rarely a process problem — it is almost always a trust problem expressing itself in the safest available vocabulary. Process critique is what teams escalate to when they cannot yet say "I don't trust what's happening above me."

The pattern of senior departures reinforces this. Four senior engineers leaving voluntarily is not the signature of burnout (which tends to take juniors and mid-levels first, or produces medical leave before resignations) nor of skill atrophy (which produces disengagement, not exit). Senior engineers have the most market optionality and the sharpest read on organizational risk. When they leave in a cluster after a layoff, they are voting on perceived future stability and leadership credibility.

Burnout (A) is plausible but would have been visible *before* the layoff, given the "sustained pace" framing — yet delivery was strong until two quarters ago. Incentive (B) and specialization (D) issues are slow-moving and don't explain a sharp inflection. Leadership-phase mismatch (E) is the strongest alternative and may well be a contributing factor, but it's a longer-arc diagnosis that doesn't match the sudden six-month deterioration; it's more likely an amplifier than the root.

The recovery plan for C is also the highest-leverage: transparency on future workforce decisions and visible leadership accountability directly address the unspoken question driving the behavior ("am I next, and can I trust what I'm told?"). Until that question is answered, interventions targeting workload, comp, or skills will be received as deflection — which will accelerate, not reverse, the attrition.

**Recommendation: Diagnose as C, with E monitored as a likely secondary factor.**

### M2 (frame: neutral, model: `openai/gpt-5.5`)

The most likely primary diagnosis is **Option E: leadership style mismatch**.

The strongest signal is the shift in retrospectives from “what should we ship next?” to “process and communication.” That usually means the team’s operating model is no longer matching its complexity. A 40-person engineering group across four squads is past the point where heroic coordination, informal alignment, founder-style urgency, or high-trust verbal agreements are enough. Those patterns often work well during a growth or push phase, but they begin to fail when the organization needs clearer ownership, cross-squad planning, prioritization discipline, and more explicit communication channels.

The missed milestones across two quarters also point to a system-level execution problem rather than a single overloaded sprint or isolated morale dip. If this were primarily burnout, I would expect fatigue, quality issues, and reduced velocity, but not necessarily a retro pattern centered on process and communication. If it were primarily the layoff, the timing would matter: the decline has been visible for six months, while the layoff occurred four months ago. The layoff may have worsened trust and attrition, but it is less likely to be the root cause if the decline predates it.

The loss of four senior engineers is especially consistent with leadership mismatch. Senior people are often the first to leave when decision-making becomes unclear, when they feel they are compensating for organizational gaps, or when leadership does not adapt from “drive harder” to “build a scalable system.”

The recovery plan should therefore focus on leadership coaching, clearer role definitions, and possibly reallocating responsibilities. The CTO should assess whether current leaders are still operating as delivery accelerators when the team now needs integrators, prioritizers, and system designers. Fixing PTO or incentives may help at the margins, but unless the leadership model changes, the same coordination failures will keep reproducing.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I recommend **Option E (Leadership style mismatch)** as the primary diagnosis. This conclusion is driven by the specific nature of the surface signals—most notably, the shift in retrospective themes and the nature of the attrition—when viewed through the lens of organizational scale.

A 40-person engineering organization split across four squads sits exactly at the inflection point where informal, startup-style operational models break down. During an initial "growth phase," strong delivery is often achieved through tight-knit, brute-force heroics and informal alignment. However, as the product and team mature, that same leadership style inevitably leads to chaotic cross-squad dependencies, strategic ambiguity, and operational drag. 

The most telling symptom is the shift in retrospective themes from "what to ship next" to "process and communication." When teams are simply burned out from sustained pace, retrospectives typically highlight excessive workloads, technical debt, or sheer exhaustion. A hyper-focus on process and communication strongly indicates that the foundational scaffolding of the organization is failing. The engineers are struggling with *how* work gets done, pointing to workflow bottlenecks, unclear scopes, and misaligned priorities—all hallmarks of a leadership team that has not adapted its management style to a maturation phase. 

Furthermore, the voluntary departure of four senior engineers is a critical signal. Senior engineers are highly sensitive to systemic inefficiencies because they are usually the ones forced to bridge the communication gaps when leadership fails to establish mature processes. Their grouped exit is rarely tied to compensation or temporary fatigue; rather, it is usually a vote of no confidence in the current operational environment and a rejection of the resulting administrative friction.

To recover, the CTO must address the leadership gap. By implementing leadership coaching, redefining managerial roles, and establishing mature organizational processes, the company can clear the communication bottlenecks and empower the squads to return to high output.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

The most likely primary diagnosis is **Option C: Loss of psychological safety following a layoff round 4 months ago**. The timeline and symptoms align tightly with a trust rupture, not just accumulated fatigue or compensation gripes. The decline began within two months of the layoff—a classic lag as remaining employees first go into shock, then into self-protection mode. High-performing teams depend on candid debate and intelligent risk-taking, both of which evaporate when people feel their jobs are contingent. The shift in retro themes from “what to ship next” to “process and communication” is a diagnostic red flag: the team has stopped focusing on the product and started focusing on how to survive each other and management. They are likely avoiding conflict, over-aligning on safe tasks, and slowing down due to invisible coordination costs.

The voluntary departure of four senior engineers reinforces this. Senior engineers have the most market mobility and the least tolerance for environments where they cannot speak freely or influence direction. They leave not just for better pay, but because they sense a loss of agency and trust. If burnout were primary, we’d see broad-based exhaustion signs, not a selective exit of seniors. If incentives were misaligned, the retro themes would center on rewards, not communication. And if leadership style were the sole issue, the decline would trace more directly to specific leadership actions, not a discrete event like a layoff. The recovery plan—structured trust rebuild, transparency on future workforce decisions, and leadership accountability—is precisely what research on psychological safety prescribes after an integrity breach. Ignoring this root cause would render any load-management or comp-fix superficial.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

 The primary diagnosis is leadership style mismatch (Option E).

The most telling signal is the shift in retrospective themes from “what to ship next” to “process and communication.” That is not the vocabulary of individual exhaustion; it is the vocabulary of systemic coordination failure. A team that delivered strongly and then begins missing milestones while fixating on communication channels has typically outgrown a leadership model that worked for a single squad but fractures at the ~40-person, four-squad boundary.

This pattern fits a classic maturation event. Six months of declining output and voluntary attrition among senior engineers suggests the organization has hit a scaling breakpoint. Seniors rarely leave en masse simply because they are tired—they leave when they lose faith that leadership can architect the coordination systems required for sustainable execution. The back-to-back missed quarterly milestones are consistent with ambiguous decision rights, conflicting priorities across squads, and process debt accumulating because managers are still operating in a hands-on, directive mode suited to an earlier growth phase rather than an enablement mode suited to a multi-squad structure.

Burnout may be present, but it is a downstream symptom of chaotic process and unclear ownership. Without any evidence in the brief of compensation complaints or recent layoffs, misaligned incentives or psychological safety collapse require importing hypothetical causes not supported by the surface signals. Skill atrophy is even less consistent with the retrospective focus.

Recovery must therefore start at the top: leadership coaching to transition from heroics to systems-thinking, redefining roles to emphasize coordination architecture, and reallocating responsibilities so that squad leads own delivery rather than being overridden by centralized command. Fix the leadership operating system, and execution and retention will recover.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/B_N_run3/cell.json`.

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
