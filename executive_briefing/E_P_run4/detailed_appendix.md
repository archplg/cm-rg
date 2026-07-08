# Detailed Appendix: E_P_run4

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

The contrarian signal here is loud: A, C, and D all assume the coalition can meaningfully define "frontier," "high-risk," or "civilizational risk" in legislative text that will survive 18 months of drafting and five years of capability scaling. That assumption is almost certainly wrong. Every horizontal AI framework written to date has been obsolete on arrival because the object being regulated is moving faster than the regulators defining it. Option E refuses that trap.

Sectoral regulators already possess two things a new meta-regulator cannot manufacture in 18 months: domain expertise and enforcement muscle. A medical device regulator knows what "harm" means in oncology triage; a financial regulator knows what "manipulation" means in credit scoring. They have inspectors, case law, and political legitimacy. Layering a general AI act on top duplicates effort and invites capture by whichever frontier lab writes the best compliance template — exactly what happened with the EU AI Act's GPAI annex.

E is also the **most reversible** choice, which matters when uncertainty is this high. If sectoral coverage proves inadequate, the coalition can bolt on horizontal elements later (a liability layer from B, rights provisions from C). The reverse — repealing a licensing regime once incumbents have organized around it — is politically near-impossible. A and D create lock-in; E preserves option value.

**Why not C, the most compelling alternative?** C is seductive because it sounds principled and EU-compatible. But "EU-compatible" is precisely the trap: the coalition would become a rule-taker, not a norm-setter, contradicting goal (c). Worse, rights-and-process frameworks tend to ossify into compliance theater that burdens domestic startups while large foreign providers absorb the cost as a market-entry tax. C protects citizens on paper and hollows out competitiveness in practice.

**What would make E a mistake in 5 years?** Three conditions, jointly: (1) a genuinely general-purpose system causes significant cross-sector harm that no single regulator had standing to prevent; (2) sectoral regulators demonstrably failed to share information through the coordination mechanism; and (3) the coalition's voice in global standards bodies shrank rather than grew because it lacked a flagship "AI Act" to point to. If all three hold, E was wrong and a horizontal layer was needed earlier. I'd accept that bet — because the failure modes of A, C, and D over the same five years look worse and are harder to unwind.

### M2 (frame: Q, model: `openai/gpt-5.5`)

Recommend **Option A: capability-threshold licensing** as the coalition’s primary framework.

For frontier AI, the governance problem is not mainly ordinary consumer protection; it is low-frequency, high-severity risk under uncertainty. The empirically relevant fact is that frontier capability is currently concentrated in a small number of actors, and training compute, model access, and deployment channels are measurable enough to regulate within 18 months. A licensing regime above a defined threshold—paired with mandatory evaluations, incident reporting, cybersecurity standards, and controlled export of model weights—gives the coalition a credible, legible position in global standard-setting. It also protects competitiveness better than it appears: most domestic AI firms will operate below the frontier threshold, while those above it get a predictable compliance pathway rather than fragmented national rules.

The most compelling alternative is a rights-and-process framework, because it is politically durable and EU-compatible. But it is insufficient as the primary framework for frontier systems. Process rights help when harms are individualized, observable, and contestable. They are weak against systemic misuse, autonomous cyber capability, biosecurity-relevant outputs, model theft, or cascading economic disruption. Impact assessments can be useful, but without a hard gate for frontier training and deployment they risk becoming auditable paperwork after the dangerous capability already exists.

The coalition should implement Option A narrowly: license only genuinely frontier training runs; update thresholds every 6–12 months using compute, capability benchmarks, and expert audits; exempt ordinary research and most open-source activity below threshold; and create mutual recognition so firms face one coalition-wide process.

I would consider this choice a mistake in five years if three conditions hold: first, dangerous capabilities routinely emerge below the licensed threshold; second, measured compliance costs substantially reduce domestic AI investment or frontier participation relative to peer economies; and third, observed AI harms are overwhelmingly sectoral and rights-based rather than frontier-model-driven. If that evidence appears, the expected value would shift toward a sectoral or rights-process regime. But given current uncertainty and tail-risk asymmetry, a narrow frontier licensing framework is the most defensible primary choice.

### M3 (frame: S, model: `google/gemini-3.1-pro-preview`)

To govern a complex adaptive system undergoing exponential change, regulations must be dynamic, not static. The coalition must adopt **Option B (Outcomes-based liability)**. 

To exert influence, our mid-sized coalition must leverage its primary asset: a $15T unified market. Option B is a structural intervention that functions as an adaptive, second-order feedback loop. By establishing strict liability with a reverse burden of proof and mandatory insurance, we do not need to predict the exact shape of future AI failures or define arbitrary risk categories. Instead, we outsource the epistemology of risk to distributed actuarial networks. Insurance markets will act as decentralized safety auditors, continuously pricing risk as capabilities evolve. To access our 600-million-citizen market, US and Chinese labs will be forced to internalize their safety externalities, building provable alignment into their systems. This avoids single points of regulatory failure and ensures the rules scale automatically with the technology.

Why not the most compelling alternative, Option A (Capability licensing)? Option A relies on static thresholds in a dynamic system—a recipe for extreme policy fragility. Algorithmic efficiencies will inevitably decouple capabilities from raw FLOPs, turning today's strict definitions into tomorrow's loopholes. Furthermore, licensing mechanisms are highly vulnerable to regulatory capture by well-capitalized incumbents who will weaponize compliance to pull up the ladder. Lastly, the US and China control the silicon and data-center supply chains; our coalition lacks the physical leverage to effectively string-pull a compute-based regime. 

For Option B to be definitively proven a mistake in five years, two systemic failures would need to occur. First, the emergence of *instantaneous uninsurable ruin*—a scenario where the very first materialized harm from a deployed model is so globally catastrophic (e.g., autonomous bio-weapon synthesis) that a post-deployment economic feedback loop arrives too late to halt systemic collapse. Second, the successful exploitation of cross-jurisdictional shell architecture by foreign providers, effectively nullifying the liability penalties and stripping the framework of its deterrence power before the international community could close the loopholes.

### M4 (frame: E, model: `deepseek/deepseek-v4-pro`)

**Recommendation: Option A — Capability-Thresholds Licensing**

The binding constraint is *control over the frontier*, not refinement of downstream liability, not sectoral adaptation, not normative alignment with existing rights frameworks. Frontier AI is a dual-use general-purpose technology. Its risk profile is not incremental; it is epistemic — the systems exhibit emergent capabilities we cannot predict ex ante. The mechanism that matters is the *training run*. Everything downstream is derivative.

Licensing at the compute threshold is the only approach that directly intervenes at the causal bottleneck. Without controlling the point of creation, you are left chasing consequences through courts (Option B), documenting impacts you cannot forecast (Option C), or hoping that openness does not produce catastrophe before consensus (Option D). Post-hoc liability does not prevent irreversible proliferation; it prices it. The coalition is not large enough to absorb the externalities of a capability jump from an unlicensed actor.

The most compelling alternative is Option B, not because it is sufficient, but because it is politically lightweight. It avoids the appearance of pre-market intervention and defers to judicial mechanisms that coalition members already possess. But its mechanism is *compensation for harm after the fact*, which is structurally incapable of addressing systemic or catastrophic risk. A liability-only regime assumes the distribution of harms is observable, attributable, and compensable. For frontier models with recursive self-improvement potential, that assumption fails.

Why this, now: The coalition comprises mid-sized economies with concentrated technical capacity and limited unilateral leverage. Acting in concert with a licensing regime creates a credible regulatory zone that labs must navigate — not because of market size, but because of precedent. The coalition becomes a standard-setter for what constitutes legitimate frontier development, forcing larger powers to interoperate or isolate.

Five-year falsification condition: This choice would be a mistake if the compute threshold becomes decoupled from actual capability — that is, if algorithmic efficiency improvements render the FLOP trigger irrelevant, creating a world where dangerous systems fall below the licensing floor while the regulatory apparatus entrenches compliance costs on an obsolete metric. If that occurs, the framework becomes protectionist theater rather than risk governance. The coalition must condition its commitment on continuous threshold recalibration tied to *demonstrated capability*, not static compute budgets.

### M5 (frame: H, model: `moonshotai/kimi-k2.6`)

 I recommend **Option C: a rights-and-process-based framework** as the coalition’s primary position. This choice begins from the right question: *who is affected and how?* The answer is six hundred million ordinary people confronting algorithmic scoring in welfare offices, diagnostic engines in clinics, and surveillance in public space. Codifying enforceable rights—to transparency, explanation, contestability, and human opt-out—places vulnerable parties at the center of governance. It dignifies the individual as an active rights-holder, not a passive risk-exposure unit, and leverages the coalition’s existing democratic and judicial infrastructure rather than inaugurating an opaque licensing priesthood.

The most compelling alternative is **Option A**, capability-threshold licensing. I reject it because its distributional consequences fall hardest on the least powerful: smaller domestic labs, open-source researchers, and Global South adopters are locked out, while incumbent frontier developers capture the regulatory moat. Licensing answers “who governs?” with “those who already own the compute,” concentrating life-shaping power in unelected boards and foreign-headquartered labs and offering citizens no concrete redress for everyday algorithmic harm.

I would consider Option C a failure in five years if three conditions held: first, catastrophic or systemic harms—such as automated bioweapon design, critical infrastructure sabotage, or irreversible democratic manipulation—materialized from models that rights-based impact assessments failed to intercept; second, coalition regulators proved unable to enforce cross-border due process, reducing rights to paperwork theater; and third, the coalition’s global normative influence collapsed because major powers dismissed process rights as commercially irrelevant. If rights protected neither daily dignity nor collective survival, the framework will have failed its moral warrant.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/E_P_run4/cell.json`.

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
- of A, C, and D over the same five years look worse and are harder to unwind

**M2 (Q):**
- under uncertainty
- becoming auditable paperwork after the dangerous capability already exists
- asymmetry, a narrow frontier licensing framework is the most defensible primary choice

**M3 (S):**
- to distributed actuarial networks
- as capabilities evolve

**M4 (E):**
- profile is not incremental; it is epistemic — the systems exhibit emergent capabilities we cannot predict ex ante

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
