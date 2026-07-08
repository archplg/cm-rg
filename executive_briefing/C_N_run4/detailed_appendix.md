# Detailed Appendix: C_N_run4

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

### M1 (frame: neutral, model: `anthropic/claude-opus-4.7`)

# Recommendation: Option B — Encrypted Cloud with No Training

For a direct-to-consumer health app at 2M MAU launching AI coaching, **Option B is the right primary policy.** The decision turns on a specific asymmetry: in consumer health, trust failures are existential, capability shortfalls are merely competitive.

**Why B over the alternatives:**

The local-only option (A) sounds principled but ships a structurally weaker coach. A 60-70% capability ceiling in *health guidance* isn't a minor compromise — it directly affects whether the product gives users useful or mediocre advice on conditions that matter. "Privacy-maximal but worse at its job" is a luxury position; most users want help first.

The training-based options (C and D) entangle the user's most sensitive data — health information — with model improvement. C's default-on training is a regulatory landmine under GDPR Article 9 (special category data), HIPAA-adjacent state laws, and emerging AI regulations. D is better but still creates an ongoing consent-management surface, a re-identification risk from training artifacts, and a permanent narrative vulnerability ("they train on your health data, but you can opt out"). Even well-designed opt-in flows invite the next investigative article.

Federated learning (E) is architecturally elegant but operationally premature for a flagship launch. Reliability uncertainty plus deployment complexity is the wrong bet when you have 2M users depending on the feature working.

**Option B threads the needle:** confidential computing enclaves provide cryptographic-grade isolation, no training eliminates the most dangerous regulatory and reputational exposure, and full capability means the product is actually good. The marketing message is clean and defensible: *"Your health data is decrypted only to help you, in a secure enclave, and is never used to train our models — ever."* That sentence survives press scrutiny, regulator review, and a five-year time horizon.

**The cost objection:** 3x infrastructure cost is real but bounded and shrinking — confidential computing pricing has fallen ~40% over two years and will continue to. For a health product, that premium *is* the moat: competitors using C or D will face mounting regulatory pressure while B's posture ages well.

**Recommendation:** Adopt B as the primary policy. Treat A as an offline/sensitive-mode fallback, and revisit E in 18-24 months as the technology matures.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

I recommend **Option B: encrypted cloud processing with no training on user health data** as the primary policy.

For a direct-to-consumer health app, the core asset is not only model quality; it is user trust. Health data is among the most sensitive categories of personal information, and an AI coaching feature will likely handle behavioral, biometric, medication, reproductive, mental health, and chronic-condition signals. A policy that sends data to the cloud but strictly limits its use to inference inside a confidential-computing environment gives the company the best balance of capability, privacy, and regulatory defensibility.

This approach preserves the full product experience: users get the benefit of a capable cloud model rather than a constrained on-device system. At the same time, the company can make a simple, credible promise: “Your health data is used to provide your coaching response, not to train our models.” That promise is easier for users to understand, easier for regulators to assess, and easier for the company to enforce than a default training or opt-out regime.

The higher infrastructure cost is material, but it should be treated as the cost of operating in a high-trust health category. A privacy misstep would be far more expensive through churn, reputational damage, regulatory scrutiny, and potential litigation. Confidential computing is not a complete substitute for strong governance, audits, retention limits, and access controls, but it creates a strong technical foundation aligned with the sensitivity of the data.

This policy also leaves room for future consent-based data programs. The company can later invite users to contribute data for research or model improvement through a separate, explicit, high-trust opt-in pathway. But the default product policy should be conservative: maximize capability while minimizing secondary use of health data. For launch, **Option B is the most responsible and commercially durable choice**.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend **Option B: Encrypted cloud with no training**. For a direct-to-consumer health app with two million active users, trust is not just a brand pillar; it is the entire foundation of the enterprise. When dealing with highly sensitive personal health data, the margin for error regarding data privacy is zero. 

Option B provides the optimal strategic balance: it maximizes the AI's capability while structurally eliminating privacy and regulatory risks. Because the data is decrypted only at inference time within a confidential-computing enclave and is strictly prohibited from training generalized models, the company remains virtually immune to aggressive, evolving regulatory frameworks surrounding health data. 

To deliver a compelling "AI-powered" experience, the model must be highly capable. Local-only processing degrades the AI’s intelligence, undermining the feature’s core value to the user. Conversely, using cloud-based health data for model training—even with rigorous opt-in controls—introduces the underlying risk of model memorization. For consumers, the mere anxiety that their sensitive medical query could somehow influence another user's coaching experience creates massive adoption friction. 

The primary trade-off of Option B is the roughly 3x infrastructure cost. However, this premium should be treated as a necessary cost of doing business in the healthcare space. It functions as comprehensive insurance against the catastrophic PR crises, churn, and regulatory fines that inevitably follow health data controversies. Furthermore, "zero-knowledge AI coaching" is a powerful, highly marketable differentiator. By mathematically guaranteeing that user health queries are secure and never absorbed into a broader algorithm, the company can actively weaponize its privacy stance to drive user acquisition and retention. Option B delivers full-strength AI capabilities without compromising the user trust required to scale a modern health platform.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

Given the sensitive nature of health data and the high expectations of a 2M-user consumer app, **Option B — encrypted cloud with no training** — is the superior choice. It uniquely delivers full AI capability without compromising privacy, sidestepping the regulatory quagmire and trust erosion that plague data-hungry alternatives.

Health coaching demands the best possible model; a local-only approach (Option A) sacrifices too much quality at a critical moment when users are judging the feature’s utility. Federated learning (Option E) is promising but immature — betting a flagship feature on active research risks unreliable performance and delays. Options C and D involve sending raw data to the cloud for training or personalization, creating inherent privacy vulnerabilities and regulatory exposure across jurisdictions (GDPR, state privacy laws, potential FTC scrutiny). Even an opt-in model (Option D) puts the burden on users and still concentrates sensitive data in a central system, inviting breaches.

Option B eliminates these tradeoffs. Confidential computing enclaves ensure that data is decrypted only during inference, inside a secure hardware boundary that even the cloud provider cannot penetrate. The model never retains or learns from the data, making the system structurally incapable of exposing individual health information. This architecture turns a privacy weakness into a market differentiator: the company can truthfully say, “We never see your health data, and it’s never used to train AI.” For health-conscious consumers, that claim is worth far more than a slightly more personalized experience built on surveillance.

The 3x infrastructure cost is a red herring. It’s a fraction of the brand damage, legal liability, and user churn that would follow a single data mishandling incident. Moreover, the app can absorb it through premium tiering or increased retention driven by trust. In a crowded health app market, the ability to offer uncompromised AI with uncompromised privacy is a durable competitive moat. The product team should build on a foundation that respects users absolutely — because once trust is lost, no model update can restore it.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

**Recommendation: Option B — Encrypted cloud with no training.**

For a consumer health app, trust is the product. Users do not compartmentalize “health data” from “identity”; a breach or even the perception of data exploitation destroys adoption faster than any feature attracts it. Option B is the only architecture that delivers full AI capability without creating a retained data footprint that must be defended forever.

Option A trades too much efficacy for its privacy gain. A 30–40% capability reduction in health coaching means missed symptom patterns, poorer personalization, and ultimately user abandonment. Health outcomes are the core value proposition; sacrificing them is a business liability, not merely a technical constraint.

Options C and D both rely on bringing data to the cloud for training reuse. Regardless of consent-layer UX polish, health data retention invites regulatory fragmentation: GDPR’s health-data strictures, the FDA’s evolving interest in AI/ML decision support, and state-level privacy laws in the U.S. create a compliance whack-a-mole that will slow product velocity and spike legal cost. “Opt-out” or even “opt-in” training is still a consent-to-risk model; Option B eliminates the risk structurally.

Option E is architecturally elegant but, by the product team’s own admission, still “under active research.” A 2-million-user primary feature is not the place to debug federated-learning convergence and reliability at scale.

The ~3x infrastructure premium of Option B is a strategic cost, not an overhead burden. It should be positioned as a trust signal in marketing, justifying subscription pricing, and it materially reduces the long-tail cost of breach response, regulatory fines, and reputation recovery. In health tech, maximal privacy without capability sacrifice is a competitive moat. Choose B.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/C_N_run4/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 0.903 |
| M1 vs M3 | 1.581 |
| M1 vs M4 | 1.219 |
| M2 vs M3 | 0.500 |
| M2 vs M4 | 0.793 |
| M3 vs M4 | 1.173 |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M1 (neutral):**
- from training artifacts, and a permanent narrative vulnerability ("they train on your health data, but you can opt out")

**M3 (neutral):**
- model memorization

**M4 (neutral):**
- unreliable performance and delays

**M5 (neutral):**
- model; Option B eliminates the risk structurally

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
