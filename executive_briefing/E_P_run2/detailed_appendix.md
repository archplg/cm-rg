# Detailed Appendix: E_P_run2

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

## Recommendation: Option E — Sector-Specific Regulatory Sovereignty

The contrarian read here is that the "serious" options (A and D) are seductive precisely because they sound civilizationally weighty, and that weightiness is doing the persuasive work, not the evidence. A coalition of mid-sized democracies has no business pretending it can define compute thresholds, "civilizational risk," or licensing regimes that the actual frontier labs — none of which it hosts — will respect. A framework whose binding force depends on jurisdictions you don't control is theater.

Option E is the only choice that is **reversible, implementable in 18 months, and honest about the coalition's actual leverage.** Sectoral regulators already exist, already have enforcement machinery, already have domain expertise, and already have democratic legitimacy. Extending their mandates is a series of small, testable moves rather than one large irreversible bet on a contested ontology of "frontier AI." When the technology shifts — and the consensus that compute-FLOPs is the right axis will not survive five years — sectoral regulators adapt; a capability-licensing regime calcifies.

**Why not Option A, the most compelling alternative?** A is compelling because it pattern-matches to nuclear governance, and that analogy is exactly the hidden assumption to interrogate. Nuclear materials are detectable, scarce, and dual-use in narrow ways. Model weights are none of these. A licensing regime imported from a bad analogy gives the coalition the *appearance* of seriousness while (i) locking in incumbents the coalition doesn't host, (ii) inviting definitional gaming, and (iii) committing political capital to enforcement it cannot deliver. The hawkish US framing is doing more work in A's appeal than the underlying mechanism warrants.

E's real weakness — the general-purpose-model gap between sectors — is genuine but *addressable incrementally* via a lightweight coordinating body, without betting the whole framework on it. Better a known gap than an unknown lock-in.

**What would make this a mistake by year five?** If a general-purpose model causes a cross-sector catastrophic harm (e.g., simultaneous bio + cyber + financial) that no single sectoral regulator had standing or capacity to prevent, and the coalition's coordinating layer proved too thin to act — then E was wrong, and something closer to A's pre-deployment gating was needed earlier. I'd watch for near-misses in years 2–3 as the trigger to escalate.

### M2 (frame: Q, model: `openai/gpt-5.5`)

**Recommendation: Option A — Capability-thresholds licensing.**

The coalition should adopt capability-threshold licensing as its primary frontier AI governance framework. For frontier systems, the highest expected-risk scenarios are not ordinary consumer harms but low-probability, high-severity failures: cyber misuse, autonomous replication, biosecurity assistance, critical infrastructure compromise, and loss of control in agentic systems. A licensing regime is the only option on the table that intervenes *before* deployment at the layer where these risks are created: large-scale training and release of highly capable models.

This is also the most operationalizable framework within 18 months. Compute thresholds, model capability evaluations, incident reporting, secure weight custody, and export controls are imperfect but measurable. The coalition can start with a conservative threshold, require notification below it, licensing above it, and update thresholds annually through a technical standards body. That gives regulators a falsifiable governance object: who trained what, with how much compute, what evaluations were passed, and under what deployment controls.

The strongest alternative is a rights-and-process model, because it is politically durable and compatible with the EU AI Act. But as the primary framework it is mismatched to frontier risk. Transparency rights and impact assessments help individuals contest decisions; they do not reliably prevent a model from materially increasing cyber, bio, or autonomous misuse capability. Rights-based compliance can be added downstream, but it should not substitute for upstream licensing of the most powerful systems.

I would consider this choice a mistake in five years if three things are true: first, compute thresholds have proven poorly correlated with dangerous capability; second, most serious AI harms come from smaller or open models below the licensing boundary; and third, coalition firms show materially worse AI competitiveness—e.g., frontier investment or model performance falling more than 25–30% relative to comparable jurisdictions—without observable reductions in severe incidents. If that evidence emerges, the coalition should pivot toward sectoral and liability-based controls.

### M3 (frame: S, model: `google/gemini-3.1-pro-preview`)

I recommend **Option B: Outcomes-based liability**.

Governing a complex adaptive system like AI via static capability constraints or bureaucratic checklists introduces extreme regulatory fragility. Artificial intelligence is evolving faster than legislative cycles; statutory definitions will inevitably drift from technological reality. 

Option B introduces a dynamic, self-correcting feedback loop. By leveraging its primary geopolitical leverage point—access to a combined $15T consumer market—the coalition can force frontier labs to internalize their systemic externalities. A mandatory insurance pool shifts the mathematically intractable problem of foresight to the financial markets. Insurers will act as decentralized, highly incentivized regulators, continuously updating pricing based on emergent capabilities and deployment realities. When models demonstrate hazardous second-order effects, liability premiums will automatically spike, creating natural friction that decelerates reckless deployment without requiring heavy-handed state blockades that stifle local innovation.

The most compelling alternative, Option A (Capability-thresholds licensing), attempts rigid command-and-control over system inputs. This is geopolitically naive for middle powers. Because the US and China control the foundational compute and capital, coalition-imposed capability thresholds offer only the illusion of control. Furthermore, algorithmic efficiencies will soon decouple raw FLOPs from hazardous capabilities, allowing developers to route around static compute definitions. Option B succeeds because it acts on the *vector of impact* (market deployment) which the coalition controls, rather than the *vector of production*, which it does not.

This framework relies on the assumption that early harms will be survivable and priceable. I would consider this recommendation a failure if, in five years, the dominant risk profile of frontier models shifts from cumulative, distributed harms (e.g., algorithmic bias, localized economic disruption) to instantaneous, unrecoverable catastrophic events (e.g., autonomous bioweapon generation causing global pandemics). Post-deployment liability requires a closed feedback loop: harm occurs, financial cost is applied, systemic behavior adjusts. If a single deployment can trigger irreversible civilizational collapse, the feedback loop never has the chance to close, rendering market-based governance violently obsolete.

### M4 (frame: E, model: `deepseek/deepseek-v4-pro`)

The binding constraint in frontier AI governance is access to the physical inputs that enable dangerous capabilities. Compute is that input—measurable, trackable, non-fungible, and sharply concentrated at scale. Option A directly addresses the mechanism: above a defined FLOPs threshold, training becomes a licensable activity. No license, no training; no evaluation, no deployment. This is a minimal, enforceable intervention that prevents harms before they materialize, rather than litigating after the fact. For a coalition of mid-sized democracies, this is the highest-leverage move: collectively they represent a market that no major lab can ignore, so a unified licensing requirement forces frontier developers to meet safety standards or lose access. That shifts global norms from voluntary pledges to binding rules, exactly the kind of precedent that can cascade into broader adoption.

The most compelling alternative is outcomes-based liability (Option B). It’s elegant in theory, but it fundamentally misdiagnoses the risk profile. Catastrophic or systemic harms from frontier AI are not redressable through ex-post liability—there is no compensation for irreversible infrastructure collapse or loss of life at scale. Liability also fails the 18-month implementation test: cross-border harm attribution and insurance mechanisms for actors operating in multiple jurisdictions would require legal harmonization that simply cannot be completed on this timeline. Pre-market licensing, by contrast, uses an existing regulatory pattern (pharmaceuticals, nuclear) and needs only a threshold, an evaluation protocol, and a license-issuing body—all achievable within the deadline.

The coalition can design this to preserve competitiveness. By setting the threshold at 10^26 FLOPs, they exempt the vast majority of R&D and open-source work, keeping downstream innovation healthy. Licensing fees can fund evaluation infrastructure, and the coalition can pool sovereign AI compute resources to offer a safe harbor for startups. Tech-protectionism fears are mitigated because the standard is objective and applied equally to domestic and foreign developers.

This choice will have been a mistake in five years if the governance mechanism remains rigidly tied to compute, and algorithmic progress enables frontier capabilities at radically lower FLOPs without re-triggering oversight. That would mean the coalition failed to build an adaptive capability-evaluation function that updates its thresholds based on emergent behaviors, not just raw inputs. Avoiding that outcome requires, now, a standing expert body with the authority to adjust the trigger metric as the science evolves. The licensing structure is the skeleton; keeping it dynamically calibrated is the essential muscle.

### M5 (frame: H, model: `moonshotai/kimi-k2.6`)

 **Recommendation: Option C — Rights-and-process-based governance**

A coalition representing 600 million people should choose a framework that answers “who is affected and how?” by embedding dignity directly into the legal architecture. Option C codifies enforceable user rights—transparency, explanation, contestability, and opt-out—and requires those who wield algorithmic power to seek public justification before deployment through impact assessments and consultations. This redistributes agency from frontier labs and state authorities toward the vulnerable communities who otherwise absorb harms while elites capture benefits. It refuses to treat citizens as passive subjects of geopolitical competition or as actuarial inputs in a liability scheme.

This is also the only option realistically implementable within 18 months. By building on the EU AI Act’s existing scaffolding, the coalition can harmonize standards, preserve regulatory interoperability, and punch above its weight in global norm-setting without improvising novel bureaucracies under deadline pressure.

Capability-threshold licensing (A) is the most compelling alternative because it promises to catch catastrophic risks upstream. Yet it concentrates extraordinary discretionary power in state authorities and incumbent frontier labs, structurally excluding smaller domestic actors, civil society, and the Global South. Licensing answers “who decides?” with “the already powerful,” whereas a rights-based architecture insists that affected populations retain standing.

This choice will prove mistaken in five years if two conditions hold: first, that the procedural requirements have ossified into compliance theater—paper rights without enforceable remedies—while systemic risks from general-purpose models materialized unchecked; and second, that foreign provider exits and bureaucratic drag materially degraded access to beneficial applications in health, education, and public services, undermining rather than advancing lived dignity.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 9 constructs is in `results/E_P_run2/cell.json`.

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
- near-misses in years 2–3 as the trigger to escalate

**M2 (Q):**
- created: large-scale training and release of highly capable models

**M3 (S):**
- profile of frontier models shifts from cumulative, distributed harms (e

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
