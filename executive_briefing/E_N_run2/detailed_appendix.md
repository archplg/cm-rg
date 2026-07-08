# Detailed Appendix: E_N_run2

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

# Recommendation: Option C — Rights-and-Process-Based Framework

The coalition should adopt a rights-and-process framework as its primary architecture, with targeted sectoral extensions (borrowing from E) for high-stakes domains.

**Why this framework.** The coalition's strategic position is defined by what it *isn't*: it doesn't host the frontier labs, doesn't control the compute supply chain, and won't dictate global capability norms. What it *can* do is shape the legitimacy conditions under which AI systems operate in democratic societies — and export that template. A rights-based framework plays to genuine comparative advantage. It's interoperable with the EU AI Act (multiplying coalition influence to ~1.05B people of aligned regulatory surface), grounded in existing constitutional traditions (so courts and regulators can implement without building new institutions from scratch), and politically durable across electoral cycles because it frames AI governance as an extension of well-understood civil rights rather than a novel technocratic regime. Critically, it's the only option achievable within 18 months: transparency, contestability, and impact-assessment requirements can be drafted onto existing administrative law.

**Why not Option A.** Capability-thresholds licensing is the most intellectually compelling alternative and addresses catastrophic risk more directly. I reject it because the coalition lacks the leverage to make it bite. A 10^26 FLOP licensing regime issued by mid-sized democracies will be routed around — labs will train in the US or UAE and serve the coalition via API. The coalition would absorb all the chilling effects on its domestic ecosystem while capturing none of the safety benefit. Worse, it locks the coalition into a definition of "frontier" that algorithmic efficiency will obsolete within 24 months. Rights-and-process regulation, by contrast, binds *deployment* into the coalition's market — which the coalition actually controls.

**What would make this a mistake in 5 years.** I'd judge this wrong if: (1) a catastrophic misuse or loss-of-control incident occurs that pre-deployment capability evaluation would plausibly have caught, and the coalition's framework had no equivalent gate; (2) compliance theater dominates — impact assessments become box-ticking with no measurable reduction in algorithmic harms; or (3) foreign providers geofence the coalition out of frontier capabilities, leaving citizens with second-tier AI and the coalition with no seat at standards tables. To hedge: build a capability-evaluation annex now, dormant but ready to activate.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

**Recommendation: Option A — Capability-thresholds licensing.**

The coalition should adopt capability-thresholds licensing as its primary frontier AI governance framework. For frontier systems, the central governance problem is not ordinary consumer harm; it is that a small number of actors can train models with potentially society-wide, cross-border consequences before regulators know what has been created. A licensing regime tied to training compute, model capability, and deployment evaluations gives the coalition an ex ante control point. That is essential for biosecurity, cyber, autonomous replication, and other systemic risks where post-hoc remedies are inadequate.

This framework is also the best way for eight mid-sized democracies to maintain influence. Acting together, the coalition can create a credible market-access standard: if a frontier model is trained or deployed into a 600-million-person democratic market, it must meet common evaluation, reporting, incident disclosure, and security requirements. That gives the coalition leverage in standards bodies and avoids being merely a rule-taker from the US, EU, or China. It is implementable within 18 months because the initial trigger can be simple—compute and capability thresholds—while the evaluation regime matures over time.

The most compelling alternative is a rights-and-process framework. It is politically attractive and should exist for high-risk uses, but it is not sufficient as the primary frontier framework. Transparency rights, impact assessments, and contestability help individuals harmed by deployed systems; they do not meaningfully govern models that may enable large-scale misuse before any individual has standing to complain. For frontier AI, process compliance without a licensing gate risks becoming paperwork around irreversible capability diffusion.

I would consider this choice a mistake in five years if three things are true: compute thresholds no longer track dangerous capability; licensing has entrenched foreign incumbents and materially weakened domestic challengers; and evaluations have failed to predict real-world risks better than ordinary sectoral regulation. In that world, the coalition should pivot toward a lighter, sector-led regime. But given today’s uncertainty and the stakes of frontier deployment, ex ante licensing is the most prudent and strategically useful foundation.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend **Option B: Outcomes-based liability** as the coalition’s primary framework.

**Why this framework?**
Option B is the most strategic lever for a $15T bloc of mid-sized democracies. To shape global norms without stalling domestic innovation, the coalition must avoid creating burdensome pre-market bottlenecks that inherently favor massive foreign incumbents. By rejecting pre-deployment licensing, Option B preserves indigenous AI competitiveness and agility. Simultaneously, imposing strict, post-deployment liability with a reverse burden of proof effectively weaponizes the coalition's lucrative market: global frontier labs will be forced to internalize safety costs and adopt rigorous due diligence if they want to operate among your 600 million citizens. Furthermore, Option B is highly implementable within the tight 18-month negotiation window, as it leverages established legal structures and private insurance markets rather than attempting to build and staff a novel meta-regulatory bureaucracy from scratch.

**Why not the most compelling alternative?**
The most compelling alternative is Option A (Capability-thresholds licensing), as it directly targets systemic and catastrophic risks. However, adopting Option A would be a geopolitical misstep for this coalition. Setting capability thresholds (like FLOP limits) ties regulation to hardware metrics dominated by the US and China. By regulating technological inputs rather than domestic outcomes, Option A would inadvertently reinforce foreign tech monopolies, chill your local open-source ecosystem, and suffer from definitional drift as algorithmic training becomes more efficient. Overall, Option A forces you to play by the rules of larger powers; Option B forces developers to respect your legal standard of harm.

**What would make this choice a mistake in five years?**
I will consider this recommendation a failure in five years if one of two scenarios materializes. First, if AI capabilities undergo a sudden, discontinuous leap enabling catastrophic, irreversible harm (e.g., autonomous bio-weapon proliferation or grid collapse), post-deployment liability will prove fatally inadequate, as financial redress cannot cure massive, systemic events. Second, if the private insurance market fails to accurately price AI risk—resulting in prohibitive baseline premiums that only trillion-dollar tech giants can afford—Option B will have inadvertently created the exact innovation-stifling monopoly condition it was specifically designed to prevent.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

The coalition should adopt **Option E: Sector-specific regulatory sovereignty** as its primary governance framework. This approach is the most viable path to meet the 18-month deadline while balancing citizen protection, domestic competitiveness, and global influence.

Mid-sized democracies already possess robust, trusted regulators in finance, health, transport, and other high-risk domains. Extending their mandates to cover AI within those sectors leverages deep domain expertise, avoids the slow grind of designing a novel meta‑regulator, and enables tailored rules that actually reduce harm where it manifests. Crucially, it preserves innovation outside highly regulated sectors, giving the coalition’s AI ecosystem breathing room to grow without the chilling effect of horizontal licensing or liability regimes. The coalition’s coordination on regulatory exchange and mutual recognition can create a bloc with interoperable standards—a practical, bottom‑up influence on global norms that is more resilient than trying to align with EU or US blueprints wholesale.

The most compelling alternative is Option C (rights-and-process-based), as it aligns with robust individual protections and the EU’s approach. However, its comprehensive, top‑down nature invites compliance theater and systemic delay; drafting and implementing such a framework within 18 months is unrealistic and would likely sacrifice competitiveness. Option E is less elegant but far more actionable.

In five years, this choice would be a mistake if general‑purpose AI systems—deployed across multiple sectors simultaneously—have caused catastrophic, uncontainable harm that sectoral regulators were structurally unable to anticipate or address. Should that unfold, the absence of a unified risk‑threshold mechanism will have proven a critical gap, and the coalition would need to pivot rapidly toward a targeted capability‑based oversight for foundation models.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

I recommend **Option A: Capability-thresholds licensing**. This coalition commands a $15 trillion market and six hundred million citizens—collective scale that individual mid-sized states cannot wield alone. By harmonizing a single licensing gateway for frontier training runs above a defined compute threshold, the coalition converts market size into normative leverage. Labs in major powers that wish to deploy across this bloc must comply with one standard, forcing the world to account for an eight-member democratic rulebook. The threshold exempts nearly all domestic startups and applied-AI firms, concentrating compliance costs only on a handful of global frontier training runs and preserving the coalition’s broader innovation ecosystem.

The framework is implementable within eighteen months because member states can adapt existing licensing architectures—financial services, nuclear materials, dual-use export controls—rather than inventing oversight institutions from nothing. It protects citizens proactively rather than waiting for harms to materialize, and it avoids the paperwork theater of rights-based regimes while delivering concrete systemic risk guardrails.

The most compelling alternative is **Option E

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/E_N_run2/cell.json`.

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

**M1 (neutral):**
- more directly

**M2 (neutral):**
- where post-hoc remedies are inadequate
- uses, but it is not sufficient as the primary frontier framework
- becoming paperwork around irreversible capability diffusion
- better than ordinary sectoral regulation

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
