# Detailed Appendix: B_N_run1

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

The timeline is the strongest signal. A layoff occurred 4 months ago; decline has accelerated over 6 months with the steepest symptoms (senior departures, retro shift) appearing *after* the layoff. When previously high-performing teams pivot retro language from "what to ship" to "process and communication," that is almost always a trust signal, not a process signal. Process complaints are how engineers safely voice fear: it's socially acceptable to critique a standup, far riskier to say "I don't trust leadership won't cut me next."

The senior departures reinforce this. Burnout (Option A) typically claims the most loaded ICs broadly, not specifically four seniors — seniors leave when they lose confidence in the org's trajectory or leadership's judgment, and they have the market optionality to act first. Their exit is a leading indicator that the people with the most context and the most options have updated their priors downward.

Why not the others as primary?
- **Burnout (A)** is likely a *co-occurring* symptom but doesn't explain why retros shifted to communication themes, nor the timing cluster around the layoff.
- **Incentives (B)** rarely flip a high-performing team in 6 months; comp issues produce slow drift, not cliff-edge decline.
- **Skill atrophy (D)** doesn't match — output is declining, not quality of technical decisions, and there's no signal of capability gaps.
- **Leadership mismatch (E)** is plausible and may be partially true, but it's a structural explanation for a symptom pattern that has an acute trigger. Occam's razor favors the discrete event.

**Recovery emphasis:** The proposed plan is directionally right but order matters. Lead with *transparency on future workforce decisions* — concrete commitments (criteria, timing, runway). Trust-rebuild rituals without that substrate become performative and accelerate cynicism. Leadership accountability sessions should include naming what the layoff cost the team, not just process resets. Expect 2-3 quarters before delivery metrics recover; pushing for faster will re-trigger the original wound.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

My recommendation is **leadership style mismatch** as the primary diagnosis.

The strongest signal is the qualitative shift in retrospectives: a team that used to focus on “what to ship next” is now spending its energy on “process and communication.” That usually means the team’s operating system is no longer matching its scale or stage. At ~40 engineers across 4 squads, the leadership behaviors that worked during a high-growth, high-delivery phase—fast decisions, heroic execution, informal coordination, strong founder/CTO-style direction—can start to create ambiguity, bottlenecks, and frustration as the organization matures.

The missed milestones and senior attrition are consistent with this. Senior engineers often leave when they feel the environment no longer lets them be effective: unclear priorities, too much coordination tax, inconsistent decision-making, or leadership that is either too directive for experienced teams or too hands-off for a more complex organization. The fact that four senior engineers left voluntarily suggests more than temporary fatigue; it suggests loss of confidence in how the team is being led and how work gets done.

Burnout and psychological safety may be contributing factors, especially if the team has recently endured sustained pace or layoffs. But I would treat those as downstream symptoms or amplifiers unless there is stronger evidence they are the root cause. The broader pattern points to a team that outgrew its previous leadership model.

The recovery plan should focus on redefining leadership responsibilities, decision rights, planning cadence, and cross-squad coordination. The CTO should assess whether current engineering leaders are still fit for the team’s present needs, provide coaching where possible, and reallocate responsibilities where necessary. The goal is not to blame leadership, but to update the management system so a previously high-performing team can operate effectively at its new level of complexity.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

The most likely primary diagnosis for the decline in team performance is **Option E: Leadership style mismatch**, specifically stemming from leadership's failure to adapt as the organization transitions from a growth phase to a maturation phase.

A 40-person engineering organization distributed across four squads represents a critical scaling threshold. During earlier growth phases, teams can successfully rely on a highly informal, execution-oriented leadership style. However, as complexity scales to four distinct teams, the implicit, ad-hoc coordination that previously drove "strong delivery" fundamentally breaks down.

The most compelling signal for this diagnosis is the shift in retrospective themes from "what to ship next" to "process and communication." This shift is a direct operational cry for help. The team is actively diagnosing that the lack of mature structural scaffolding is what is now blocking their delivery. A growth-stage leadership style—which typically prioritizes hustle and informal alignment over scalable systems—creates severe operational friction once an engineering organization reaches this size and complexity. 

Crucially, this diagnosis explains the voluntary departure of the four senior engineers. In scaling environments that lack mature communication pathways, senior engineers inevitably become the organizational "glue." They are forced to manually bridge communication gaps across squads and manage systemic friction. When leadership fails to adopt a mature, process-oriented mindset, these senior contributors are left shouldering heavy, invisible organizational debt. They become frustrated by having to fight the system to get work done, leading directly to attrition.

Past success followed by a systemic scaling failure points directly to an organizational bottleneck at the top. To reverse the six-month slide in milestone delivery, the CTO must implement the Option E recovery plan. By initiating leadership coaching, redefining roles, and establishing the formal operational processes required of a mature 40-person organization, the company can directly resolve the systemic friction currently paralyzing the squads.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

The most likely primary diagnosis is **Option C: Loss of psychological safety following the layoff round 4 months ago**.

The timeline is the strongest signal. The decline began roughly 6 months ago, and a major organizational trauma—a layoff—occurred 4 months ago. Such events are well-documented to fracture psychological safety, especially in previously high-performing teams where members feel a strong sense of shared purpose and social cohesion. The sudden removal of colleagues, even with a rational business justification, often reads to survivors as a breach of the implicit “we take care of our own” contract. This triggers a cascade: trust evaporates, risk-taking plummets, and energy shifts from external delivery to internal self-protection.

The symptoms align precisely. Four senior engineers voluntarily left in the wake of the layoff; high-performers with options are the first to exit when trust is broken. The retro themes migrating from ambitious “what to ship next” to defensive “process and communication” reveal a team that no longer feels safe to debate ideas or raise problems openly. Instead, they retreat into meta-conversations about how work gets done, often a proxy for unspoken fears about job security, scapegoating, or broken fairness norms. Missed quarterly milestones then become a second-order effect of a team that has deprioritized execution to navigate a minefield of interpersonal caution.

While burnout (A) or leadership mismatch (E) could contribute, they don’t explain the abrupt shock and the specificity of the shift. A layoff is a single, observable cause that perfectly fits the pattern: strong delivery, then a trust-destroying event, then attrition, process fixation, and missed commitments. Other factors may be present, but they are downstream of the primary rupture. The recovery plan must therefore start with a structured rebuild of psychological safety—transparent future workforce commitments, leadership accountability, and deliberate trust-restoration exercises—before any productivity interventions can succeed.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

 The primary diagnosis is **Option C: loss of psychological safety following the layoff round**. This is the only explanation that binds the timeline, talent signals, and retrospective data into a coherent causal chain.

Layoffs are acute organizational trauma. Their worst symptoms often lag by one to two quarters, precisely matching this team’s trajectory. The immediate aftermath is not just grief but ambient threat: employees begin to question whether candor is safe, whether mistakes are survivable, and whether leadership’s future workforce decisions can be trusted. That threat asymmetrically hits senior engineers, who possess the greatest market mobility and the lowest tolerance for low-trust environments; their voluntary exit is both a symptom and an accelerant. When four senior engineers leave a forty-person organization, they do not merely reduce headcount—they dismantle informal coordination networks and cultural memory, which immediately degrades execution velocity.

Consequently, missed milestones are not a capacity problem but a decision-tax problem. Energy that once went into shipping is now diverted to self-protection, excessive consensus-building, and bureaucratic cover. The retrospective shift from “what to ship next” to “process and communication” is the decisive signal: it indicates that interpersonal friction and hidden constraints—not technical roadblocks or incentive misalignment—are the binding constraint. Burnout would surface as exhaustion and sustainability complaints; a leadership-style mismatch would likely appear as strategic disillusionment before execution collapse; misaligned incentives would generate political gaming rather than flight; skill atrophy is far too gradual to match a six-month inflection. Only a collapse in psychological safety explains why a formerly high-performing team suddenly cannot talk its way to clear decisions.

Recovery must therefore begin with trust, not scope redistribution or compensation tweaks. Structured transparency on future workforce stability, leadership accountability sessions, and explicit rituals to re-normalize dissent are the necessary pre

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 13 constructs is in `results/B_N_run1/cell.json`.

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
