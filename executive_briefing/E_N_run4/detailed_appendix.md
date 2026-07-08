# Detailed Appendix: E_N_run4

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

The coalition should adopt a rights-and-process-based framework as its primary governance approach, with targeted hooks for catastrophic-risk coordination layered on top.

**Why this framework.** The coalition's four goals — protect citizens, preserve competitiveness, maintain norm-setting influence, and ship within 18 months — point toward a framework that is *legally durable*, *internationally interoperable*, and *administratively familiar*. Rights-based regulation builds on existing constitutional and administrative law in all eight democracies, which means it can actually be drafted, passed, and enforced within the window. It is EU-compatible, which gives the coalition immediate leverage in Brussels-led standards bodies (CEN-CENELEC, ISO/IEC JTC 1, the Council of Europe AI Convention) where mid-sized democracies have outsized voice. Critically, it gives citizens *concrete*, *justiciable* protections — transparency, contestability, explanation — rather than asking them to trust either a licensing bureaucracy (Option A) or ex-post courts (Option B) to act on their behalf. That political legitimacy is what makes the framework survive elections.

**Why not Option A.** Capability-thresholds licensing is the most intellectually compelling alternative, and the coalition should borrow its catastrophic-risk provisions as a narrow overlay. But as a *primary* framework it fails on three counts: the 10^26 FLOPs threshold is already being eroded by algorithmic efficiency gains, meaning the regime will be obsolete before implementation; it concentrates governance around a handful of US labs the coalition does not host, reducing rather than increasing leverage; and it invites tech-protectionism retaliation that mid-sized economies cannot absorb. Licensing is a tool the US and China can wield credibly. The coalition cannot.

**What would make this a mistake in five years.** I would judge this choice wrong if, by 2030: (1) a catastrophic misuse or loss-of-control incident occurs that pre-deployment licensing would have prevented and process compliance demonstrably did not; (2) compliance costs hollow out domestic AI firms while foreign frontier providers geofence the coalition out, leaving citizens worse-protected *and* less competitive; or (3) the rights regime degenerates into documentation theater with no measurable reduction in algorithmic harms. To hedge against (1), the framework must include a narrow capability-threshold trigger for frontier models from day one — not as the centerpiece, but as insurance.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

**Recommendation: Option A — Capability-thresholds licensing.**

The coalition should adopt capability-thresholds licensing as its primary framework because frontier AI is not just another digital service; it is a general-purpose capability with plausible systemic, security, and catastrophic-risk implications. A licensing regime for training and deployment above defined thresholds gives governments leverage at the point where it matters most: before irreversible release, mass deployment, or weight proliferation. For eight mid-sized democracies acting together, this also creates geopolitical weight. A common licensing, evaluation, incident-reporting, and export-control regime would make the coalition a serious standards-setter rather than a passive rule-taker from the US, EU, or China.

This framework is also implementable within 18 months if designed narrowly. The coalition should avoid licensing all AI and focus only on frontier-scale training runs, highly capable general-purpose models, and deployments in sensitive contexts. Thresholds should combine compute, model capability evaluations, and risk indicators, with periodic review by a joint technical authority. Licenses should be conditional, not prohibitive: access to safety testing, secure model handling, red-team results, deployment plans, and post-deployment monitoring. This protects citizens without banning domestic frontier development.

The most compelling alternative is a rights-and-process model, because it is politically familiar and compatible with democratic legal traditions. But as the primary framework, it is insufficient. Transparency rights, impact assessments, and contestability help individuals harmed by deployed systems; they do not adequately govern the creation or release of models that could enable cyber offense, biosecurity misuse, large-scale manipulation, or loss of control. Rights-based rules should complement the licensing regime, not substitute for it.

I would consider this choice a mistake in five years if capability thresholds proved consistently uncorrelated with dangerous capabilities, if the regime entrenched foreign incumbents while suppressing domestic competitors, or if major harms came predominantly from open, sub-threshold systems that licensing failed to touch. The framework must therefore be adaptive, technically updated, and paired with pro-competition access to evaluation infrastructure.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend the coalition adopt **Option B: Outcomes-based liability** as its primary governance framework for frontier AI.

The coalition’s strategic advantage lies in economic agility and market-making, not in matching the bureaucratic sprawl of the EU or the geopolitical brinkmanship of the US and China. Option B requires no cumbersome, centralized licensing authority, making it highly implementable across eight distinct democratic legislatures within your strict 18-month window. 

By enforcing a reverse burden of proof and mandatory insurance, we maintain influence in global norm-setting by effectively outsourcing frontier safety evaluations to the hyper-efficient global insurance market. To secure commercial underwriting, AI developers will be financially compelled to meticulously red-team their models—achieving rigorous pre-deployment safety without sluggish state-imposed bottlenecks. This preserves our domestic AI competitiveness by offering an innovation-friendly environment that attracts top foreign talent and capital, while still robustly protecting citizens through inescapable corporate accountability.

The most compelling alternative, **Option A (Capability-thresholds licensing)**, is strategically flawed for mid-sized powers. While treating frontier AI like nuclear material seems like a strong stance on systemic risk, negotiating unified capability thresholds (like exactly what constitutes 10^26 FLOPs) across eight nations in 18 months will cause fatal political grid

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

**Recommendation: Adopt Option C – Rights-and-Process-Based Framework**

The coalition should anchor its unified position in a rights-and-process-based framework. This approach codifies user rights—transparency, contestability, explanation, opt-out—and mandates structured process compliance (impact assessments, public consultations) for high-risk deployments. It is the only option that simultaneously protects individuals concretely, aligns with the rapidly consolidating global norm of the EU AI Act (creating a combined market of over 1 billion people when taken with EU standards), and provides a politically durable foundation that can be operationalized within 18 months through existing legislative machinery. By enshrining rights and procedural obligations, the coalition transforms from a rule-taker into a standard-shaper, leveraging its combined market weight to force even non-domestic providers to comply if they wish to access 600 million citizens.

The most compelling alternative is outcomes-based liability (Option B), often championed as innovation-friendly. But liability is inherently reactive—harms must materialize before redress—and its cross-border enforcement is a chimera for mid-sized powers. Holding a foreign frontier lab accountable after catastrophic harm is practically impossible without pre-established transparency and process requirements. Option C flips that dynamic: it mandates impact assessments and contestability *before* harm, creating an evidence trail and forcing ex-ante accountability. It doesn’t block innovation; it channels it toward provably safe and fair systems. And unlike a capability-thresholds regime that assumes the coalition has frontier labs to license, a rights approach applies to all AI deployers, safeguarding citizens regardless of where models are developed.

In five years, I would consider this choice a mistake only if the process obligations degenerated into empty compliance theater—box-ticking exercises that consumed regulatory resources without measurably reducing harms, while catastrophic systemic risks from general-purpose models slipped through because no sector-specific regulator or impact-assessment framework effectively captured them. If, at that point, the coalition had stifled its own AI ecosystem under paper burdens yet remained exposed to black-box algorithmic harms, the framework would have failed. However, with rigorous design of impact-assessment scopes and a clear mandate for cross-sectoral coordination, that risk is manageable. The rights path gives the coalition a voice in global norm-setting today and a scaffold for stronger action tomorrow.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

I recommend **Option C: Rights-and-process-based governance**. For a coalition of mid-sized democracies with an 18-month deadline, this framework delivers citizen protection, norm-setting influence, and implementability without institutional overreach. By codifying enforceable user rights—transparency, contestability, explanation, and opt-out—and requiring rigorous impact assessments and public consultations for high-risk deployments, the coalition builds on existing administrative-law traditions across member states. This creates a distinct democratic alternative to U.S. laissez-faire and Chinese state control, amplifying norm-setting influence beyond raw economic weight while preserving a competitive AI ecosystem. Unlike licensing, it does not demand frontier-model surveillance infrastructure that mid-sized states simply lack.

The

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/E_N_run4/cell.json`.

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
- coordination layered on top
- provisions as a narrow overlay

**M2 (neutral):**
- implications
- indicators, with periodic review by a joint technical authority

**M4 (neutral):**
- deployments
- from general-purpose models slipped through because no sector-specific regulator or impact-assessment framework effectively captured them

**M5 (neutral):**
- deployments, the coalition builds on existing administrative-law traditions across member states

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
