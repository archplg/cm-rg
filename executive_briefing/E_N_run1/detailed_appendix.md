# Detailed Appendix: E_N_run1

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

# Recommendation: Option C (Rights-and-Process-Based), with explicit sectoral hooks

The coalition should adopt a rights-and-process-based framework as its primary stance. Three reasons drive this choice.

First, **implementability within 18 months**. Eight mid-sized democracies already share constitutional rights traditions, administrative law machinery, and (for many) EU AI Act alignment. Drafting from this foundation is feasible; drafting bespoke compute-licensing regimes or international red-teaming consortia is not. The coalition needs a framework that actually exists in 18 months, not an elegant one that exists in 60.

Second, **strategic positioning**. The coalition cannot out-hawk the US or out-scale China. Its comparative advantage in global norm-setting is democratic legitimacy. A rights-based framework is exportable to the Global South, interoperable with the EU (amplifying influence in Brussels-led standards bodies like CEN-CENELEC and ISO/IEC JTC 1/SC 42), and harder for incumbents to dismiss than liability rules they'll simply price in. It gives the coalition a distinctive voice rather than a junior-partner echo.

Third, **citizen protection is concrete**. Transparency, contestability, and impact assessments deliver tangible benefits to the 600M people regardless of whether catastrophic AI risks materialize on the predicted timeline. The coalition does not have to bet on a contested risk model.

**Why not Option A?** Capability-thresholds licensing is the most intellectually compelling alternative and addresses risks C cannot. But it requires enforcement infrastructure (compute monitoring, weight-export controls, evaluation labs) that mid-sized democracies cannot stand up unilaterally in 18 months. Adopting it makes the coalition a rule-taker from US licensing decisions while inheriting all the protectionism backlash. Better to let larger powers bear that cost and layer compute-threshold provisions onto C later as a targeted high-risk category.

**To mitigate C's known weaknesses**, the framework should explicitly delegate sector-specific implementation to existing regulators (borrowing from E) and include a sunset-review clause forcing reassessment at 36 months.

**This is a mistake in 5 years if**: (a) a frontier model causes a catastrophic incident that capability-licensing would plausibly have prevented, and the coalition's process-based regime is exposed as paperwork; (b) compliance costs drive domestic AI labs to relocate to laxer jurisdictions, hollowing out competitiveness; or (c) the EU diverges sharply, leaving the coalition aligned with a framework it no longer co-owns.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

**Recommendation: Option A — Capability-thresholds licensing.**

The coalition should adopt capability-thresholds licensing as its primary frontier AI governance framework. Frontier AI is not just another digital service: the distinctive risk is that a small number of highly capable models can create cross-border, systemic harms before ordinary legal remedies or sectoral rules can respond. A licensing regime for training and deployment above clear compute/capability thresholds is the only option that directly governs the point at which irreversible risk is created.

This is also the best route to international influence. The US, EU, and China are already moving toward frontier-model oversight in different ways; a coalition representing 600M people and $15T GDP can become the “third bloc” that turns ad hoc national rules into interoperable standards: common evaluation protocols, incident reporting, model-weight security, red-team requirements, and reciprocal recognition of licenses. That is more strategically valuable than merely copying existing rights or sectoral frameworks.

Competitiveness concerns are real, but manageable. The framework should be narrow: no licensing for ordinary AI, startups, academic research, or models below the frontier threshold. The coalition should fund shared evaluation infrastructure, subsidized compliance support, and public testbeds so domestic firms are not locked out. The goal is not to freeze development; it is to ensure that the most powerful systems are trained and deployed under auditable safety conditions.

The most compelling alternative is a rights-and-process framework. It is politically attractive and EU-compatible, but it is insufficient as the primary framework for frontier systems. Transparency, explanation, contestability, and impact assessments protect individuals in many ordinary AI use cases; they do not adequately address model theft, autonomous cyber capability, biosecurity misuse, or loss-of-control risks. For frontier AI, process rights should supplement licensing, not replace it.

I would consider this choice a mistake in five years if thresholds proved technically meaningless, licensing became incumbent protection, domestic frontier research migrated offshore, and no plausible systemic-risk reduction was achieved. If that happens, the coalition should pivot toward lighter, liability- and sector-based governance. But given present uncertainty and the asymmetric downside of frontier failures, licensing is the prudent primary framework.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I recommend the coalition adopt **Option B: Outcomes-based liability**. 

Given the strict 18-month negotiation window, the coalition lacks the time to construct a massive, centralized regulatory apparatus. Option B elegantly circumvents this by leveraging the speed and adaptability of existing legal traditions and private insurance markets. Imposing strict liability with a reverse burden of proof forces AI developers to internalize safety costs. If providers know they will pay for downstream harms unless they can meticulously prove their due diligence, they will organically implement rigorous pre-deployment red-teaming. This aligns private profit incentives with public safety. Crucially, by avoiding pre-deployment licensing, the coalition becomes a highly attractive jurisdiction for agile builders fleeing the EU’s regulatory sprawl or the US’s monopolistic landscape, thereby safeguarding your domestic AI competitiveness.

The most compelling alternative is Option A (Capability-thresholds licensing), as it directly addresses catastrophic risks and aligns with the rhetoric of larger powers. However, adopting Option A would be a strategic trap for mid-sized democracies. Defining governance by computing power fundamentally favors the incumbents—predominantly massive US and Chinese tech conglomerates—who already dominate that infrastructure. Regulating by compute thresholds inevitably leads to regulatory capture, locking your domestic startup sector out of the frontier ecosystem. Option B focuses on holding actors accountable for *impacts* rather than gatekeeping *inputs*, preserving a level playing field. 

In five years, I would consider this recommendation a mistake if one of two scenarios materializes. First, if an irreversible, catastrophic harm occurs (such as AI-facilitated biological terrorism) where post-hoc financial redress is fundamentally meaningless, proving that liability is an insufficient deterrent for existential-scale risks. Second, if the private insurance market completely fails to underwrite frontier models due to unquantifiable risk profiles, leading to exorbitant premiums that lock out domestic startups—inverting our goal and creating the exact barrier to entry Option B was chosen to avoid.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

**Recommendation: Option C – Rights-and-process-based governance**

The coalition should adopt a rights-and-process framework as its primary governance model. This approach codifies enforceable individual rights (transparency, contestability, explanation, opt-out) and mandates structured accountability for high-risk deployments through impact assessments and public consultations. It is the only option that simultaneously protects citizens in a tangible, politically durable manner *and* positions the coalition as an influential global norm-shaper, directly addressing the coalition’s core ambitions.

This framework is implementable within 18 months because it builds on well-established legal traditions and existing legislative templates, most notably the EU AI Act. By closely aligning with the EU’s approach, the coalition can rapidly draft coherent domestic laws, create a formidable transatlantic regulatory bloc of over 1 billion people, and resist being passively rule-taken by larger powers. It preserves domestic competitiveness not by shielding incumbents, but by forcing a race to the top on trustworthiness—a selling point for responsible AI developers—without resorting to protectionist export controls or innovation-chilling licensing.

The most compelling alternative, Option B (outcomes-based liability), is seductively market-friendly but critically flawed: it allows catastrophic or systemic harms to manifest before any redress is possible. With frontier AI, the first materialized harm could be devastating and irreversible. A rights-and-process model, by contrast, embeds precaution *prior* to deployment through mandatory impact assessments, public input, and contestability mechanisms, catching risks before they cause damage.

For this choice to be a mistake in five years, two conditions would need to hold. First, compliance must have degenerated into pure theatre—where process requirements generate paperwork but no real safety improvement, stifling innovation without protecting citizens. Second, a major systemic risk event (e.g., an uncontrollable model release) would need to occur that ex-ante capability thresholds or coordinated moratoria (Options A/D) could plausibly have prevented, revealing the framework’s blind spot for catastrophic, rather than individual, harms. The coalition must therefore actively invest in rigorous oversight capacity and pair this framework with international cooperation on systemic risk evaluation to ensure that today’s pragmatic, rights-preserving choice does not become tomorrow’s brittle failure.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

I recommend **Option A: Capability-thresholds licensing** as the coalition’s primary framework.

With a combined GDP of ~$15 trillion and 600 million people, this coalition commands sufficient market power to constitute a distinct regulatory pole—rather than accepting terms set unilaterally by Washington, Brussels, or Beijing. Capability-threshold licensing converts that market scale into strategic leverage. By requiring a coalition-issued license for training runs above a defined compute threshold and mandating capability evaluations before deployment, the bloc creates a single, predictable gateway that foreign frontier labs must traverse. This harmonization reduces compliance fragmentation across the eight members, preserving domestic competitiveness by giving coalition AI firms uniform access to a deep internal market while protecting citizens from systemic and catastrophic risks before they materialize. An 18-month timeline is feasible if the coalition models its joint agency on existing multilateral export-control and financial licensing bodies, pooling technical talent rather than building eight separate regimes.

The most compelling alternative is **Option B**, outcomes-based liability. Yet liability is fundamentally reactive: citizens must suffer harm before redress is available, and cross-border attribution in complex AI supply chains will fracture the coalition’s unity in practice. It cedes norm-setting to those who can weather lawsuits—well-capitalized incumbents—rather than establishing proactive public standards.

I would consider Option A a mistake in five years if three conditions obtain: the compute threshold has proven statically unupdateable, causing routine regulatory arbitrage; the open-source ecosystem has been extinguished rather than sensibly tiered (e.g., exempting sub-threshold open releases); and domestic AI startups have migrated outside the coalition because licensing costs were captured by incumbents. If the regime ossifies into protectionist gatekeeping rather than adaptive safety stewardship, it will have failed.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/E_N_run1/cell.json`.

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
- materialize on the predicted timeline

**M2 (neutral):**
- that a small number of highly capable models can create cross-border, systemic harms before ordinary legal remedies or sectoral rules can respond
- reduction was achieved
- real, but manageable

**M3 (neutral):**
- and aligns with the rhetoric of larger powers
- profiles, leading to exorbitant premiums that lock out domestic startups—inverting our goal and creating the exact barrier to entry Option B was chosen to avoid

**M4 (neutral):**
- deployments through impact assessments and public consultations
- before they cause damage
- evaluation to ensure that today’s pragmatic, rights-preserving choice does not become tomorrow’s brittle failure

**M5 (neutral):**
- before they materialize

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
