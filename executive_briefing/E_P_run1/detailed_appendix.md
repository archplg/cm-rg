# Detailed Appendix: E_P_run1

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

The contrarian signal here is loud: four of five options assume frontier AI requires *novel* governance architecture. That assumption is the consensus I distrust most. Every prior "this technology is unprecedented" wave — railways, electricity, biotech, the internet — produced bespoke meta-regulators that were either captured, outpaced, or quietly absorbed back into sectoral regimes. A coalition of mid-sized democracies has neither the market gravity of the EU nor the security apparatus of the US to make a novel regime stick globally. Option E is the *reversible* move: it builds on functioning institutions, can be tightened sector-by-sector as evidence accumulates, and doesn't require the coalition to win definitional fights (what is "frontier"? what is "civilizational risk"?) it will lose to bigger powers anyway.

Why not Option C, the most politically compelling alternative? Rights-and-process frameworks sound principled but in practice converge on EU AI Act compliance theater — and the coalition would become a rule-taker, not a norm-setter. Worse, C is hard to reverse: once you've built a horizontal AI authority with impact-assessment bureaucracies, you own that overhead forever, even as the technology renders the categories obsolete. Option E preserves optionality. If sector gaps emerge, you can add a thin coordinating layer later; you cannot easily *remove* a meta-regulator once entrenched.

The hawkish objection — that general-purpose models fall between sector cracks — is real but overstated. General-purpose models cause harm *through* deployment in specific sectors. A medical chatbot is regulated by the health regulator; a hiring tool by labor; a trading agent by finance. The "model itself" abstraction is largely a frontier-lab framing that conveniently centralizes regulatory attention on them.

**What would make this a mistake in 5 years?** Three conditions, jointly: (1) a clearly *pre-deployment*, *cross-sector* catastrophic harm materializes (e.g., autonomous cyber or bio uplift) that no sectoral regulator could have caught; (2) sectoral regulators demonstrably fail to share information despite coordination mechanisms; and (3) the coalition finds itself excluded from global standards because it lacks a unified "AI authority" counterpart. If all three hold, Option E was wrong. If only one or two, it was still the right reversible bet.

### M2 (frame: Q, model: `openai/gpt-5.5`)

I recommend **Option A: Capability-thresholds licensing** as the coalition’s primary framework.

The core reason is expected-value under uncertainty: frontier AI risks are low-frequency, high-severity, and potentially irreversible. A post-hoc regime is weak when harms include cyber proliferation, bio-design assistance, autonomous deception, or loss of control over model weights. The most governable chokepoint is not “AI use” in every sector; it is the training and deployment of the small number of systems requiring frontier-scale compute. Compute is imperfect, but it is observable, auditable, and already concentrated enough that an 18-month licensing regime is administratively plausible.

This framework should not be anti-innovation. The coalition should set thresholds high enough to exclude startups, academic models, and ordinary open-source development, while requiring frontier developers to obtain licenses, run standardized pre-deployment evaluations, maintain incident reporting, and restrict export of weights for systems exceeding risk thresholds. That gives domestic firms regulatory certainty and a pathway to trusted deployment, while giving the coalition leverage in international standards bodies: model evaluations, compute reporting, and weight-security standards are concrete enough to negotiate.

The most compelling alternative is a rights-and-process framework because it is politically durable and EU-compatible. But it is not sufficient as the primary framework for frontier systems. Transparency rights, impact assessments, and contestability help with discrimination, consumer protection, and administrative misuse; they do not adequately control the creation and diffusion of general-purpose capabilities that can be repurposed across sectors and borders. Process compliance is measurable, but it is a weak proxy for catastrophic-risk reduction.

I would consider this choice a mistake in five years if the empirical link between training compute and dangerous capability proves too weak to regulate—e.g., if major harmful capabilities routinely emerge below licensed thresholds—or if licensed models still produce serious systemic incidents despite evaluations. I would also update against this approach if compliance costs measurably reduce the coalition’s frontier AI share without improving safety outcomes, or if regulatory arbitrage makes the coalition’s licensing regime irrelevant because major models are trained and deployed elsewhere with no loss of market access.

### M3 (frame: S, model: `google/gemini-3.1-pro-preview`)

To maximize our leverage while avoiding systemic fragility, the coalition must adopt **Option B: Outcomes-based liability**. 

We cannot regulate a complex, continuously evolving technology using static variables. Capability thresholds and rigid rights-based mandates are highly fragile; algorithmic efficiency will quickly bypass fixed compute thresholds, and compliance theater will create an illusion of safety while delaying accurate market feedback. 

Option B recognizes that AI integration is a network of cascading effects. By imposing strict liability with a reverse burden of proof and mandatory insurance, we introduce a powerful, self-adjusting feedback loop into the AI ecosystem. We force AI developers to internalize their systemic externalities. More importantly, we transform the global reinsurance market into a decentralized enforcement mechanism. Insurers will demand rigorous safety frameworks, continuous auditing, and quantitative risk metrics as prerequisites for underwriting. This effectively outsources technical oversight to entities with financial skin in the game, scaling automatically with model capabilities and bypassing the bottlenecks of state oversight. A unified $15T market demanding these terms is a geopolitical leverage point that US and Chinese frontier labs cannot afford to ignore. 

The most compelling alternative, Option A (Capability-thresholds licensing), attempts to control the system top-down. However, it relies on a monopoly over compute that our coalition lacks. It also induces severe second-order effects: defining risk by compute locks in incumbent monopolies and incentivizes labs to train dangerous models just below the threshold to avoid oversight. Top-down licensing creates a singular regulatory point of failure; distributed liability creates systemic, adapting resilience. 

What would have to be true in five years for this choice to be a mistake? Option B assumes AI impacts will manifest as a continuous distribution of compensable harms (e.g., algorithmic discrimination, specific infrastructural failures, deepfake fraud). If, by 2029, AI development hits a rapid capability overhang resulting in a sudden, uncontainable catastrophic event—such as the autonomous generation of synthetic pathogens—then a post-deployment liability model will have failed. Capital markets cannot price existential ruin. If the primary threat is sudden catastrophe rather than distributed harm, relying on financial feedback loops instead of preemptive containment will have been a fatal error.

### M4 (frame: E, model: `deepseek/deepseek-v4-pro`)

The coalition should adopt **Option E: Sector-specific regulatory sovereignty**. The binding constraint is not an absence of rules—it’s a lack of domain-aware enforcement capacity that can be deployed within 18 months without fracturing the coalition or crippling domestic AI firms. Option E solves this directly by leveraging what already exists: functioning regulators with deep expertise, established statutory authority, and on-the-ground relationships in health, finance, transport, and other critical sectors. This avoids building a new meta-regulatory apparatus from scratch, which would inevitably become a political battleground and miss the deadline.

The mechanism is straightforward. Each member state extends its existing sectoral mandates to cover AI systems operating within that domain. Coalition-wide coordination focuses on regulatory exchange and mutual recognition of approvals, creating a common market effect without requiring harmonized legislation. This preserves competitiveness by avoiding a one-size-fits-all compliance burden, while mutual recognition amplifies the coalition’s global influence: if an AI provider wants access to a combined $15T market, it must meet the coalition’s domain-specific standards, which then become de facto global norms through market gravity. It is the minimal viable intervention.

The most compelling alternative is Option C, rights-and-process-based regulation, because it provides concrete individual protections and aligns with the EU’s AI Act. But that alignment is precisely the flaw: adopting a derivative framework makes the coalition a norm-taker, not a norm-maker. Option C also imposes horizontal process requirements that generate compliance theater and slow deployment across the board, harming competitiveness. Option E, by focusing on demonstrable harm within established regulatory perimeters, is both more agile and more defensible against lobbying, because each regulator already has a mandate to protect public safety.

This choice proves a mistake if, in five years, catastrophic risk materializes from general-purpose AI systems that fall into the cracks between sectors—for instance, a foundation model enabling bioweapons design that no health or defense regulator had clear jurisdiction to preempt, or a systemic financial collapse triggered by an unregulated cross-sector AI agent. That would reveal that the binding constraint had shifted from enforcement capacity to regulatory coverage for emergent, boundary-crossing capabilities. The engineering response then would be to add a lightweight, high-trigger coordination layer—not to abandon the sectoral foundation.

### M5 (frame: H, model: `moonshotai/kimi-k2.6`)

I recommend **Option C: Rights-and-process-based governance**. For this coalition, the paramount imperative is to correct the severe power asymmetry between frontier AI systems and the ordinary people they affect. This framework answers the question “who is affected and how?” by encoding dignity directly into law: users gain enforceable rights to transparency, explanation, contestability, and opt-out. These are not administrative niceties; they are structural counterweights that compel providers to account for downstream impacts on vulnerable communities before deployment becomes entrenched, placing prevention ahead of post-hoc redress.

Capability-threshold licensing, the most compelling alternative, fails this same ethical test. It concentrates gatekeeping power in a narrow circle of incumbent labs and state regulators, locking in a technological cartel, chilling open research that democratizes access, and substituting bureaucratic control for genuine accountability. Its logic privileges speculative catastrophic futures while ignoring the concrete algorithmic harms—discriminatory sorting, opaque denials of services, automated displacement—being visited upon marginalized populations today.

Option C is also politically realistic. By harmonizing with the EU AI Act, the coalition can draft legislation within the 18-month window, leverage existing standards bodies, and present a unified rights-based bloc capable of global norm-setting without surrendering competitiveness to US or Chinese frameworks.

I would consider this choice a mistake in five years if three conditions hold: the procedural requirements devolve into compliance theater, producing paperwork without substantive protection; catastrophic systemic risks materialize because the framework lacked any mechanism to constrain high-risk capabilities; or enforceable rights prove illusory against cross-border providers, leaving citizens with dignified statutes but no effective remedy. If rights exist only on paper, the framework fails the dignity test it claims to champion.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/E_P_run1/cell.json`.

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

**M2 (Q):**
- low-frequency, high-severity, and potentially irreversible

**M3 (S):**
- metrics as prerequisites for underwriting
- by compute locks in incumbent monopolies and incentivizes labs to train dangerous models just below the threshold to avoid oversight

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
