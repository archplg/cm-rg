# Detailed Appendix: D_P_run4

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

**Who is affected, and how?** Every strategy here ultimately routes through people: the fisher whose coast erodes, the smallholder whose yields collapse, the child in a school that becomes a hurricane shelter, the 2-3 million who will move whether we plan for them or not. The decisive question is not what we build but whether the population arrives at 2040 with the capacities — health, skills, housing, trust, local agency — to survive what is coming. Option E is the only strategy that treats this as the central problem rather than a downstream effect.

**Why this, concretely.** Climate migration on the projected scale (4-6% of the population) will either be absorbed by functioning institutions or it will produce informal settlements, labor exploitation, political backlash against migrants, and a generation of children whose schooling and health collapse mid-transition. Universal climate health insurance, municipal adaptation funds, social housing pipelines, and worker retraining are not "soft" measures — they are the load-bearing infrastructure for a society undergoing demographic reorganization. They also distribute decision-making to municipalities, which know their own vulnerabilities better than any ministry. The 30% baseline preparedness budget still funds essential hard defenses around the densest at-risk areas; Option E complements rather than replaces engineering.

**Why not Option B (managed retreat),** the most serious alternative. Retreat is probably necessary in places, but as a *primary* strategy it inverts the moral order: it treats displacement as a policy lever before building the social fabric that makes displacement survivable with dignity. Forced or incentivized relocation without prior investment in receiving communities, portable benefits, and cultural continuity reliably produces immiseration — we have decades of evidence from dam projects, urban renewal, and prior climate relocations. Retreat should be an *instrument* of Option E's framework, not its substitute.

**Main vulnerability.** Physical assets will degrade visibly while Option E's benefits accrue invisibly in avoided suffering and preserved social trust. A single catastrophic hurricane during years 3-7 could be framed as policy failure ("they spent on schools while the port flooded"), creating pressure to abandon the strategy before it matures. Mitigating this requires a clear public narrative, transparent metrics on adaptive capacity, and disciplined use of the 30% baseline for the most legible physical risks.

### M2 (frame: C, model: `openai/gpt-5.5`)

**Recommendation: Option E — Social cohesion and human capital first.**

The primary adaptation strategy should treat people, not assets, as the core infrastructure of the country. Over the next 15 years, the most destabilizing climate impact is unlikely to be a single failed seawall; it will be the cumulative social shock of displaced households, unaffordable housing, job loss in exposed regions, climate-related illness, and declining trust in government. A country of 50 million facing 2–3 million internal migrants cannot “engineer” its way out if receiving cities, labor markets, schools, and health systems are unprepared.

This strategy is also the most robust under uncertainty. Sea-level rise may be 30 cm or 50 cm; storms may cluster unpredictably; crop losses may be worse or unevenly distributed. But in every scenario, a healthier, better-trained, better-housed, more mobile population adapts faster. Social housing for relocation zones, portable benefits, retraining, climate health coverage, and municipal adaptation funds create optionality. They do not overcommit the country to defending every existing settlement, nor do they require betting that a specific technology or barrier design will be sufficient.

The most plausible alternative is hard infrastructure-first. It is politically attractive because it is visible, concrete, and reassuring. But that is precisely the danger: it can create a false sense of security and lock the country into defending yesterday’s geography at tomorrow’s prices. Seawalls protect assets until they fail, are overtopped, or shift risk elsewhere. They should be used selectively through the baseline 30% preparedness budget for ports, power, hospitals, and dense urban cores—not as the national organizing principle.

The main vulnerability of a human-capital-first strategy is that it can look intangible or insufficiently “climate-specific.” If citizens see money spent on housing, schools, clinics, and retraining while floods continue, political support may erode. To counter that, the program must be tied to transparent climate-risk maps, relocation targets, and measurable resilience indicators. The aim is not to avoid all damage; it is to ensure the country remains governable, mobile, and cohesive as the map changes.

### M3 (frame: Q, model: `google/gemini-3.1-pro-preview`)

I recommend **Option B: Managed retreat and relocation** as the primary strategy. 

Our fundamental optimization problem is to minimize expected climate damages—defined as **Probability of Event × Asset Exposure**—under a strict $17.5B/year constraint (70% of the $25B budget). Option B is the only strategy that structurally reduces the exposure variable to zero in the highest-risk zones. 

What is the data? Relocating 3 million people over 15 years requires moving 200,000 people annually. At our $17.5B allocation, this yields a budget of $87,500 per capita per year. This is highly operationalizable to fund buyouts and inland infrastructure. By physically eliminating exposure for 6% of the population, Option B mathematically bounds our future downside. The expected value (EV) of avoided continuous reconstruction costs—especially given the observed 500% baseline increase in hurricane frequency—clearly yields a positive net present value (NPV) over the 15-year horizon.

We must reject the most plausible alternative, **Option A (Hard infrastructure)**, because it fails basic quantitative feasibility and operates poorly under uncertainty. At conservative global averages of $15M per kilometer for seawalls, hardening even half of our 4,500 km coastline immediately exhausts the budget. Furthermore, hard infrastructure scales poorly against fat-tailed distributions. Current 95% confidence intervals (CI) for sea-level rise contain severe upper-bound risks. If water levels exceed engineered tolerances, seawalls suffer binary failure (overtopping), reducing the protective value to zero and resulting in unmitigated catastrophic loss to the assets "protected" behind them. 

The primary vulnerability of Option B is the lack of empirical data for pricing relocation friction. The strategy requires standardizing subjective, non-market values (e.g., social resistance, heritage) into falsifiable financial models. If political friction causes actual per-capita buyout costs to exceed our $87,500/year CI bounds, the strategy risks fiscal overrun before achieving critical mass. To mitigate this, we must enforce strictly operationalized, non-negotiable valuation matrices for real estate buyouts based solely on historical market data, ignoring subjective premium demands.

### M4 (frame: S, model: `deepseek/deepseek-v4-pro`)

**Recommendation: Option E — Social Cohesion and Human Capital First**

Climate adaptation is not fundamentally a problem of coastlines, crops, or infrastructure; it is a problem of systemic fragility in the human systems that must navigate compounding shocks. Option E addresses the deepest leverage point: the adaptive capacity of the population itself. By investing in universal climate health insurance, retraining, social housing, education, and community-led funds, we build a society that can absorb disruptions and reorganize—regardless of whether the next shock is a hurricane, a supply chain collapse, or a technology failure. This strategy creates a positive feedback loop: increased social trust and human capital lower the costs of every other response, from disaster recovery to innovation adoption. It also avoids the moral hazard and lock-in that hard infrastructure creates, and unlike managed retreat, it strengthens political consent rather than eroding it.

The most plausible alternative—and the one with the greatest superficial appeal—is Option A, hard infrastructure. Seawalls and grids offer visible certainty and political wins. But they are a brittle fix that increases long-term systemic risk. They encourage continued development in vulnerable zones, concentrating assets behind defenses that can be overtopped by events worse than projected. When (not if) they fail, the losses are catastrophic. Option A solves a first-order problem while breeding second-order fragility.

Option E’s main vulnerability is that it does not directly build physical protection against acute events. A major hurricane in year three could still devastate a dense coastal city, and critics will cry “inaction.” However, this vulnerability is mitigated in two ways. First, the 30% baseline preparedness budget persists, covering essential early warning, emergency response, and natural buffer maintenance. Second, community-led adaptation funds (a pillar of Option E) empower municipalities to deploy local, context-appropriate measures—often cheaper and more flexible than centralized mega-projects. The real danger is not a lack of concrete, but a loss of public trust if visible defenses are absent. To counter this, the government must aggressively reframe the narrative: strength is a resilient populace, not a wall.

### M5 (frame: E, model: `moonshotai/kimi-k2.5`)

**Choose Option B: Managed Retreat and Relocation**

The binding constraint is not capital, but geophysics: you cannot engineer 4,500 km of coastline against 30–50 cm of sea-level rise coupled with tripling hurricane frequency for $25B/year. Hard infrastructure (Option A) fails first-principles arithmetic. Seawalls cost $20–50M per km; defending even 20% of the coastline consumes the entire 15-year budget before accounting for maintenance or storm overtopping. When a Category 5 hurricane generates 5-meter surges, engineered defenses become catastrophic liabilities—concentrating assets behind walls that breach, rather than dispersing risk.

The actual mechanism of climate harm here is *exposure*: fixed capital and populations occupying increasingly untenable hydrology. The efficient solution reduces exposure directly. Relocating 2–3 million people and abandoning the most vulnerable coastal zones aligns the country’s geography with its future climate, rather than freezing it in place with concrete. It transforms unplanned, chaotic migration (which will happen regardless when insurance markets retreat and hurricanes strike) into a capital-efficient, planned transition. The fiscal math favors buyouts and inland greenfield development over perpetual maintenance of sinking coastal assets.

The most plausible alternative, Option A, is seductive because it appears technically straightforward, but it commits the country to a capital-intensive war against thermodynamics that cannot be won within the budget envelope. It also locks in the current spatial distribution of the economy, which is maladaptive under rising sea levels.

**Main vulnerability:** Execution velocity. Retreat must outpace stochastic extreme weather. If a major hurricane strikes before high-risk zones are depopulated, the state bears both the cost of relocation *and* emergency disaster response for assets it already wrote off. Mitigation requires immediate no-build zoning in highest-risk areas and rapid monetization of abandoned land (e.g., carbon-sequestration easements) to defuse political resistance from property interests.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 8 constructs is in `results/D_P_run4/cell.json`.

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
- as; Option E complements rather than replaces engineering

**M2 (C):**
- maps, relocation targets, and measurable resilience indicators

**M3 (Q):**
- fiscal overrun before achieving critical mass

**M4 (S):**
- is not a lack of concrete, but a loss of public trust if visible defenses are absent

**M5 (E):**
- zones are depopulated, the state bears both the cost of relocation *and* emergency disaster response for assets it already wrote off
- as and rapid monetization of abandoned land (e

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
