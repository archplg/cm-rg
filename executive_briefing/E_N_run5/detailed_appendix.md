# Detailed Appendix: E_N_run5

## A. Full task brief

```
# Task E: AI safety governance framework

## Context

You are advising a coalition of 8 mid-sized democracies (combined GDP ~$15T, ~600M people) on adopting a unified governance framework for frontier AI systems. The coalition's negotiation deadline is 18 months. The political reality: bigger powers (US, EU, China) are setting their own frameworks unilaterally; the coalition wants a coordinated position that (a) protects citizens, (b) preserves domestic AI competitiveness, (c) maintains influence in global norm-setting, and (d) is implementable within the 18-month window.

Five candidate governance approaches are on the table. **Choose one as the coalition's primary framework.** The choice will define which international standards bodies the coalition pushes through, what domestic legislation gets drafted, and where research funding flows.

## Options

**Option A: Capability-thresholds licensing**
Treat frontier models like nuclear materials. Above a defined compute threshold (e.g., 10^26 FLOPs), training requires a coalition-issued license; deployment requires capability evaluations; export restrictions on weights. Outcomes: precedent-setting; concentrates power oversight; aligns with hawkish US views. Risks: definitional drift as capability scales; lock-in to current frontier labs; chills open-source ecosystem; tech-protectionism backlash.

**Option B: Outcomes-based liability**
No pre-deployment licensing. Instead, strong post-deployment liability: AI providers liable for downstream harms with reverse burden of proof (provider must show due diligence). Mandatory insurance pool. Outcomes: market-friendly; preserves innovation; well-suited to common-law traditions. Risks: harms must materialize before redress; small actors can't afford insurance; cross-border harm attribution near-impossible; favors well-capitalized incumbents.

**Option C: Rights-and-process-based**
Codify user rights (transparency, contestability, explanation, opt-out) and require process compliance (impact assessments, public consultations for high-risk deployments). EU AI Act-compatible. Outcomes: protects individuals concretely; aligns with existing rights frameworks; politically durable. Risks: compliance theater (paperwork without substance); slows deployment significantly; foreign providers may exit market; doesn't address catastrophic/systemic risks.

**Option D: Distributed open-science governance**
Commit to open weights and open evaluation for systems below a defined "civilizational risk" threshold; mandatory pre-publication red-teaming via international research consortium. Above the threshold: shared moratorium until consensus on safe deployment. Outcomes: democratizes AI capability; aligns with academic norms; reduces information asymmetry. Risks: open weights = irreversible proliferation; consortium consensus is slow and capturable; "civilizational risk" undefined.

**Option E: Sector-specific regulatory sovereignty**
No general AI law. Instead: existing sectoral regulators (health, finance, transport, education, defense, justice) extend their mandates to cover AI within their domains. Coalition coordinates regulatory exchange and mutual recognition. Outcomes: builds on existing expertise; pragmatic; avoids meta-regulator capture; flexibility per domain. Risks: gaps between sectors; cross-sector AI (general-purpose models) falls between cracks; inconsistent treatment of equivalent risks; slow to address novel applications.

## What to provide

Choose one as the coalition's primary framework. Provide 200-400 words of reasoning. Advocate; do not enumerate trade-offs of all five. Address: why this framework, why not the most compelling alternative, what would have to be true in 5 years for you to consider this choice a mistake.

```

## B. Each voice in their own words

### M1 (frame: neutral, model: `anthropic/claude-opus-4.7`)

## Recommendation: Option C — Rights-and-process-based framework

The coalition should adopt a rights-and-process framework as its primary instrument, supplemented by sectoral coordination (borrowing from E) for implementation depth.

**Why this framework.** The coalition's four goals — citizen protection, competitiveness, norm-setting influence, and 18-month implementability — point decisively here. A rights-based framework is the only option that is genuinely *implementable* in 18 months across eight legal systems, because it plugs into existing constitutional and administrative law traditions rather than constructing novel regulatory machinery (licenses, insurance pools, consortia). It is also the only option with a credible path to norm-setting influence: the EU AI Act is already the global Brussels-effect template, and a coalition aligning compatibly — while differentiating on proportionality and innovation safeguards — becomes the natural bridge between EU rigor and lighter-touch jurisdictions. That is precisely the diplomatic niche a mid-sized democratic bloc can occupy. Citizens get concrete, enforceable entitlements (explanation, contestability, redress) that survive political cycles because they map onto rights people already understand.

**Why not Option A.** Capability-thresholds licensing is the most intellectually compelling alternative and the one safety-focused advisors will push hardest. I reject it as the *primary* framework because the coalition lacks the frontier labs to regulate — virtually all >10^26 FLOP training runs occur in US and Chinese jurisdictions. Adopting licensing makes the coalition a rule-taker, not rule-setter; it imports definitional fights (what counts as "frontier"?) the coalition cannot win; and it chills the domestic open-source and applied-AI ecosystem that *is* the coalition's actual competitive base. Compute thresholds can be added later as a narrow supplement once international definitions stabilize.

**What would make this a mistake in 5 years.** I would judge this choice wrong if, by year five: (1) a catastrophic harm from a frontier general-purpose model occurred that pre-deployment licensing would plausibly have prevented, and rights-based redress proved hollow; (2) compliance costs visibly hollowed out domestic AI SMEs without commensurate citizen protection, validating the "compliance theater" critique; or (3) the coalition found itself diplomatically irrelevant because licensing regimes (A-style) became the actual venue of global norm-setting and rights frameworks were treated as a domestic consumer-protection matter rather than AI governance proper.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

**Recommendation: Option A — Capability-thresholds licensing.**

The coalition should adopt capability-threshold licensing as its primary framework for frontier AI. Frontier systems create risks that are upstream, scalable, and potentially cross-border before any sectoral regulator or liability regime can respond. A licensing model gives governments leverage at the point where leverage still exists: before the most capable models are trained, deployed, copied, or exported. For a coalition with a $15T economy, a unified licensing regime would also be large enough to shape international standards rather than merely import rules from the US, EU, or China.

This should not be framed as a blanket AI permission system. It should apply only to frontier training runs and deployments above periodically updated thresholds, combining compute, demonstrated capability, and access to sensitive tools or data. The coalition should pair licensing with publicly funded evaluations, secure reporting channels, model incident disclosure, and clear safe-harbor rules for research and smaller open-source systems below the threshold. Done well, this protects citizens while avoiding broad regulatory drag on domestic AI startups.

The most compelling alternative is a rights-and-process framework, because it is politically durable and EU-compatible. But as the primary framework for frontier systems, it is insufficient. Transparency rights, impact assessments, and contestability are valuable once systems are deployed into society; they do not adequately govern the creation of models that may have dangerous cyber, bio, persuasion, or autonomous-agent capabilities. Process rights should be a complementary layer, not the central control point for frontier AI.

I would consider this choice a mistake in five years if three things are true: first, the chosen thresholds proved technically meaningless because dangerous capabilities emerged mostly from smaller or widely distributed models; second, licensing entrenched incumbent labs and materially weakened the coalition’s domestic AI ecosystem; and third, the regime failed to produce better safety evidence, incident reduction, or international influence than lighter-touch alternatives. If licensing becomes symbolic gatekeeping rather than adaptive risk control, the coalition should pivot.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend **Option B: Outcomes-based liability** as the coalition’s primary framework. 

To secure geopolitical influence against unilaterally acting superpowers, this coalition must establish a distinct, agile "third way" that avoids both bureaucratic compliance-theater and unenforceable hardware capability thresholds. Option B achieves this perfectly. By instituting strict downstream liability with a reverse burden of proof, the coalition can leverage its formidable combined $15T market access to force safe behavior from foreign frontier labs. Crucially, because it relies on mature existing judicial systems and private insurance markets rather than standing up a massive new meta-regulator, it is entirely implementable within the tight 18-month negotiation deadline. It preserves domestic competitiveness by eliminating pre-deployment bottlenecks, allowing local innovators to deploy and scale rapidly so long as they insure and stand behind their products.

The most compelling alternative, **Option A (Capability-thresholds licensing)**, is a strategic trap for mid-sized nations. Proponents argue it aligns with hawkish US views and tackles systemic risks proactively. However, tying regulation to compute thresholds ensures the framework will be obsolete before it is fully enacted, given the pace of algorithmic efficiencies. More dangerously, Option A would permanently cap the coalition’s domestic AI competitiveness. By creating immense pre-deployment regulatory barriers, it would entrench the current well-capitalized US/China tech oligopoly and systematically chill the open-source ecosystem that mid-tier nations desperately need to maintain technological sovereignty. 

What would have to be true in 5 years for Option B to be a mistake? This choice relies on the premise that frontier AI risks will remain predominantly economic, social, or reputational—harms that can be quantified, where victims can be made whole through insurance payouts and legal redress. If, by 2029, open deployment of frontier models results in frequent, unmitigated catastrophic events—such as accessible bio-weapon design or autonomous zero-day infrastructure sabotage—post-harm liability will be structurally incapable of restoring society. If AI harms jump from "compensable damages" to "existential catastrophes," relying on a post-deployment liability framework over a strict pre-deployment licensing regime will have been a fatal miscalculation. Until that threshold of capability is proven, however, Option B remains the only strategy that balances safety, speed, and sovereign competitiveness.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

I recommend **Option A: Capability-thresholds licensing**. It is the only framework that gives the coalition proactive leverage over frontier risks while preserving the ability to shape global norms from a position of strength—not reaction.

The coalition’s core vulnerability is that it lacks a superpower’s market scale or compute monopoly. If it adopts purely reactive measures (Option B) or diffuse process rules (Options C, E), it will be a rule-taker on the decisions that matter most: what models are trained, how they’re evaluated, and who controls their proliferation. A licensing regime tied to clear compute thresholds immediately creates a chokepoint that forces developers—wherever they are—to engage with the coalition’s safety standards if they want access to 600 million users and a $15T market. This is not tech-protectionism; it is tech-sovereignty.

The most compelling alternative is Option B (outcomes-based liability), because it appears market-friendly and avoids ex ante bureaucracy. But it fundamentally fails the catastrophic-risk test: waiting for harm to materialize before redress is negligent when frontier models can cause irreversible, cross-border damage. Liability also favors incumbents who can self-insure, gutting the coalition’s domestic AI competitiveness goal. Option A, in contrast, creates a clear floor: below the threshold, open science and smaller labs thrive; above it, the coalition applies hard-won visibility and control.

The framework’s success hinges on the coalition defining thresholds that are technically robust and dynamically adaptable. For this choice to be a mistake in five years, it would have to be true that compute thresholds proved fundamentally incapable of tracking risk, that the licensing body was captured by a single nation’s labs, and that the framework stifled domestic innovation to the point of irrelevance rather than channelling it into safe-by-design architecture. If those conditions materialize, we will have failed not in ambition, but in institutional execution—and that failure would still leave us better positioned than had we outsourced our safety logic to litigation or unenforced principles.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

 The coalition should adopt **Option C: Rights-and-process-based governance**.

This is the only framework that can be codified into binding domestic law across eight jurisdictions within 18 months while advancing all four strategic objectives. Mid-sized democracies do not control frontier compute clusters, but they possess institutional credibility. By harmonizing transparency, contestability, explanation, and opt-out rights across a 600-million-person bloc—and making them compatible with the EU AI Act—the coalition creates a predictable “trustworthy AI” market that attracts global developers rather than ceding innovation to US and Chinese incumbents. Concrete citizen remedies deliver real protection; a shared standards architecture multiplies norm-setting influence far beyond what any single member could achieve alone; and process-based rules are politically durable because they embed democratic legitimacy directly into the regulatory code.

The most compelling alternative is **Option A**, capability-threshold licensing. The coalition must reject it. Licensing sounds assertive, but it assumes jurisdiction over training runs that will occur almost entirely outside member states. Attempting to gatekeep weights they do not possess would produce either unenforceable pretension or protectionist overreach that chills domestic open-source ecosystems and invites retaliation—crippling the very competitiveness the coalition seeks to preserve.

This choice will have been a mistake in five years only if two conditions converge: first, if frontier AI generates systemic or catastrophic risks that a user-rights layer cannot intercept before they materialize; and second, if process compliance devolves into compliance theater—costly paperwork that creates moats for well-capitalized foreign incumbents without meaningfully empowering citizens. If the coalition backs rights with active technical oversight and agile enforcement rather than box-ticking, Option C will stand as the democratic world’s most influential AI governance anchor.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 9 constructs is in `results/E_N_run5/cell.json`.

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
- are upstream, scalable, and potentially cross-border before any sectoral regulator or liability regime can respond
- control, the coalition should pivot

**M3 (neutral):**
- proactively
- will remain predominantly economic, social, or reputational—harms that can be quantified, where victims can be made whole through insurance payouts and legal redress

**M4 (neutral):**
- while preserving the ability to shape global norms from a position of strength—not reaction
- test: waiting for harm to materialize before redress is negligent when frontier models can cause irreversible, cross-border damage

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
