# Detailed Appendix: E_P_run3

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

The contrarian signal here is loud. Options A, C, and D all carry the perfume of consensus among AI-policy intellectuals: "frontier models are categorically novel, therefore require categorically novel governance." That premise is the hidden assumption worth attacking. Frontier capability claims are made by the labs that profit from them; "civilizational risk" thresholds are speculative; compute thresholds are gameable and will be obsolete within the 18-month implementation window itself. Building a coalition framework atop contested technical predictions is a bet on forecasters who have repeatedly missed.

Option E is the most reversible move. Sectoral regulators already have democratic legitimacy, domain expertise, enforcement machinery, and case law. Harms from AI in radiology, lending, hiring, and autonomous vehicles are *not* novel harms — they are old harms with new vectors. Existing regulators can act in months; a new meta-regulator (Options A, C) needs years to staff, define terms, and survive its first court challenge. The coalition's 18-month deadline functionally rules out anything else being real rather than performative.

**Why not Option A**, the most intellectually compelling alternative? Capability-thresholds licensing concentrates oversight precisely where the coalition has *least* leverage: it locks the coalition into chasing US/China definitions of "frontier," cedes norm-setting to whoever controls the compute metric, and entrenches three or four incumbent labs as the only legal trainers. For a mid-power coalition, this is strategic suicide dressed as seriousness. It trades real domestic regulatory capacity for a symbolic seat at a table the big powers already own.

Option E's weakness — cross-sector general-purpose models falling between cracks — is real but addressable through a thin coordinating layer (a coalition AI council with referral powers, not licensing powers). Start thin; thicken if evidence demands.

**What would make this a mistake by year five?** If (1) a genuinely general-purpose model causes coordinated cross-sector harm that no sectoral regulator could have anticipated or contained; (2) sectoral regulators demonstrably fail to share information, producing arbitrage; or (3) the coalition's competitiveness erodes because firms face *more* fragmented compliance than under a unified regime. If two of these three occur, Option E was wrong, and — crucially — it leaves the door open to adopt A or C later. The other options do not leave that door open.

### M2 (frame: Q, model: `openai/gpt-5.5`)

**Recommendation: Option A — capability-threshold licensing.**

The coalition should adopt capability-threshold licensing as its primary frontier AI governance framework, with dynamic thresholds tied to training compute, model capability evaluations, and controlled deployment of model weights. This is the best fit for the problem class: frontier AI risks are concentrated in a small number of high-cost training runs, run by a small number of labs and cloud providers, making pre-deployment oversight feasible within 18 months. Unlike broad process regulation, this gives governments a measurable intervention point: compute used, model capability, security practices, red-team results, and deployment conditions.

The expected-value case is straightforward. Even if catastrophic misuse or loss-of-control risks are low-probability, they are high-consequence and potentially irreversible once powerful model weights proliferate. Post-hoc remedies are weak where attribution is hard and harms cross borders. Licensing does not need to cover all AI; it should focus narrowly on frontier systems above quantitative thresholds and require evidence of safety testing, cybersecurity, incident reporting, and controlled release.

The most compelling alternative is rights-and-process regulation, especially because it aligns with the EU AI Act and is politically legible. But it is not sufficient as the primary framework for frontier systems. Transparency rights, impact assessments, and contestability mechanisms help citizens harmed by deployed systems, but they do little against systemic risks from highly capable general-purpose models. They also risk measuring paperwork rather than risk reduction. The coalition can still borrow rights-based protections downstream, but the primary framework should govern the creation and release of the most capable models.

I would consider this choice a mistake in five years if three things are true: first, compute and benchmark thresholds prove poorly correlated with dangerous capabilities; second, licensing measurably entrenches incumbents and reduces domestic frontier AI formation without reducing major incidents; and third, open or lightly regulated ecosystems demonstrably produce equal or better safety outcomes, measured by incident rates, misuse cases, model security failures, and independent evaluation results. Until that evidence exists, the prudent choice is targeted pre-deployment control over the small number of systems with the largest downside risk.

### M3 (frame: S, model: `google/gemini-3.1-pro-preview`)

For a coalition aiming to maximize leverage and avoid systemic fragility, the optimal intervention is **Option B: Outcomes-based liability**. 

From a systems-strategy perspective, AI governance requires adaptive feedback loops, not static tripwires. Attempting to govern frontier AI via rigid capability thresholds (Option A) is systemically fragile. Compute thresholds (FLOPs) focus on upstream inputs rather than downstream impacts, creating a brittle paradigm that algorithmic efficiency will quickly bypass. Furthermore, Option A inevitably induces regulatory capture, centralizing power into a single gatekeeper and locking out domestic challengers without tangibly reducing systemic risk. 

Option B acts as a decentralized leverage point. By enforcing strict liability with a reverse burden of proof, we force AI developers to mathematically internalize the systemic externalities of their outputs. Rather than relying on a slow-moving, capturable state bureaucracy to define "safe," Option B deputizes a globally distributed sensing mechanism: the mandatory insurance market. Underwriters, driven by financial preservation, will continuously update their safety evaluations dynamically as AI capabilities scale. This creates a continuous, market-driven feedback loop that demands *provable* safety from developers. Importantly, this framework can be legislated within the 18-month window by adapting existing product liability doctrines (a natural fit for the coalition’s common-law structures), cleanly sidestepping the regulatory bloat of EU-style approaches. It also preserves the coalition's global leverage by making access to a $15T market contingent on financial accountability, effectively exporting our norms globally without needing to out-compute the US or China.

What would have to be true in five years for this choice to be a mistake? This framework hypothesizes that financial liability is a sufficient deterrent to unsafe behavior. I would consider Option B a failure if "ruin" dynamics emerge—specifically, if a frontier model initiates a sudden, irreversible systemic shock (e.g., democratized bioterrorism or critical infrastructure collapse) where the compounding damage outstrips the entire capitalization of the insurance pool. If post-deployment harms prove to be uninsurable and unrecoverable, then retroactive liability will have failed as a stabilizing force against catastrophic phase shifts.

### M4 (frame: E, model: `deepseek/deepseek-v4-pro`)

The coalition’s binding constraint is preventing irreversible catastrophic harm from frontier AI without ceding competitive advantage or requiring superpower-level enforcement. The only framework that directly addresses the mechanism of harm is **Option A: capability-thresholds licensing**. It inserts a hard ex ante gate—compute—before training or deployment, the minimal efficient intervention to control tail risk.

Compute is the fundamental choke point for frontier models. It is measurable, verifiable, and tightly correlated with potential capability, making a licensing threshold (e.g., 10²⁶ FLOPs) a low-ambiguity trigger. This avoids the definitional slipperiness of “high-risk” or “civilizational harm” that plagues other options. By requiring a coalition-issued license for any system above that threshold trained or deployed within their jurisdictions, the coalition leverages its combined $15T market as a de facto regulatory union. Labs seeking access to 600 million citizens will comply, giving the coalition outsized norm-setting influence despite its mid-sized members—exactly as the GDPR did for privacy.

The most compelling alternative, rights-and-process frameworks (Option C), only addresses individual, atomized harms. It treats AI as a consumer product with transparency obligations, but it cannot handle systemic or catastrophic risks that manifest discontinuously. Liability regimes (Option B) are similarly reactive: compensation after a disaster doesn’t prevent it, and providers may be judgment-proof against truly existential damage. By contrast, licensing forces a safety case before exposure, which is the engineering approach to high-consequence systems.

This framework is implementable within 18 months: the compute threshold can be adopted from existing frontier-lab training disclosures, and a joint licensing body can be stood up through a coalition treaty rather than a bespoke mega-regulator. Domestic legislation simply codifies the licensing requirement and the evaluation mandate.

This choice would prove a mistake only if, within five years, algorithmic breakthroughs decouple dangerous capability from compute scale, allowing catastrophic systems to emerge below the threshold while open-source development atrophies under the licensing regime. In that world, we would have imposed a costly gate on a fading proxy, stifling distributed innovation without containing the real risk. But the current scaling paradigm makes that an unlikely near-term bet—and the coalition can adapt the threshold if the evidence shifts. The priority is to stop the most dangerous models before they are deployed, not to perfect a regime for all time.

### M5 (frame: H, model: `moonshotai/kimi-k2.6`)

 The coalition should adopt **Option C: Rights-and-process-based governance**.

The governing question must be: who is affected, and how? For the 600 million people across these democracies, AI is not an abstract capability score; it is a benefits algorithm that denies disability claims, a hiring tool that screens out ethnic names, a credit system that hardwires historical exclusion. Option C centers dignity by giving individuals enforceable rights—transparency, explanation, contestability, opt-out—and mandates public participation before high-risk deployment. It redistributes power from vendors and bureaucrats toward the vulnerable people who live with the outcomes.

This is also strategically sound for mid-sized states. It builds on existing administrative-law traditions instead of inventing a new licensing priesthood from scratch, making it achievable in 18 months. By harmonising with the EU AI Act, the coalition gains bloc leverage in global standards bodies without caving to US or Chinese unilateralism.

The most compelling alternative, Option A’s capability-threshold licensing, fails the dignity test. It treats citizens as passive subjects of frontier-lab gatekeepers and concentrates oversight in the hands of the same wealthy incumbents and great powers that already own the compute supply chain. Mid-sized democracies would become rule-takers, not norm-shapers.

I would regard this choice as a mistake in five years if: the impact assessments have become expensive paperwork theatre that shields incumbents while smaller domestic actors drown in compliance; if foreign frontier labs have simply routed processing outside coalition jurisdiction, hollowing out protection; or if a systemic, cross-sector catastrophic risk—such as a widely disseminated biological design tool or automated mass manipulation—materialises that a rights-based process could neither foresee nor contain.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/E_P_run3/cell.json`.

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
- concentrated in a small number of high-cost training runs, run by a small number of labs and cloud providers, making pre-deployment oversight feasible within 18 months
- low-probability, they are high-consequence and potentially irreversible once powerful model weights proliferate
- from highly capable general-purpose models
- measuring paperwork rather than risk reduction

**M4 (E):**
- manifest discontinuously

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
