# Detailed Appendix: D_P_run3

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

## Recommendation: Option E — Social cohesion and human capital first

**Who is affected, and how?** The honest answer is that 2-3 million people will be displaced regardless of which seawall we build or mangrove we plant. The 30-50 cm of sea-level rise is largely locked in; the hurricanes are already arriving. The question is not whether dislocation happens but whether the people experiencing it — disproportionately poor coastal communities, smallholder farmers, informal workers, the elderly who cannot relocate easily — face it with a safety net or without one. Every other option optimizes for assets, geography, or technology. Option E optimizes for the human beings who will actually live through the next 15 years of disruption.

**Why this, concretely.** Universal climate health insurance prevents the cascade where a single flood event pushes a working family into permanent destitution. Retraining and social housing convert "climate migrants" — a category that historically becomes a permanent underclass — into absorbed citizens. Municipality-level adaptation funds respect that a fishing village in the south and a rice-farming district inland face different threats and know their own terrain better than any ministry. This is also the most politically durable choice: a population that feels protected supports continued climate spending; a population that watches seawalls protect wealthy districts while their livelihoods erode produces backlash and policy reversal.

**Why not Option C, the strongest alternative.** Ecosystem-based adaptation is genuinely excellent on cost-benefit grounds and I would push hard for it within the residual 30% baseline budget and within municipal adaptation funds. But mangroves do not retrain a 45-year-old dockworker whose port is closing, and wetlands do not insure a diabetic grandmother against a heat wave. Ecosystems are a *means*; human dignity under transition is the *end*. Choosing C as primary risks the same error as A and D: treating the physical system as the patient when the patient is the society.

**Main vulnerability.** Physical infrastructure will degrade visibly while this strategy's benefits remain diffuse and statistical. Within 5-7 years, a major hurricane will hit hardened-but-aging defenses and critics will say we chose welfare over walls. Mitigation: ringfence a meaningful share of the 70% for community-led *physical* adaptation, and publish per-municipality outcome data so the human gains become legible.

### M2 (frame: C, model: `openai/gpt-5.5`)

I recommend **Option E: Social cohesion and human capital first** as the primary national adaptation strategy.

The contrarian point is that climate adaptation will not be won by correctly guessing which coastline, crop, grid node, or port fails first. It will be won by making the population mobile, healthy, employable, housed, and institutionally trusted when forecasts are wrong. The country is already facing 2–3 million likely internal migrants; that is not just an engineering problem, it is a legitimacy problem. If migration becomes chaotic, every other adaptation investment becomes harder: housing prices spike, local backlash grows, health systems strain, labor markets fragment, and disaster response becomes politicized.

The most plausible alternative is a hard infrastructure-first strategy. It is attractive because it is visible, buildable, and politically legible. But it risks spending the next 15 years defending yesterday’s settlement pattern. Seawalls and hardened grids can be necessary in selected places, but as a national primary strategy they create a dangerous illusion: that exposure can be preserved rather than reduced or absorbed. Worse, they fail discontinuously. A wall that is overtopped does not fail gracefully; it can concentrate loss.

Human-capital adaptation is more robust under uncertainty. Social housing for migrants, retraining, climate health coverage, school-based preparedness, and municipal adaptation funds work across multiple futures: higher sea-level rise, worse storms, crop failure, or slower-than-expected climate impacts. These investments are also politically durable because benefits are broad rather than confined to protected coastal asset owners.

The main vulnerability is that this strategy does not by itself stop physical damage. It can look soft while bridges, ports, and coastlines visibly deteriorate. To succeed, it must be paired with ruthless infrastructure triage in the baseline 30%: protect only assets of national importance, stop subsidizing new exposure, and communicate clearly that the goal is not to save every place, but to keep the country functioning as places change.

### M3 (frame: Q, model: `google/gemini-3.1-pro-preview`)

To optimize Expected Value (EV) under deep uncertainty, I strongly recommend **Option B: Managed retreat and relocation**. 

My epistemological baseline is strictly empirical: what is the data? Current observations demonstrate a persistent rightward shift in extreme weather distributions (an empirical 600% frequency increase from baseline). To manage this, Option B is the only mathematically sound strategy because it structurally zeroes out the exposure variable in our expected loss function, rather than marginally reducing vulnerability. The strategy is cleanly operationalizable: allocating 70% of the $25B annual budget yields $262.5B over 15 years. This funds the relocation of the 2.5 million median projected migrants at ~$105,000 per capita (95% Confidence Interval: $88,000–$121,000), permanently insulating these populations from compounding coastal shocks. 

The most plausible alternative, Option A (Hard infrastructure), presents an unacceptable probabilistic risk. Hard engineering relies on static design thresholds. If we build seawalls engineered for the 50cm sea-level rise upper-bound, and actual sea-level rise hits 55cm, the damage curve acts as a step-function to total, catastrophic failure. The downside variance of Option A is mathematically unbounded if extreme tail-risks are realized. (I discard Options C and E entirely; concepts like "social cohesion" or "ecosystem healing" represent non-falsifiable frameworks with outcomes that cannot be rigorously measured or operationalized. Show me the data on the verifiable, high-sigma storm-surge reduction of a restored wetland). 

The primary vulnerability of Option B lies in cost-variance scaling. Our $105k/capita expected cost assumes linear relocation dynamics. If inland land markets adjust dynamically to the state's buyout signals, property acquisition premiums could spike, blowing past the upper bound of our 95% CI and causing a budget shortfall before the 15-year horizon concludes. To mitigate this risk, the government must execute aggressive, immediate forward contracts on inland real estate to lock down baseline pricing and cap the variance of our future liabilities. Under measurable evidentiary standards, Option B is the only mathematically defensible mechanism for minimizing long-term expected loss.

### M4 (frame: S, model: `deepseek/deepseek-v4-pro`)

**Recommendation: Option E – Social cohesion and human capital first**

The primary leverage point in any climate adaptation system is not physical infrastructure or technological forecasting—it is the distribution of adaptive capacity across the population. Option E treats this directly, and it is the only strategy that addresses the fundamental constraint on all others: without a society that trusts its institutions, can relocate without fracturing, and possesses the health and skills to navigate recurrent disruption, every engineered solution collapses at its political or social seam.

Climate threats are systemic, compounding, and unevenly distributed. Sea walls (Option A) create moral hazard—they concentrate assets behind a single point of failure, amplifying fragility until a worse-than-projected event triggers cascading loss. Managed retreat (Option B) is, in isolation, the most obvious risk-reduction play, but it is politically explosive precisely because it demands a high-trust social fabric to implement. If you attempt retreat without first building that fabric, you get litigation, backlash, and stalled buy-outs, leaving communities stranded in hazard zones with diminished services. Option E invests in the substrate that makes retreat, and every other adaptation, feasible: universal climate health insurance, retraining, expanded social housing, community-led funds, and climate literacy. These are not soft measures—they are the preconditions for collective action under stress.

The strategy’s interlocking feedback loops are virtuous over the long horizon. A healthier, more mobile workforce absorbs agricultural decline and migration shocks without collapsing into grievance politics. Community-led adaptation funds decentralize learning, speeding up local responses that a central ministry could never architect. Climate education shifts the paradigm from “protect my house at all costs” to a resilient-systems mindset, reducing resistance to necessary retreats or land-use changes later. The 30% baseline preparedness budget can meanwhile handle near-term physical triage—emergency seawalls, early warning—while the 70% builds the adaptive muscle that allows the nation to adjust strategy as conditions evolve.

The main vulnerability is timing. If a severe hurricane or flood strikes before social programs are fully scaled, the immediate rescue-and-rebuild narrative may discredit the whole approach, triggering a political swing back to “fortress” infrastructure. Mitigation requires explicit framing from the outset: this is a resilience investment with a ten-year maturation curve, and it must be paired with a transparent communication strategy that treats early shocks as stress tests, not verdicts. But absent this investment, every other option is a brittle monument waiting for the water to rise.

### M5 (frame: E, model: `moonshotai/kimi-k2.6`)

 **Recommendation: Option C, Ecosystem-based adaptation.**

The binding constraint is fiscal and spatial: \$25 billion annually cannot construct and maintain engineered defenses along 4,500 kilometers of coastline without lethal gaps. From first principles, the actual mechanism of coastal damage is kinetic wave energy and storm-surge mass propagating inland; the most efficient, distributed dissipater of that energy is hydraulic roughness from mangroves, wetlands, and coastal forests, not concrete. Vegetation drag reduces wave amplitude exponentially in shallow water; wetlands provide retention storage that lowers peak discharge; soil microbiome management directly governs crop water-use efficiency and heat tolerance at the root interface. These are physical and biochemical mechanisms, not metaphors.

Hard infrastructure—the most plausible alternative—optimizes for political legibility, not physics. Seawalls reflect energy, accelerating downdrift erosion, and suffer unavoidable chloride-induced reinforcement corrosion in salt air. They lock the country into defending a static geography that the sea is already abandoning, and they leave inland watershed and agricultural pressures untouched.

Ecosystem-based adaptation is the only approach where the budget scales to the geometry of the problem. At roughly thirty percent the cost of concrete per kilometer, it can cover the long tail of exposure rather than fortifying political priorities while leaving the remainder bare.

The main vulnerability is maturation velocity. Biomass density and soil community establishment require years to achieve design-level wave attenuation, and the hurricane frequency is increasing now. The next five years carry an exposure gap that the reserve preparedness budget must cover while the living infrastructure reaches functional mass.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/D_P_run3/cell.json`.

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

**M1 (H):**
- the same error as A and D: treating the physical system as the patient when the patient is the society

**M2 (C):**
- spending the next 15 years defending yesterday’s settlement pattern

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
