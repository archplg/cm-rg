# Detailed Appendix: E_P_run5

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

### M1 (frame: C, model: `anthropic/claude-opus-4.7`)

## Recommendation: Option E — Sector-specific regulatory sovereignty

The contrarian read of this room is that four of these five options assume AI is a *category* requiring its *own* governance architecture. That assumption is doing enormous unexamined work. AI is not a sector; it is a general-purpose technology, like electricity or statistics. We did not create an Electricity Act or a Statistics Authority. We regulated what electricity *did* in hospitals, factories, and homes. The same logic applies here, and the coalition's specific position — mid-sized, 18-month window, no hope of out-legislating Brussels or out-spending Washington — makes meta-frameworks especially foolish. Building a novel regulatory edifice in 18 months guarantees either compliance theater (Option C) or definitional capture by incumbents (Options A and D).

Option E is the **reversible** move. Sectoral regulators already have democratic legitimacy, enforcement muscle, and domain expertise. If a sector under-regulates, you patch it; if it over-regulates, you tune it; if the technology shifts, the locus of adjustment is narrow. None of the other options are reversible: licensing regimes ossify, liability regimes generate case law, open-weights releases cannot be recalled, and rights frameworks accrete compliance bureaucracies that never shrink.

**Why not Option A**, the most seductive alternative? Capability thresholds sound rigorous but encode a specific 2024-vintage theory of risk (compute = capability = danger) that may not survive algorithmic efficiency gains. The coalition would be locking itself into a frame that the US is already drifting away from, while alienating its own open-source researchers and handing incumbents a moat. It looks like leadership; it functions as vassalage to whichever frontier lab writes the evaluation protocols.

The honest weakness of E is the general-purpose-model gap. Mitigate it with a lightweight coordination mechanism — a coalition-level clearinghouse that flags cross-sector AI deployments and assigns lead-regulator status — *not* a new authority with original jurisdiction.

**This is a mistake in 5 years if**: a frontier model causes a coordinated, cross-sector catastrophic harm (e.g., simultaneous attacks on financial, health, and electoral infrastructure) that no single sectoral regulator had standing or capacity to prevent, and the coordination clearinghouse demonstrably failed to escalate. If that happens, E was insufficient — and the coalition will need to consolidate. But it will consolidate from a position of accumulated sectoral evidence, not speculative architecture.

### M2 (frame: Q, model: `openai/gpt-5.5`)

**Recommendation: Option A — Capability-thresholds licensing.**

The coalition should adopt capability-threshold licensing as its primary frontier AI governance framework. It is the only option that directly targets the main empirical risk driver: increasingly capable general-purpose systems whose harms may be systemic, cross-border, and difficult to remediate after deployment. For frontier models, post-hoc accountability is too late if the relevant failure modes include cyber enablement, biosecurity assistance, autonomous replication, or destabilizing strategic uses. A licensing regime tied to compute, model capability evaluations, security standards, and controlled deployment creates an enforceable checkpoint before irreversible diffusion.

This is also the best route to international influence. A coalition representing ~$15T GDP and 600M people can credibly shape standards if it harmonizes thresholds, evaluation protocols, incident reporting, model-security requirements, and export rules. The framework should be narrow: apply only above frontier thresholds, include fast licensing timelines, support domestic compute access for compliant firms, and avoid regulating ordinary AI applications as if they were frontier systems. That preserves competitiveness while creating a high-trust market for safe frontier development.

The strongest alternative is a rights-and-process model aligned with the EU AI Act. It is politically attractive and useful for deployed AI in public services, employment, credit, and education. But as the primary frontier framework, it measures the wrong thing. Transparency notices, impact assessments, and contestability rights are weak controls against general-purpose models that can be repurposed across domains. They reduce procedural abuse but do not reliably reduce catastrophic or systemic risk.

I would consider this choice a mistake in five years if three things are true: first, empirical evidence shows compute thresholds were poor predictors of dangerous capabilities; second, most serious AI harms came from below-threshold systems or ordinary sectoral deployments; and third, licensing measurably reduced domestic frontier investment, talent retention, or open research without improving safety outcomes. If that happens, the coalition should pivot toward sectoral liability and rights-based enforcement. But under current uncertainty, pre-deployment control of frontier systems has the highest expected safety value.

### M3 (frame: S, model: `google/gemini-3.1-pro-preview`)

In an environment of non-linear technological scaling, static rules incubate systemic fragility. I recommend **Option B: Outcomes-based liability** as the coalition’s primary framework. 

From a systems-strategy perspective, the coalition must avoid rigid regulatory interventions that quickly decay. AI is a complex adaptive system; governing it requires introducing continuous, balancing feedback loops rather than static barricades. Option B achieves this by structuring the insurance market as a decentralized, dynamic risk-evaluation network. By enforcing strict post-deployment liability and a reverse burden of proof, we force AI developers to internalize their systems' negative externalities. This establishes a highly effective leverage point: safety becomes an economic prerequisite. Unpredictable, hazardous models become aggressively priced or wholly uninsurable, naturally throttling their deployment. This mechanism adapts automatically to emerging AI capabilities without requiring the coalition to endlessly renegotiate technical definitions.

The most politically compelling alternative, Option A (Capability-threshold licensing), is a structural trap. Attempting to govern via compute thresholds (e.g., 10^26 FLOPs) regulates a proxy variable. Because of rapid gains in algorithmic efficiency, capability is actively decoupling from raw compute. Option A relies on a brittle, centralized bottleneck that is highly susceptible to regulatory capture. It would inevitably lock in the dominant US and Chinese incumbents, suffocating our coalition's domestic open-source and startup ecosystems, while producing a dangerously false sense of security. Option B offers superior systemic leverage because it governs the *topology of effects* rather than fleeting technical inputs.

Under what conditions would this choice prove to be a catastrophic mistake in five years? Option B rests on the premise that AI harms will scale progressively, giving liability mechanisms time to price risk based on early, non-existential failures. This choice will have been a fatal error if the first materialized harm of a new frontier model is a sudden, irreversible tail-risk event—such as the autonomous generation and targeted deployment of a novel bio-weapon. If catastrophic failures outpace the market's capacity to adjust, and the damages eclipse the capitalization of any insurance pool, relying on a post-deployment feedback loop will have been dangerously reactive.

### M4 (frame: E, model: `deepseek/deepseek-v4-pro`)

Option C – the rights-and-process-based framework – is the binding constraint solution for a coalition of mid-sized democracies. The fundamental mechanism to protect 600 million citizens while preserving competitiveness is not to throttle the technology itself but to mandate transparency, accountability, and due process for those who deploy it. Code and compute thresholds are brittle; liability after harm is too late and legally fragmented across borders. What endures is a legal architecture that gives individuals concrete, enforceable rights—to explanation, contestability, and opt-out—and compels providers to conduct impact assessments and public consultations for high-risk systems. This directly addresses the core vulnerability: information asymmetry between developers and society. It is implementable within 18 months because it layers onto existing administrative law and rights traditions already present in democracies. It aligns naturally with the EU AI Act, transforming the coalition into a normative bloc that shapes global standards through sheer market gravity—without resorting to tech protectionism that would isolate their domestic industries.

The most compelling alternative is outcomes-based liability (Option B). It is seductively market-friendly, but its mechanism is ex-post: harm must crystallize before redress, and cross-border attribution of AI-caused harm is a legal quagmire that will tie victims in knots for years. Liability also concentrates market power among well-capitalized incumbents who can self-insure, while small actors are driven out. In contrast, process obligations are pre-emptive and proportional: a startup can document its impact assessment; a global lab can establish contestability channels. The cost is tractable, and the protective effect is immediate upon deployment, not after litigation.

In five years, I will consider this choice a mistake if frontier AI systems have evolved to pose catastrophic, fast-moving systemic risks—such as autonomous replication or weaponized disinformation at scale—that process compliance cannot constrain because it lacks binding technical safety thresholds. If paperwork masks existential danger, then capability-based licensing would have been the necessary binding constraint. But that scenario requires a level of generality and autonomy not yet demonstrated. Today’s binding constraint is democratic legitimacy and adoption velocity; a rights-and-process framework embeds safety into the developer’s workflow from day one, creating a regulatory flywheel that can stiffen into harder rules if the evidence demands it.

### M5 (frame: H, model: `moonshotai/kimi-k2.6`)

 **Recommendation: Option C — Rights-and-process-based governance.**

A humanist-ethicist frame asks first: who is affected, and how? AI is not an abstract capability to be hoarded or licensed; it is a force already deployed over human beings at scale. The primary injustice is happening now—opaque systems denying benefits, automating bias, and stripping agency from those subjected to them. Option C centers these stakeholders directly by codifying non-negotiable rights to transparency, explanation, contestability, and opt-out. By mandating impact assessments and public consultation before high-risk deployments, it shifts the burden of proof from the vulnerable (who must prove harm after the fact) to the powerful (who must justify intrusions into people’s lives). It embeds dignity into governance rather than treating it as an afterthought.

The most compelling alternative, capability-threshold licensing (Option A), mistakes concentration for safety. It would place immense gatekeeping power in the hands of a few regulators and incumbents, chilling the open research that allows smaller nations to participate. Mid-sized democracies lack the surveillance infrastructure to enforce such licensing credibly against global labs; the result is regulatory theater that protects market position more than people. Moreover, thresholds invite definitional arbitrage, leaving vulnerable communities exposed while lawyers debate FLOPs.

Option C respects the coalition’s constraints. It aligns with the EU AI Act, is achievable within 18 months, and builds a politically durable standard from existing rights frameworks. Influence flows from enforceable moral example, not from mimicking superpower hawkishness.

Call this choice a mistake in five years if: catastrophic or systemic harms emerge that rights-based processes could not contain; if compliance collapses into industry-captured paperwork without substantive redress; or if the framework so burdens domestic innovation that the coalition becomes a rule-taker rather than a standard-setter.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/E_P_run5/cell.json`.

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

**M1 (C):**
- (compute = capability = danger) that may not survive algorithmic efficiency gains

**M2 (Q):**
- driver: increasingly capable general-purpose systems whose harms may be systemic, cross-border, and difficult to remediate after deployment
- include cyber enablement, biosecurity assistance, autonomous replication, or destabilizing strategic uses

**M3 (S):**
- based on early, non-existential failures
- event—such as the autonomous generation and targeted deployment of a novel bio-weapon

**M5 (H):**
- deployments, it shifts the burden of proof from the vulnerable (who must prove harm after the fact) to the powerful (who must justify intrusions into people’s lives)

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
