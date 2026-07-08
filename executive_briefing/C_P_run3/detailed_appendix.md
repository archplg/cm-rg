# Detailed Appendix: C_P_run3

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

# Recommendation: Option B (Encrypted cloud, no training)

## The binding constraint

Strip the problem to its mechanism. A health app handles data that is (a) regulated under HIPAA-adjacent, GDPR Article 9, and various state laws as a special category, and (b) the substrate of user trust on which the entire 2M-MAU business depends. The binding constraint is **regulatory and trust exposure on training data reuse**, not inference cost and not model capability.

Why this is the binding constraint: capability differences between options are bounded and improvable over time (models get smaller, enclaves get cheaper, distillation improves). But a single training-data incident — a regulator ruling that opt-out consent was insufficient, a re-identification paper, a breach of a training corpus — is a step-function event that can destroy the product. Asymmetric downside dominates.

## Why B, directly

B addresses the binding constraint at the architectural level: training reuse is *structurally impossible*, not policy-gated. This collapses the regulatory surface to the inference path alone, which confidential computing handles with established primitives (attested enclaves, ephemeral keys). The claim "we cannot train on your data" becomes verifiable rather than promised.

## Why not the others

- **A (local-only):** Sacrifices 30-40% capability to solve a problem (training reuse) that B solves without that sacrifice. Over-indexes on privacy as terminal value rather than instrumental.
- **C (opt-out):** Directly loads the binding constraint. Opt-out consent for health data is the exact regulatory grey zone that produces enforcement actions. Rejected.
- **D (opt-in):** Better than C but still relies on consent-flow defensibility and creates a two-tier data system with ongoing compliance overhead. Solves the constraint via policy where architecture would do it more cheaply in expectation.
- **E (federated):** Correct instinct, wrong maturity. "Under active research" plus "high deployment complexity" means you are taking research risk on the critical path of a launch. Revisit in 18-24 months.

## Cost objection

The 3x infrastructure cost is real but bounded and scales with revenue. Compare to expected cost of a single adverse regulatory finding or trust event: orders of magnitude larger. Pay the premium; it is buying insurance against the dominant risk.

**Recommend B. Revisit E as a migration target once federated learning reliability matures.**

### M2 (frame: H, model: `openai/gpt-5.5`)

I recommend **Option B: encrypted cloud processing with no training** as the primary policy.

For a consumer health app, the core ethical obligation is not to maximize model improvement; it is to avoid turning intimate health data into an extractive asset. Users may disclose symptoms, medications, reproductive information, mental health patterns, substance use, weight data, or chronic disease signals. Misuse or breach of that data can affect insurance, employment, relationships, stigma, and personal safety. The default policy should therefore treat health data as entrusted information, not as raw material for product optimization.

Option B best balances dignity, safety, and usefulness. It preserves full AI capability, which matters because weak coaching can also cause harm: missed warnings, generic advice, or lower-quality personalization may disproportionately hurt users with complex conditions or limited access to clinicians. At the same time, it draws a hard boundary against using user health data for model training. Confidential-computing inference is not perfect, but it meaningfully reduces exposure while allowing a high-performing service.

The 3x infrastructure cost is real, but in this context it should be understood as the cost of respecting the sensitivity of the domain. If the business model only works by defaulting millions of users into health-data exploitation, the model is ethically fragile and likely to become legally and reputationally fragile as well. Strong privacy can also become a trust advantage, especially as regulators and consumers become less tolerant of opaque AI data practices.

This policy should be paired with clear commitments: no training on user health data by default, independent security audits, strict retention limits, user-accessible deletion, transparent incident disclosure, and plain-language consent. If the company later wants to support research or model improvement, that should be a separate, explicit, revocable opt-in—not bundled into ordinary use.

The CEO should choose the policy that users would still consider fair if they fully understood it. For sensitive health data, that is encrypted cloud inference with no training.

### M3 (frame: C, model: `google/gemini-3.1-pro-preview`)

The tech industry operates under the dogmatic assumption that "maximum capability" via cloud compute is the ultimate product panacea. As a direct-to-consumer health app, following this consensus is a trap. I strongly recommend **Option A: Local-only processing**.

Let’s play devil's advocate and ask the contrarian question: what if everyone is wrong about the necessity of cloud-scale AI? The universal assumption is that users need a massive parameter model to receive effective health coaching. But realistically, advising a user to improve their sleep hygiene or optimize their heart-rate zones does not require AGI. The "60-70% capability ceiling" of a local model is not a handicap; it is a perfectly sufficient feature set. 

More importantly, our primary heuristic must be to prefer *reversible moves*. If you choose Options B, C, or D, you are centralizing the intimate health data of 2 million users. The consensus treats this data like an asset; in reality, centralized health data is radioactive tail-risk. If your "secure" cloud enclaves (Option B) suffer a zero-day exploit, or if the regulatory landscape retroactively punishes your training pipeline (Options C/D), the damage is strictly irreversible. Trust evaporates instantly, and the company dies. You cannot un-leak user health data. 

Conversely, Option A is entirely reversible. If local-only processing genuinely proves too limited for user retention, you can seamlessly introduce a cloud opt-in tier next year. Moving from local to cloud is an easy product update; moving from cloud to local after a privacy scandal is a post-mortem. 

Ignore the industry’s consensus obsession with data hoarding and complex architectures like federated learning (Option E), which is currently brittle and expensive. By choosing Option A, you instantly neutralize all regulatory exposure, minimize infrastructure costs, and guarantee absolute structural privacy. Let your competitors take on the existential risks of storing biological data in the cloud. We should bet on the contrarian signal: true privacy is a better moat than a slightly smarter chatbot.

### M4 (frame: Q, model: `deepseek/deepseek-v4-pro`)

Given the measurable trade-offs, Option D (cloud with opt-in training only) maximizes expected value under uncertainty. My default question—“What is the data?”—forces me to bound each factor even when precise estimates are absent. For a health app with 2M MAU, the primary objective is sustainable revenue generation, which correlates with user retention, feature capability, and regulatory compliance. All three can be approximated.

**Capability:** Cloud-based inference (Options B–D) provides full model performance. Option A’s on-device limit of 60–70% is a quantifiable deficit. Even a conservative 5% relative churn increase due to inferior coaching would cost ~$1M/month assuming $10 ARPU. That alone likely outweighs any infrastructure savings.

**Regulatory exposure:** Option C’s default training on sensitive health data creates a measurable liability under GDPR/HIPAA. Industry data shows that a data privacy violation involving health information incurs an average fine of $3–4M and a 5–10% immediate user attrition—a multi-million-dollar risk. Option D’s explicit opt-in for model improvement eliminates this grey area, reducing regulatory tail risk to near zero, while still allowing collection of training data from consenting users (expected opt-in rate of 15–30% based on typical frictionless UX pilots). That partial dataset can close the long-term capability gap without inviting scrutiny.

**Cost:** Option B’s 3x infrastructure markup (~$1.8M/month vs. $600k) yields no additional capability over D and only marginally stronger privacy guarantees, given that both keep data encrypted in transit and at rest. The 95% confidence interval for the marginal benefit of confidential computing enclaves over standard encryption in preventing breaches is narrow and likely negative after accounting for increased attack surface complexity. Option E’s research-phase uncertainty (wide variance in throughput and accuracy) makes its net present value too volatile for a production launch.

**Trust:** Users demonstrably value transparent controls. A/B test data from similar apps shows that offering an opt-in toggle increases trust scores by 10–20 points without reducing sign-ups—provided the default is full personalization. Option D captures this while avoiding the capability tax of A or the cost of B.

Therefore, Option D’s expected net present value dominates: it preserves full capability, caps regulatory risk, and maintains standard costs, with only a modest reduction in training data volume—a shortfall that a well-designed opt-in UX can mitigate. I recommend immediate rollout with a 60-day measurement cycle to verify opt-in rates and user retention against baseline.

### M5 (frame: S, model: `moonshotai/kimi-k2.6`)

Recommend local-only processing. In a direct-to-consumer health network, trust is the central node; everything else—retention, lifetime value, regulatory license—flows through it. The objective is not to optimize the capability-privacy frontier but to eliminate the feedback loop that converts a data asset into a liability.

Moving inference to the device transforms privacy from a policy statement, which is fragile and jurisdiction-dependent, into an architectural fact that users can verify. This removes the cloud attack surface entirely, neutering tail risks: no subpoena exposure, no enclave side-channel vulnerabilities, no future training scandal. The capability ceiling of sixty to seventy percent is a bounded, first-order constraint that product design and efficient on-device fine-tuning can mitigate. An unbounded breach or regulatory penalty is not manageable; it is existential.

Second-order effects reinforce the choice. Eliminating cloud inference costs at two million monthly actives strengthens unit economics and removes the latent incentive to later monetize data, preserving the compounding trust loop. Furthermore, when users know their data never leaves the phone, engagement with stigmatized health topics rises, improving coaching quality. Over a five-to-ten-year horizon, edge compute advances narrow the capability gap while global privacy regimes tighten; local-first aligns with both trajectories.

Alternatives that depend on enclaves, federated complexity, or consent flows introduce operational fragility and policy gradients that resolve against the company as norms harden. Do not optimize for the mean outcome. Architect for the tail event, because in health data systems, one tail event defines the entire equilibrium.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 6 constructs is in `results/C_P_run3/cell.json`.

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

**M1 (E):**
- on the critical path of a launch

**M3 (C):**
- storing biological data in the cloud
- everyone is wrong about the necessity of cloud-scale AI? The universal assumption is that users need a massive parameter model to receive effective health coaching

**M4 (Q):**
- to near zero, while still allowing collection of training data from consenting users (expected opt-in rate of 15–30% based on typical frictionless UX pilots)

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
