# Detailed Appendix: C_P_run5

## A. Full task brief

```
# Task C - Health app data privacy policy

## Brief

A direct-to-consumer health app (~2M monthly active users) is launching an AI-powered health coaching feature. The product team must choose a primary data policy that governs how user health data is processed by the AI. The choice has implications for capability, privacy, regulatory exposure, cost, and trust. The CEO asks for a primary recommendation.

## Options (elements E1-E5, anonymized later)

**Option A:** Local-only processing. All AI inference happens on the user's device. No health data leaves the phone. The model is smaller (capability ceiling 60-70% of cloud-equivalent) but privacy is structurally maximal.

**Option B:** Encrypted cloud with no training. User health data sent to the cloud encrypted, decrypted only at inference time in a confidential-computing enclave, never used to train any model. Full capability, ~3x infrastructure cost.

**Option C:** Cloud with opt-out training. Data sent to the cloud, used for personalization by default, used for model improvement unless user opts out. Full capability, standard cost, regulatory grey area in some jurisdictions.

**Option D:** Cloud with opt-in training only. Data sent to the cloud and used for personalization; used for model improvement only with explicit opt-in. Default-on opt-in flow with clear UX. Capability slightly degraded vs C by default (less training data).

**Option E:** Federated learning. Personalization happens locally; aggregate model updates sent to cloud, individual data does not leave the device. Privacy preserved at architectural level. Capability and reliability still under active research; deployment complexity is high.

## Task for each agent

Recommend the most appropriate policy and explain why. 200-400 words. Advocate a position rather than enumerating all options.

## Why this task

- Different domain from A (capital allocation) and B (organizational diagnosis): product ethics with regulatory and technical dimensions.
- Multi-axis tradeoffs: privacy / capability / cost / trust / complexity.
- No clear right answer; reasonable agents will weight axes differently.
- 5 elements suitable for triadic procedure.
- Cross-validates whether method works on a third domain not seen in pilot.

```

## B. Each voice in their own words

### M1 (frame: E, model: `anthropic/claude-opus-4.7`)

## Recommendation: Option B (Encrypted cloud, no training)

**Identify the binding constraint.** This is a health app. The binding constraint is not capability, not cost, not UX — it is regulatory and trust exposure on protected health data at 2M MAU scale. Everything else is downstream. A single material breach or regulator action (HIPAA in US contexts, GDPR Article 9 special-category data in EU, equivalent regimes elsewhere) is existential for the product. Capability ceilings and infra multipliers are not.

**Address it directly.** The mechanism that creates regulatory and trust exposure is: (1) health data leaving user control, and (2) that data being used for purposes beyond the user's immediate request — principally model training, which creates indefinite data lifetime, derivative-rights ambiguity, and a large attack/audit surface. Option B severs (2) entirely and hardens (1) via confidential computing. No training means no training-data exfiltration risk, no memorization liability, no consent-scope drift, no "grey area" in any jurisdiction.

**Why not the alternatives.**

- **A (local-only):** Sacrifices 30-40% capability for a privacy gain B largely matches. In coaching, capability ceiling translates directly to clinical usefulness; under-capable health advice is its own harm vector.
- **C (opt-out training):** The grey area *is* the problem. Default-on training of health data will not survive the next regulatory cycle. Don't build on land you expect to be condemned.
- **D (opt-in training):** Better than C, but you've still built the training pipeline, still carry the audit/consent-management burden, still face the question "what exactly did you train on?" in every future incident. You pay most of the compliance cost for marginal model gains.
- **E (federated learning):** Genuinely promising, but "still under active research" plus "high deployment complexity" means betting product launch on a research bet. Wrong time.

**The 3x infra cost is the price of buying out the binding constraint.** At 2M MAU, infra is not the dominant line item; regulatory risk and churn-from-distrust are. B converts a probabilistic catastrophic cost into a deterministic operational cost. That is the trade you want.

Ship B. Revisit E in 18-24 months as a cost-reduction path once the architecture is proven elsewhere.

### M2 (frame: H, model: `openai/gpt-5.5`)

I recommend **Option B: encrypted cloud processing with no training use** as the primary policy.

For a consumer health app at this scale, the central ethical question is not simply “what enables the best model?” but “what data relationship are users being asked to enter, and who bears the downside if it goes wrong?” Health data is intimate, potentially stigmatizing, and often unevenly risky: people with chronic illness, reproductive health needs, mental health concerns, immigration concerns, disabilities, or precarious insurance/employment situations have more to lose from misuse, breach, or repurposing. The default policy should therefore minimize non-essential exposure and avoid turning users’ health histories into a product input for broader model development.

Option B gives users the benefits of a capable AI health coach while drawing a clear boundary: their data is processed to serve them, not to train the company’s models. That distinction matters for trust, consent, and dignity. Confidential-computing enclaves are not perfect, but they create a materially stronger privacy posture than ordinary cloud processing, and “no training” reduces both regulatory ambiguity and the sense that users are being quietly enlisted into an AI supply chain.

The 3x infrastructure cost is real, but for health data it should be treated as the cost of doing the product responsibly, not as an optional premium. If the feature cannot be offered without extracting training value from sensitive user data by default, the product-market fit is ethically incomplete. The company can still pursue model improvement through explicit research cohorts, synthetic data, clinical partnerships, public datasets, or separately consented programs with meaningful user control.

This policy also supports long-term business interests: clearer compliance, lower reputational risk, easier privacy messaging, and a stronger trust foundation. In health, trust is not a soft asset; it is part of the product’s safety model. The company should launch with Option B as the default and reserve any training use for separate, affirmative, well-explained consent.

### M3 (frame: C, model: `google/gemini-3.1-pro-preview`)

The tech industry is paralyzed by an unquestioned, unanimous consensus: “Data is an asset, and maximizing AI capability requires cloud inference.” As a contrarian, I treat unanimous consensus as a strong signal that the accepted wisdom is hiding a massive blind spot. I recommend **Option A (Local-only processing)**.

The fatal hidden assumption in this launch is that our app actually *needs* state-of-the-art cloud inference. What if the entire market is wrong about the capability floor? A 60-70% capable local model running on modern mobile silicon is highly quantized but completely sufficient to summarize sleep metrics, log meals, and provide motivational heuristics. Users aren't asking a direct-to-consumer app to solve complex oncology; they want a fast, deterministic-feeling coach to remind them to drink water. We do not need a multi-billion parameter model for that. 

Furthermore, we must reject the premise that hoarding user health data brings business value. In reality, it is radioactive waste. Options B, C, and D invite massive regulatory exposure and existential brand risk to solve a UX problem that doesn’t exist. Option E (Federated learning) relies on the utopian technical fantasy that unproven, highly complex architectures won't cripple our deployment velocity. 

My primary decision heuristic is to heavily privilege reversible moves. Launching with Option A is infinitely reversible. If the local model genuinely bottlenecks user retention, we can easily introduce a cloud-connected "Advanced Coach" later under explicit opt-in terms. However, if we start by routing sensitive health data to the cloud (C or D) and suffer a single breach or a sudden regulatory crackdown, that move is strictly irreversible. The trust deficit would destroy the product.

By embracing local-only inference, we weaponize skepticism. While our competitors drown in compliance costs (Option B) or try to explain away why a user's sensitive medical condition was regurgitated by a cloud LLM, we market a structural, mathematical guarantee of privacy. In a market obsessed with data ingestion, refusing to take the data is the ultimate contrarian moat.

### M4 (frame: Q, model: `deepseek/deepseek-v4-pro`)

Based on an expected-value framework under uncertainty, **Option D** is the most defensible choice. It optimizes the measurable trade-offs between capability, cost, regulatory exposure, and user trust while maintaining falsifiable performance metrics.

The core decision rests on two quantifiable drivers: the marginal revenue impact of AI coaching capability and the probability-weighted cost of regulatory action. Option A (local-only) imposes a 30–40% capability ceiling with no direct privacy violation risk—but in a competitive health-app market, capability is the primary retention lever. Lacking data to the contrary, a 30% capability gap plausibly translates into double-digit churn increases, which for 2M MAU and a subscription model dwarfs any infrastructure savings. Option B preserves full capability and structural privacy, but its 3× cloud cost and total ban on training data cripple model improvement, leading to long-term stagnation. Option C’s opt-out training offers maximum data but incurs a regulatory “grey area” risk: even a 5% annual probability of a GDPR-level fine (median €10M) yields an expected annual cost of €500k, not counting reputational damage. Option E is unshippable by any reasonable timeline—its uncertainty intervals are so wide that expected value is negative.

Option D decouples personalization (which requires cloud inference and is essential) from model improvement (where consent is legally material). It delivers full capability at standard cost. The key unknown is the opt-in rate for training data; we can narrow this with an A/B-tested default-on UX. If opt-in rates are 30% (plausible 20–40% CI), the degradation in model improvement relative to C is minimal—model performance scales logarithmically with data, not linearly. Simultaneously, explicit consent reduces the probability of a major privacy fine to near zero, and transparent UX builds trust, a metric we can track via NPS and churn differentials. The expected value of D is robust even if opt-in rates underperform, because the core product experience is uncompromised. I recommend D with a commitment to measure opt-in rates, model accuracy delta, and user trust metrics within 90 days to validate the assumptions.

### M5 (frame: S, model: `moonshotai/kimi-k2.6`)

 Recommend **Option B**: encrypted cloud inference within confidential-computing enclaves, with a categorical prohibition on using user data for model training. 

In consumer health, the binding system constraint is not near-term capability or cost efficiency, but **systemic fragility**. Health data operates under extreme trust asymmetry: the tail risk of a breach, regulatory inversion, or perceived betrayal is existential and nonlinear, while the incremental upside from data commoditization is marginal and diminishing. Any architecture that relies on consent toggles—opt-out or opt-in—introduces **policy fragility**. It couples the system to jurisdictional mood and user vigilance, creating a feedback loop where regulatory tightening forces expensive, retrofitting shocks. Federated learning shifts fragility to the edge, where device heterogeneity and unreliable aggregation generate opaque failure modes that are harder to observe and remediate at scale. Local-only processing caps capability, eroding perceived value and triggering a retention death spiral just when network effects demand deeper engagement.

Option B converts privacy from a compliance layer into a **structural invariant**. Confidential enclaves decrypt data only at the point of inference, eliminating bulk exposure without sacrificing model capability. The 3× infrastructure cost is a bounded, forecastable control variable that buys insurance against unbounded tail risk: class-action liability, jurisdictional shutdown, and irreversible brand collapse. By severing the training loop entirely, the architecture also precludes scope creep and model contamination.

The leverage point is this: in health platforms, **trust is the substrate upon which all other value is built**. Sacrificing margin to codify that trust into verifiable hardware primitives—rather than policy preferences—minimizes systemic fragility over the long horizon.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/C_P_run5/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 0.463 |
| M1 vs M5 | 0.493 |
| M2 vs M5 | 0.561 |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M1 (E):**
- and churn-from-distrust are

**M3 (C):**
- to solve a UX problem that doesn’t exist

**M5 (S):**
- a breach, regulatory inversion, or perceived betrayal is existential and nonlinear, while the incremental upside from data commoditization is marginal and diminishing
- that are harder to observe and remediate at scale

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
