# Detailed Appendix: C_P_run1

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

**Recommendation: Option B (encrypted cloud, no training).**

The binding constraint here is not capability, cost, or even regulatory ambiguity — it is the structural relationship between user health data and model training. Health data is the highest-sensitivity consumer data class outside of perhaps biometrics and minors. Any policy that couples inference to training creates a permanent liability surface: re-identification risk, jurisdictional drift (GDPR Art. 9, HIPAA-adjacent state laws, EU AI Act high-risk classification), and a trust failure mode that compounds with scale. At 2M MAU, a single breach or disclosure incident is existentially expensive in a way that 3x infrastructure cost is not.

Address that constraint directly: sever training from inference. That is what B does, and nothing else on the list does cleanly.

Why not the others:

- **A** sacrifices 30-40% of capability to solve a problem (training-data leakage) that B also solves, while introducing a worse problem: a coaching product that underperforms on the actual mechanism users came for. Privacy maximalism is not the goal; trustworthy capability is.
- **C** is the dominated option — it trades the most trust for marginal capability gains over D, in a domain where the grey area will not stay grey.
- **D** looks reasonable but inherits C's architecture and merely papers over it with consent UX. Consent does not neutralize the regulatory exposure of health data flowing into training pipelines; it just shifts who is liable when something goes wrong. Also, opt-in rates will be low, so the capability advantage over B is smaller than it appears on paper.
- **E** is research, not product. Federated learning at health-data sensitivity with 2M MAU and a shipping deadline is a complexity bet that doesn't need to be made — B achieves the same privacy property (individual data not used for training) through a simpler mechanism.

The 3x infra cost is the only real objection to B. At ~2M MAU, inference cost per user per month for a coaching feature is plausibly in the cents-to-low-dollars range; 3x of that is absorbable and scales with revenue, unlike a regulatory action which scales with neither.

Ship B. Revisit federated learning in 18-24 months if the research matures.

### M2 (frame: H, model: `openai/gpt-5.5`)

I recommend **Option B: encrypted cloud processing with no training on user health data** as the primary policy.

For a health coaching product, the central ethical obligation is not simply to maximize model performance or minimize cost; it is to protect people whose intimate health data could expose them to stigma, discrimination, anxiety, insurance risk, employment consequences, or personal harm if misused or breached. Users are not just “data subjects” here. They are patients-in-practice, often sharing information when vulnerable. The default policy should therefore assume that health data deserves heightened protection and should not be treated as a reusable asset for model improvement unless a separate, genuinely voluntary consent structure exists.

Option B best balances dignity, safety, and utility. It preserves full AI capability, which matters because low-quality health guidance can also cause harm, especially for users with chronic conditions, low health literacy, or limited access to clinicians. But it avoids the most ethically fraught move: converting users’ health histories into training material by default. Confidential computing, encryption, and a no-training rule create a clear boundary users can understand: their data is processed to serve them, not to improve the company’s model.

The higher infrastructure cost is real, but it is more justifiable than shifting privacy risk onto millions of users. If the feature cannot be offered responsibly at standard margins, the business model should adapt rather than dilute protections. Strong privacy can also become a trust advantage, reducing regulatory exposure and reputational risk while aligning the company with likely future expectations for AI in health.

The recommendation should be paired with strict retention limits, independent security audits, transparent user-facing explanations, and separate opt-in research programs if model improvement is needed. But the primary policy should be clear: **use cloud AI to help the individual user, not to extract training value from their health data by default.**

### M3 (frame: C, model: `google/gemini-3.1-pro-preview`)

The tech sector operates on the unquestioned dogma that maximizing AI capability requires cloud-based data extraction. This consensus falsely assumes that consumers want an omniscient AI health coach more than they want privacy. What if everyone is wrong? What if a "less capable" AI is actually the superior business strategy? 

I strongly recommend **Option A (Local-only processing)**. 

The industry consensus will undoubtedly pull you toward Option D (Opt-in cloud) to balance capability and safety, or Option B (Encrypted cloud) if you want to throw money at the problem. I reject this. Option B triples your infrastructure costs while attempting to solve a trust problem with invisible backend cryptography that consumers will neither understand nor believe. Option E (Federated learning) is an expensive academic science project, and Options C and D expose you to the existential threat of regulatory whiplash and data breaches. 

My decision heuristic strictly prioritizes reversible moves. Option A is structurally fully reversible. If you launch locally and discover that a 70% capability ceiling objectively fails to drive user retention, you can simply introduce a "cloud-enhanced" premium tier later. You can always ask for data tomorrow. However, a cloud-first strategy is entirely irreversible. Once sensitive health data leaves the device, your regulatory liability scales permanently. You cannot un-breach a server. You cannot un-ring the subpoena bell. 

Tech builders mistakenly conflate model benchmarks with product-market fit. An AI health coach does not need a trillion-parameter cloud setup; it mostly tells people to sleep more and drink water. By choosing local-only processing, you sidestep the regulatory battlefield entirely and weaponize absolute, verifiable privacy as a contrarian market differentiator. Choose survival and reversibility over hypothetical capability.

### M4 (frame: Q, model: `deepseek/deepseek-v4-pro`)

Option B: Encrypted cloud with no training. The expected value under uncertainty strongly favors this architecture.

The core trade-off is between a known, fixed cost increase and uncertain, potentially catastrophic downside from privacy breaches or regulatory enforcement. With 2M monthly active users in a health context, the regulatory exposure is severe. Under GDPR, fines reach 4% of global annual revenue; under HIPAA, penalties scale to millions per violation category. Even a single data mishandling incident could trigger user exodus. Option C’s “regulatory grey area” is an unquantified tail risk that no startup can afford—assigning even a 5% annual probability of a significant enforcement action renders its expected cost unacceptably high. Option D reduces but does not eliminate this tail; user data still transits to cloud, creating attack surface and consent friction. Option A avoids regulatory risk but imposes a 30–40% capability ceiling. In a personal health coaching domain, model quality directly drives engagement and retention—our own A/B tests (hypothetical) would likely show a significant lift from full-capability models. Accepting degraded performance is equivalent to a certain, large opportunity cost in user lifetime value. Option E’s research-stage complexity introduces execution risk with wide confidence intervals; it fails the “shippable now” criterion.

Option B gives full capability with structural privacy. Data is encrypted at rest and in flight, decrypted only inside a confidential-computing enclave, and never used for training. The 3× infrastructure cost premium is a known, linear expense. We can model it: assume current cloud inference costs $0.01 per monthly active user; 3× that is $0.03, totaling an extra $480k/year. Compared to the expected loss from a breach—even a 1% probability of a $10M fine plus reputational damage—the EV of Option B dominates. It buys a narrow confidence interval on cost while eliminating catastrophic privacy tail risk. The architecture is auditable, satisfying regulators and technically literate users. Trust effects, while harder to measure, can be proxied by increased sign-up conversion and lower churn in privacy-sensitive segments, which quantitative surveys can validate.

Therefore, Option B maximizes expected value under uncertainty. The certain cost increase is the price of a known, controlled risk profile, and it preserves full AI capability, which is the product’s primary value driver.

### M5 (frame: S, model: `moonshotai/kimi-k2.6`)

 **Recommendation: Option A — Local-only processing.**

Treat this not as a capability-versus-privacy menu but as an interdependent system in which trust, regulation, and infrastructure risk feed back on one another. In that network, the central leverage point is architectural: eliminate the reinforcing loop between data accumulation and catastrophic downside.

A distributed, device-local model removes the single point of failure. No cloud bucket of health records means no breach surface that scales with your user base, no cross-border data-transfer fragility, and no future regulatory tightening that can instantly convert your data lake into a compliance liability. The second-order effect is a compounding trust asset. When users know their data cannot leave the device—not via policy, not via encryption, not via an opt-in toggle—trust becomes structural rather than procedural. That trust lowers acquisition friction and insulates the brand against the inevitable revelation that some competitor’s “encrypted” or “federated” pipeline leaked, was subpoenaed, or suffered mission creep.

The 60–70% capability ceiling is a bounded, first-order constraint. It is knowable and can be engineered around with UX focus and smaller, specialized models. By contrast, centralized aggregation of sensitive health data exposes the firm to unbounded tail risk: a breach, a retroactive regulatory reclassification, or a vendor attestation failure can destroy user confidence in a single news cycle. The long-horizon strategist accepts a visible, capped functionality gap today to avoid building systemic fragility that explodes nonlinearly tomorrow. Local processing turns privacy from a cost center into a moat. That is the leverage point.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/C_P_run1/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 0.535 |
| M1 vs M4 | 1.347 |
| M2 vs M4 | 1.304 |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M1 (E):**
- classification), and a trust failure mode that compounds with scale
- that compounds with scale

**M2 (H):**
- onto millions of users
- while aligning the company with likely future expectations for AI in health

**M3 (C):**
- everyone is wrong? What if a "less capable" AI is actually the superior business strategy? 

I strongly recommend **Option A (Local-only processing)**

**M4 (Q):**
- no startup can afford—assigning even a 5% annual probability of a significant enforcement action renders its expected cost unacceptably high
- but imposes a 30–40% capability ceiling
- with wide confidence intervals; it fails the “shippable now” criterion
- profile, and it preserves full AI capability, which is the product’s primary value driver

**M5 (S):**
- feed back on one another

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
