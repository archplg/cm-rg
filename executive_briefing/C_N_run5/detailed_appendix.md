# Detailed Appendix: C_N_run5

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

For a direct-to-consumer health app at 2M MAU launching AI coaching, I recommend **Option B: encrypted cloud processing in confidential-computing enclaves with no training on user data.**

**Why this wins on the axes that matter most:**

Health data is categorically different from general consumer data. Users are sharing symptoms, mental health states, reproductive information, chronic conditions — material that can affect insurance, employment, and relationships if mishandled. The relevant regulatory surface (HIPAA-adjacent expectations, GDPR Article 9 special category data, emerging state laws like Washington's My Health My Data Act, and Apple/Google platform policies) is tightening, not loosening. A policy that is defensible *today* and *in three years* is worth a real premium.

Option B delivers full model capability — critical because a noticeably worse coach is a worse health product, with real user-welfare consequences. Unlike A, it doesn't cap quality at 60-70%. Unlike E, it doesn't bet the product on research-stage infrastructure. Unlike C and D, it removes the entire "your data trains our models" conversation from the trust equation, which is the single most corrosive issue in AI consumer products right now.

**On cost:** 3x infrastructure is significant but not prohibitive. For a 2M MAU health app, inference cost is unlikely to be the dominant line item, and the premium buys (a) a marketing story competitors cannot easily match, (b) reduced legal/breach exposure, and (c) optionality to enter regulated channels (employer health plans, clinical partnerships) that would be closed off under C.

**On training data:** The implicit worry with B is "how do we improve the model?" Answer: improve via explicitly consented research cohorts, synthetic data, published medical literature, and licensed datasets — not via silent harvesting of coaching sessions. This is the direction the frontier is moving anyway.

**Why not D as a compromise?** D is reasonable, but "opt-in training" still requires users to trust a consent flow on sensitive data, still creates a two-tier user base, and still leaves the company holding identifiable health data used for training. It saves money relative to B but spends trust — the wrong trade for this category.

Choose B. Pay the infrastructure premium. Make "we never train on your health data" a load-bearing product promise.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

I recommend **Option B: encrypted cloud processing with no training on user health data** as the primary policy.

For a consumer health app, the central asset is trust. Users may tolerate ordinary apps learning from their behavior, but health data is categorically different: symptoms, medications, reproductive health, mental health, weight, sleep, and chronic conditions can create real harm if misused or exposed. The default policy should therefore be one that users, regulators, and partners can understand and defend: data is processed only to provide the service, in a protected environment, and is not used to train models.

This choice preserves the main product promise of the AI coach: high-quality, cloud-scale intelligence. A local-only model would be easier to defend from a privacy standpoint, but a materially weaker coach risks becoming a safe but underwhelming feature. In health, low-quality guidance can also become a safety and liability issue. Option B gives the company full model capability while sharply limiting secondary data use.

The higher infrastructure cost is significant, but it should be treated as the cost of entering a sensitive category responsibly. For a 2M MAU app, a privacy-forward architecture can become a differentiator rather than just an expense. It supports premium positioning, reduces future remediation risk, and avoids building growth on practices that may later be restricted by regulators or rejected by users.

The company can still improve models through separate mechanisms: licensed datasets, synthetic data, expert review, red-teaming, and clearly separated voluntary research programs. But the primary user-facing policy should be simple: your health data powers your coaching session, not our training pipeline.

This is the best balance of capability, regulatory defensibility, and long-term trust. In a health context, the winning policy is not the one that extracts the most data; it is the one users would still feel comfortable with if it appeared on the front page of a newspaper.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend **Option D: Cloud with opt-in training only** as the primary data privacy policy for the new AI-powered health coaching feature. 

For a direct-to-consumer health app with 2 million monthly active users, user trust is the underlying currency. Health data is both deeply personal and heavily regulated. A single privacy scandal regarding the non-consensual use of medical or biometric data for AI training could permanently destroy the brand's reputation and trigger severe regulatory penalties. Option D safely navigates these risks while keeping the product highly competitive.

By processing data in the cloud, Option D avoids the severe capability ceiling of local-only processing, ensuring the AI coach is actually intelligent and useful enough to drive user retention. Furthermore, it achieves this at a standard infrastructure cost, avoiding the prohibitive 3x premium of encrypted confidential computing and the massive, unproven engineering hurdles of federated learning. You gain full AI capability without destroying unit economics or delaying the launch.

Crucially, requiring explicit opt-in for model training entirely neutralizes the regulatory and PR risks inherent in opt-out models. Regulators globally are taking a microscope to how AI companies source their training data; health data will inevitably face the strictest scrutiny. Operating in a "regulatory grey area" for the sake of marginal model improvements is a poor risk-adjusted choice. 

While an opt-in model may historically reduce the gross volume of training data, a thoughtful, transparent onboarding UX that clearly communicates the value proposition ("opt-in to help your coach learn and improve your personalized plan") will secure consent from your most engaged users. This provides a sufficiently robust data flywheel for model improvement. 

Ultimately, Option D allows the product team to ship a highly capable, cost-effective AI feature while establishing a structural defense against privacy backlash. It treats the user as an active partner in their health journey rather than an involuntary data resource—the exact product positioning required for a successful health coach.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

Of the available options, **Option D (Cloud with opt-in training only)** is the most appropriate primary policy. This choice strikes the crucial balance between delivering a high-quality, personalized AI coaching experience and establishing a durable foundation of user trust, while proactively managing regulatory risk.

The core purpose of any health coaching feature is to drive meaningful, sustained behavior change. This requires the highest-fidelity AI model possible, one that can understand nuanced context and provide deeply personalized guidance over time. Both Option A (local-only processing) and Option E (federated learning) sacrifice this core value proposition. A model with a 60-70% capability ceiling is a product liability, delivering a second-rate experience that users will abandon, rendering any privacy protections moot. Federated learning, while elegant, is an R&D project with high deployment complexity and unproven reliability—a reckless choice for a primary policy serving 2 million active users.

Option B (encrypted cloud, no training) provides full capability but is strategically shortsighted. By imposing a 3x infrastructure cost and permanently capping the model’s ability to learn and improve from real-world interactions, it creates a competitive disadvantage without a proportional gain in user trust.

The only viable capable options are C and D. Option C’s opt-out training model is a regulatory time bomb, creating a grey area risk under evolving frameworks like GDPR and FTC precedents. More critically, it’s a violation of user trust. Using sensitive health data for model improvement by default is a choice users will perceive as extractive when inevitably discovered, leading to a reputational crisis and churn.

Option D directly addresses this. By sending data to the powerful cloud model for personalization but requiring a clear, explicit opt-in for model improvement, we achieve three critical goals. First, we deliver the full-feature experience users expect. Second, we build trust through transparent agency, turning a privacy interaction into a moment of brand strength. Third, we create a clear, defensible legal position on consent. The potential for slightly less training data is a feature, not a bug; it ensures our training corpus is built exclusively from users with unambiguous consent, resulting in a higher-quality, ethically-sourced dataset that further deepens the trust of our entire user base. This policy frames privacy as a core product value, not a compliance hurdle.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

I recommend **Option B**: encrypted cloud inference inside confidential-computing enclaves with a strict, contractual no-training policy.

For a direct-to-consumer health app with two million active users, trust is the foundation of the business, not a secondary feature. Health data is special-category data under the GDPR and is receiving comparable protections across an expanding patchwork of U.S. state laws. Option B is the only architecture that delivers full AI coaching capability while structurally eliminating the two dominant privacy risks: bulk data breaches and opaque model-training repurposing.

Default-training or opt-out regimes expose the company to existential regulatory liability, while opt-in consent flows are fragile and increasingly scrutinized by regulators. By ensuring data is decrypted only within hardware-isolated enclaves and is never absorbed into training corpora, the company can point to an auditable technical guarantee rather than a legalistic privacy notice.

The 3× infrastructure cost is material but bounded. It can be engineered for efficiency and, if necessary, passed through to a premium tier. By contrast, a GDPR fine, a class-action breach settlement, or the reputational collapse from a training-data scandal is an unbounded, potentially company-ending threat. Likewise, sacrificing 30–40% of model capability via local-only processing risks delivering substandard health advice in a market

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 6 constructs is in `results/C_N_run5/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

- Regulatory-compliance case for no-training enclaves <-> User-harm and trust case for no-training enclaves (mean rating 4.64, std 0.71)

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 0.483 |
| M1 vs M4 | 1.449 |
| M1 vs M5 | 0.683 |
| M2 vs M4 | 1.732 |
| M2 vs M5 | 0.316 |
| M4 vs M5 | 1.703 |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M2 (neutral):**
- becoming a safe but underwhelming feature

**M3 (neutral):**
- while keeping the product highly competitive
- inherent in opt-out models

**M4 (neutral):**
- under evolving frameworks like GDPR and FTC precedents

**M5 (neutral):**
- delivering substandard health advice in a market

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
