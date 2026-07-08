# Detailed Appendix: D_P_run5

## A. Full task brief

```
# Task D: National climate adaptation strategy

## Context

You are advising the national government of a mid-sized coastal country (population ~50M, GDP ~$1T, 4500 km of coastline) on its 15-year climate adaptation strategy. The country faces compounding pressures: projected sea-level rise of 30-50 cm by 2040, increasingly frequent extreme weather (3 major hurricanes in the past 5 years vs the historical baseline of one per decade), agricultural shifts (10-15% reduction in current crop yields projected by 2035), internal climate migration (estimated 2-3M displaced from coastal/low-lying areas over the horizon), and fiscal constraints (climate budget capped at 2.5% of GDP, ~$25B/year).

Five candidate national strategies have been developed by inter-ministerial working groups. **Choose one as the primary strategy.** The chosen strategy will define ~70% of the climate budget allocation; the remaining 30% goes to baseline preparedness regardless.

## Options

**Option A: Hard infrastructure-first ("seawalls and grids")**
Concentrate spending on engineered defenses: seawalls, reinforced ports, flood barriers, hardened power grids, desalination plants. Outcomes: protects existing assets and current population centers; high engineering certainty; visible/legible to public; lock-in of current geography. Risks: hard infrastructure can be overtopped by worse-than-projected events; doesn't address inland or systemic pressures; "fortress mentality."

**Option B: Managed retreat and relocation**
Plan and fund gradual depopulation of highest-risk coastal zones over 15 years. Buy-out programs, relocation incentives, new inland city development, abandonment of vulnerable infrastructure. Outcomes: reduces long-term exposure dramatically; frees future budgets; aligns with worst-case projections. Risks: politically explosive (forced moves); cultural/heritage loss; new inland infrastructure also expensive; signal of "giving up."

**Option C: Ecosystem-based adaptation**
Invest in natural defenses: mangrove restoration, wetland reconstruction, coastal forest preservation, soil-microbe agriculture, watershed management. Outcomes: cheaper per km than hard infrastructure (~30%); co-benefits (biodiversity, fisheries, carbon sink); self-healing. Risks: slower to deploy (5-10 year maturation); less predictable protection levels; harder to attribute political wins.

**Option D: Technology-and-resilience platform**
Bet on adaptive technology: distributed renewable grids, AI-managed early warning, climate-tolerant crop genetics, mobile/modular infrastructure, supply chain redundancy. Outcomes: leverages knowledge economy strengths; creates exportable IP; flexibility under uncertainty. Risks: technology bets may not mature in time; vulnerable to systemic tech failures (cyber, supply); doesn't address physical fixed assets.

**Option E: Social cohesion and human capital first**
Prioritize the people who'll face the changes: universal climate health insurance, retraining for displaced workers, expanded social housing for migrants, climate education in schools, community-led adaptation funds at the municipality level. Outcomes: builds adaptive capacity at every income level; politically durable (broad benefit); addresses indirect climate harms (mental health, social cohesion). Risks: physical infrastructure deteriorates; political resistance from technical/industrial interests; slow visible impact.

## What to provide

Choose one option as primary strategy. Provide 200-400 words of reasoning. Advocate for your choice rather than enumerate trade-offs of all five. Address: why this option, why not the most plausible alternative, what its main vulnerability is.

```

## B. Each voice in their own words

### M1 (frame: H, model: `anthropic/claude-opus-4.7`)

# Recommendation: Option E — Social cohesion and human capital first

## Why this strategy

Begin from the question that economic and engineering framings tend to obscure: *who actually bears the weight of climate disruption, and what determines whether they survive it with dignity?* The answer is rarely the seawall. It is whether a displaced farmworker can access healthcare when the next hurricane hits, whether a relocated family finds housing rather than a slum, whether a fishing community has the literacy and institutional access to claim adaptation funds at all. With 2-3 million internal migrants projected, the central adaptation challenge is not protecting coastline kilometers — it is preventing the creation of a permanent climate underclass.

Option E does this directly. Universal climate health insurance prevents medical catastrophe from compounding displacement. Retraining and social housing convert migration from a humanitarian crisis into a managed transition. Municipality-level adaptation funds devolve decisions to communities who know their own vulnerabilities — a critical corrective against capital-city technocrats deciding which villages are "worth" defending. Crucially, this strategy distributes benefits across income deciles, which is both ethically required and politically stabilizing: a strategy that visibly serves only coastal property owners (Option A) or knowledge workers (Option D) will not survive 15 years of electoral cycles.

## Why not Option C, the most plausible alternative

Ecosystem-based adaptation is attractive — cheaper, co-beneficial, ecologically sound. But it answers a different question. Mangroves do not retrain a 52-year-old port worker whose job has vanished. Wetlands do not provide mental healthcare to communities watching their hometowns flood. Option C should be the dominant *secondary* investment within the remaining 30% baseline and through municipal adaptation funds under E — but it cannot be primary, because it leaves the human distributional question unanswered.

## The main vulnerability

Physical infrastructure will degrade. Some coastal assets that hard defenses could have saved will be lost, and the political backlash when a hurricane breaches an under-invested seawall will be severe. This is real. The mitigation is rigorous baseline preparedness in the 30%, prioritizing ecosystem buffers and triage-level hard defense for the highest-density populations — and honest public communication that no strategy protects everything, but this one protects *everyone*.

### M2 (frame: C, model: `openai/gpt-5.5`)

**Recommendation: Option E — Social cohesion and human capital first.**

The country’s central adaptation problem is not only water; it is whether 50 million people can absorb repeated shocks without political, economic, and social fracture. The hidden assumption behind most adaptation plans is that protecting places equals protecting the nation. That is doubtful. Some coastal assets will be defensible; many will not. Some forecasts will be wrong; some storms will exceed design limits. But a population with housing options, portable skills, health coverage, trusted local institutions, and migration pathways remains adaptive under many climate futures.

Option E should therefore be the primary strategy. It turns adaptation from a capital-works program into a national resilience system. Climate migration of 2–3 million people is not a side effect; it is one of the main events. If the state fails to manage housing, employment, health, education, and local legitimacy, even well-built infrastructure will sit inside a destabilized society. Social housing, retraining, climate health insurance, and municipal adaptation funds are also relatively reversible: they can be redirected as risks become clearer, unlike a seawall that locks the country into defending yesterday’s settlement pattern.

The most plausible alternative is **Option A**, because it is visible, technically legible, and politically satisfying. But it risks becoming an expensive promise that the coastline can be held in place. Hard defenses invite overconfidence, concentrate future losses behind the wall, and create a brutal allocation problem: which towns get saved and which are abandoned? They should be used selectively for critical national assets, but not as the organizing principle.

The main vulnerability of Option E is that it may look underpowered after a catastrophic storm: people will ask why more concrete was not built. That is real. The answer is to reserve the baseline 30% for targeted protection of ports, hospitals, grids, evacuation routes, and emergency systems. But the 70% priority should be national absorptive capacity. In a deeply uncertain climate future, the safest asset to harden is the population.

### M3 (frame: Q, model: `google/gemini-3.1-pro-preview`)

From a strict expected value (EV) framework, the optimal adaptation strategy must minimize measurable loss under compounding uncertainty. The objective loss function is $\text{Risk} = P(\text{Hazard}) \times \text{Exposure}$. I recommend **Option B: Managed retreat and relocation**, because it is the only strategy that structurally zeroes out the "Exposure" variable rather than battling the highly uncertain "Hazard" probability.

Show me the data: extreme weather frequency has already experienced a $6\times$ multiplier ($\lambda_{hist} = 0.1$/yr to $\lambda_{current} = 0.6$/yr). Assuming a strict $17.5B annual allocation (70% of the $25B budget), a 15-year timeline yields $262.5B. Empirically, relocating 3 million displaced individuals at a generous $80,000 per capita operational cost totals $240B. This neatly fits our fiscal constraint and yields a mathematically guaranteed return: a 100% reduction in future capital asset exposure in designated run-off zones.

The most plausible alternative, **Option A (Hard infrastructure)**, fails under an EV analysis due to the right-skewed tail risks of climate models. Engineering hard defenses for 4,500 km of coastline with $17.5B annually—approximately $3.8M per km/year—is fiscally unviable to achieve uniform protection. Furthermore, seawalls suffer from binary failure states. The 95% confidence interval for sea-level rise is currently 30–50 cm; if empirical reality shifts to a 60 cm P99 tail event, hard infrastructure is overtopped, yielding a catastrophic loss of the protected assets *plus* the sunken $262.5B defense costs. Option B avoids this lock-in by capping maximum probable loss. 

Option B's primary vulnerability is the confidence interval surrounding domestic relocation costs. While the direct buyout costs are falsifiable and easily operationalized, the secondary inflationary effects on inland real estate markets remain uncertain. If inland development costs breach the upper bound of our 95% CI (costing $> \$100,000$ per capita), the strategy will exceed the statutory 2.5% GDP cap, forcing us to dilute the baseline preparedness budget. However, unlike Option A, this financial risk can be tracked month-to-month and managed via dynamic pricing incentives, whereas physical infrastructure failure is an unmanageable step-function.

### M4 (frame: S, model: `deepseek/deepseek-v4-pro`)

Of the five strategies, **Option E (social cohesion and human capital first)** is the only one that addresses the system’s core leverage point: its capacity to adapt under compounding, non-linear shocks. In a systems view, a nation’s resilience is not a function of its physical assets or technology, but of the trust, learning, and adaptive capacity embedded in its social fabric. We therefore recommend Option E as the primary strategy, allocating approximately 70% of the climate budget to it.

The primary argument is about the nature of the threats. We are not facing a single, predictable stressor (e.g., a one-time sea-level rise) but a cascade of interacting failures: crop failures triggering migration, which strains urban housing, which erodes social trust, which then collapses the political will to fund any technical solution. Hard infrastructure (Option A) and technology bets (Option D) treat these as discrete engineering problems, creating brittle, optimized systems that fail catastrophically when a hurricane exceeds the seawall height or a cyber-attack hits the centralized grid. They are investments in *complication*, not *complexity*.

Managed retreat (Option B) is the most plausible alternative because it honestly confronts physical risk. However, it is politically fragile and, crucially, treats people as units to be moved rather than agents of adaptation. It risks a second-order effect of creating a displaced, disenfranchised population whose social capital is destroyed, creating a new, more profound vulnerability.

Option E directly builds the absorptive capacity of the system. By providing universal climate health insurance, retraining, and social housing, it creates buffers. By funding community-led adaptation, it distributes cognition and decision-making to the local level, where the most accurate and granular information about changing conditions exists. This is the definition of anti-fragile: the system can heal and reorganize in response to unforeseen shocks because its constituent elements—people and communities—have the resources and agency to do so.

The main vulnerability of this strategy is not financial or technical; it is political time. The payoffs are slow and diffuse, while a collapsing bridge or a flooded port is an acute, visible crisis that demands a visible, physical response. The risk is that a future government, in response to a disaster, cannibalizes the social cohesion budget to build a seawall, thereby locking the country into a high-cost, brittle trajectory and starving the human systems that provide long-term, generic resilience. We must accept this political risk to avoid a far greater systemic one: a society with strong walls but a hollowed-out core, unable to weather the storms of the next 15 years.

### M5 (frame: E, model: `moonshotai/kimi-k2.6`)

The binding constraint is fiscal and physical scale: you cannot oppose 4,500 km of ocean with static concrete on a 2.5% GDP budget while hurricane frequency has jumped 6×. The actual mechanism of coastal protection is energy dissipation, not force opposition. Therefore, choose **Option C**.

Ecosystem-based adaptation deploys the physics of drag and friction—mangrove prop roots and wetland vegetation attenuate wave energy and storm surge at roughly 30% the cost of hard structures per kilometre, and they self-repair after repeated events. This is the minimal solution: work with thermodynamics rather than against them. Simultaneously, soil-microbe interventions and watershed management address the agricultural yield-collapse mechanism directly, restoring water retention and nutrient cycling under heat stress. One strategy class covers coastline, food security, and inland flood buffering without locking the country into a depreciating geography.

The most plausible alternative, Option A, fails first principles. Seawalls attempt to hold a fixed boundary against a dynamic, rising one. They embody massive capital and carbon, demand maintenance under cyclic fatigue from frequent hurricanes, and fail catastrophically when overtopped. Over 4,500 km the strategy is fiscally impossible; it consumes the budget to defend assets that are losing value, producing negative marginal return.

The main vulnerability is time. Natural systems require 5–10 years to reach protective density. During the establishment phase the coastline remains dangerously exposed. Success hinges on compressing that maturation window through aggressive front-loading of nursery capacity, sediment diversion, and strict protective zoning that prevents ecosystem destruction during growth.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 15 constructs is in `results/D_P_run5/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 0.739 |
| M1 vs M4 | 0.993 |
| M2 vs M4 | 1.076 |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M2 (C):**
- become clearer, unlike a seawall that locks the country into defending yesterday’s settlement pattern
- becoming an expensive promise that the coastline can be held in place

**M3 (Q):**
- climate models
- can be tracked month-to-month and managed via dynamic pricing incentives, whereas physical infrastructure failure is an unmanageable step-function

**M4 (S):**
- a second-order effect of creating a displaced, disenfranchised population whose social capital is destroyed, creating a new, more profound vulnerability
- to avoid a far greater systemic one: a society with strong walls but a hollowed-out core, unable to weather the storms of the next 15 years

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
