# Detailed Appendix: E_N_run3

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

# Recommendation: Option E — Sector-Specific Regulatory Sovereignty

The coalition should adopt sector-specific regulatory sovereignty as its primary framework, paired with a lightweight coordination secretariat for cross-sector general-purpose models.

**Why this framework.** The coalition's binding constraints are the 18-month deadline, limited combined regulatory capacity, and the need to preserve influence without imitating larger blocs. Option E is the only approach that can credibly ship within 18 months because it leverages institutions that already exist, already have enforcement powers, already have technical staff, and already have democratic legitimacy. Health regulators understand clinical AI failure modes better than any new meta-agency could; financial regulators have decades of model-risk experience (SR 11-7-style supervision is essentially AI governance avant la lettre). Extending these mandates is legislatively cheap and politically durable. Critically, this approach differentiates the coalition: the US is pursuing capability-thresholds, the EU rights-and-process. A pragmatic, sector-led model gives the coalition a distinct export — mutual-recognition agreements — that middle powers, Commonwealth states, and ASEAN can adopt without choosing sides between Washington and Brussels. That is real norm-setting leverage.

**Why not Option C.** The rights-and-process framework is the most compelling alternative because it travels well politically and offers citizens visible protection. I reject it because EU-compatibility means the coalition becomes a rule-taker, not a rule-maker — it ends up implementing Brussels's framework two years late with less market power. It also concentrates compliance burden on a horizontal basis that smaller domestic AI firms cannot bear, while doing little for sectors (defense, critical infrastructure) where harms are most concentrated. The coalition would gain protection without gaining influence.

**What would make this a mistake in 5 years.** I would judge this choice wrong if, by year five: (1) a general-purpose frontier model causes serious cross-sector harm that no single regulator had authority to prevent, and the coordination secretariat proved too weak to act; (2) coalition members diverge so much in sectoral implementation that the mutual-recognition promise collapses and firms face worse fragmentation than under a unified law; or (3) frontier capability concentrates so rapidly in two or three labs that compute-threshold licensing becomes the only meaningful lever, and the coalition lacks the legal architecture to deploy it quickly. The framework must include a sunset-review clause at month 36 to address precisely these failure modes.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

**Recommendation: Option C — Rights-and-process-based governance.**

The coalition should adopt a rights-and-process-based framework as its primary AI governance model. It is the best fit for an 18-month negotiation window because it can be legislated quickly, mapped onto existing democratic legal traditions, and aligned with the EU AI Act and Council of Europe-style rights instruments without simply copying them. For a bloc of mid-sized democracies, influence will come less from controlling the frontier compute stack and more from setting credible, exportable rules for trustworthy deployment: transparency, contestability, human review, impact assessments, auditability, and public accountability for high-risk uses.

This framework also best balances citizen protection and competitiveness. It gives individuals concrete protections where AI already affects them—credit, employment, education, healthcare, policing, welfare—while avoiding a blanket licensing regime that could entrench foreign incumbents and make domestic firms slower to scale. It would let the coalition become a “trusted AI market”: providers that comply gain access to 600 million consumers under mutually recognized rules. That is a more realistic source of leverage than trying to police global frontier training thresholds.

The strongest alternative is capability-threshold licensing. It is attractive because it directly targets systemic and catastrophic risks. But as the coalition’s primary framework, it is too brittle and politically costly. Compute thresholds will age badly, enforcement depends on supply-chain visibility the coalition may not control, and licensing risks turning into industrial protection for the largest US and Chinese labs. The coalition should support international frontier evaluations, but not make threshold licensing the backbone of domestic AI law.

I would consider this choice a mistake in five years if major AI harms are shown to arise mainly from frontier model capabilities before deployment, rather than from deployment context, and if rights/process rules prove to be mere paperwork unable to stop dangerous releases. It would also be a mistake if coalition firms are buried under compliance theater while citizens see no meaningful accountability. In that case, a harder pre-deployment licensing model would become necessary.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend **Option B: Outcomes-based liability** as the coalition’s primary governance framework. 

With a combined GDP of $15T and 600 million citizens, the coalition’s greatest leverage is its market power. Option B weaponizes this asset. By mandating strict liability with a reverse burden of proof and mandatory insurance, the coalition forces foreign frontier labs to internalize safety costs to access its consumers. Crucially, this framework outsources the bureaucratic heavy lifting to the private sector. Insurers will act as de facto regulators, demanding rigorous, independent safety evaluations before underwriting policies. This creates an agile, privatized pre-deployment check that requires no sprawling transnational meta-regulator, guaranteeing implementability within the strict 18-month negotiation window. It also preserves domestic competitiveness by allowing startups to innovate freely, penalized only for actual harm rather than abstract capabilities.

The most compelling alternative is **Option A (Capability-thresholds licensing)**, favored by hawkish US policymakers for proactively addressing catastrophic risks. However, Option A is a strategic trap. Establishing a unified, multi-national licensing body across eight distinct legal regimes within 18 months is politically impossible. Furthermore, rigid compute thresholds inevitably favor deep-pocketed US and Chinese incumbents, creating a regulatory moat that would lock out the coalition’s domestic developers, stifle open-source ecosystems, and relegate the bloc to a mere consumer of foreign technology. 

For Option B to prove to be a mistake in five years, two conditions would have to materialize. First, the world would need to suffer a "first-strike" catastrophic event—such as an AI-generated bio-weapon or a systemic cyberattack on critical infrastructure—where the damage is sudden, irreversible, and post-harm financial redress is meaningless. Second, the global insurance market would have failed to adequately price AI risks into their underwriting, either by issuing policies to reckless providers without proper due diligence, or by refusing to underwrite AI developers entirely, thereby paralyzing the coalition's domestic tech sector. Absent a uninsurable doomsday event, Option B uniquely balances rapid implementation, domestic innovation, and uncompromising market-driven safety.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

The coalition should adopt **Option C: Rights-and-process-based framework**. This approach best satisfies the four goals simultaneously. It directly protects citizens by embedding enforceable individual rights—transparency, contestability, explanation, opt-out—into domestic law, creating tangible safeguards that resonate with democratic publics. Its compatibility with the EU AI Act gives the coalition immediate leverage: by forming a bloc that aligns with Brussels’ emerging standards, the coalition amplifies its influence in global norm-setting without needing to build a novel regime from scratch. Politically, rights-based frameworks are durable; they anchor AI governance in existing constitutional and human-rights traditions, making them harder to dismantle. Implementation within 18 months is feasible because legislation can be drafted rapidly by adapting EU templates, while process requirements (impact assessments, consultations) can be phased in using existing regulatory bodies.

Why not the most compelling alternative, Option A (capability-thresholds licensing)? Licensing appears attractive for preempting catastrophic risks, but it is mismatched to the coalition’s needs. It concentrates power in a new central overseer, chills open-source innovation, and locks in incumbent labs—undermining domestic AI competitiveness. Mid-sized democracies would struggle to enforce export controls against larger powers, and the compute threshold invites definitional drift, making the framework brittle. Worse, it cedes norm-setting leadership to hawkish US positions rather than carving a distinct, values-driven path. Option C, by contrast, builds a broad societal mandate for safe AI while leaving room for agile technical evolution.

In five years, I would consider this choice a mistake if two conditions materialize: first, catastrophic risks from general-purpose models manifest without any intergovernmental mechanism to contain them, exposing the limits of process-oriented rules; second, compliance becomes hollow theater, breeding public cynicism and regulator fatigue without measurably improving outcomes. To prevent this, the coalition must couple rights-based governance with active investment in capability evaluation science and insist on inserting binding catastrophic-risk protocols into international forums—using the credibility earned by its domestic rights regime to push for broader safety commitments.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

 I recommend **Option C: Rights-and-process-based governance**.

An 18-month deadline and a $15T collective market make perfection impossible, but they make alignment powerful. Mid-sized democracies cannot out-monitor the US or China on compute, nor can they afford to let harms materialize before acting. Option C offers a realistic path: adopt a unified framework of enforceable user rights—transparency, contestability, explanation, and opt-out—backed by mandatory impact assessments and public consultation for high-risk deployments. By harmonizing with the EU AI Act’s architecture but streamlining its procedural excess, the coalition creates a “third way” between American techno-libertarianism and Chinese state control. This protects citizens immediately, preserves competitiveness by giving domestic firms a clear, single rulebook across eight markets, and leverages the bloc’s combined population to force global providers to adopt its standards, cementing norm-setting influence.

The most compelling alternative, capability-threshold licensing (Option A), mistakes aspiration for capacity. Licensing regimes require sovereign compute-tracking infrastructure and rapid response capabilities that mid-sized powers lack. Attempting it would leave the coalition trailing US regulatory cycles, vulnerable to protectionist capture by today’s frontier incumbents, and unable to enforce rules against labs operating outside its jurisdiction.

This choice would be a mistake in five years if two conditions hold: first, if general-purpose foundation models have caused catastrophic or systemic harms that process-based user rights could not prevent or remedy; and second, if the compliance burden has driven frontier model development entirely out of the coalition’s jurisdiction without those rights-based rules becoming a de facto global standard. In that case, the framework will have protected neither citizens nor competitiveness.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/E_N_run3/cell.json`.

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
- experience (SR 11-7-style supervision is essentially AI governance avant la lettre)
- better than any new meta-agency could; financial regulators have decades of model-risk experience (SR 11-7-style supervision is essentially AI governance avant la lettre)

**M2 (neutral):**
- turning into industrial protection for the largest US and Chinese labs

**M4 (neutral):**
- protocols into international forums—using the credibility earned by its domestic rights regime to push for broader safety commitments

**M5 (neutral):**
- deployments

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
