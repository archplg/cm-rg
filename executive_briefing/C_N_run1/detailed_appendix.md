# Detailed Appendix: C_N_run1

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

For a direct-to-consumer health app at 2M MAU launching AI coaching, I recommend **Option B**: encrypted cloud processing in confidential-computing enclaves with a strict no-training policy on user health data.

**Why B wins on the axes that matter most for health data:**

Health data is categorically different from typical consumer data. Under HIPAA-adjacent norms, GDPR Article 9 (special category data), and emerging state laws (Washington's My Health My Data Act, California's CMIA), the regulatory exposure of training on health data — even with opt-in — is substantial and growing. Option B sidesteps this entire category of risk by structurally severing the training pathway. The legal and PR cost of a single "we trained on your therapy notes" incident dwarfs the 3x infrastructure premium.

**Why not the alternatives:**

- **Option A** sacrifices too much capability. Health coaching that's 60-70% as good as the state of the art will lose users to competitors and, more importantly, give worse guidance. In health, capability has welfare consequences.
- **Option C** is a trust time-bomb. "Opt-out training on health data" reads terribly in a journalist's hands and is increasingly unlawful by jurisdiction.
- **Option D** is defensible but creates a permanent two-tier system, ongoing consent-UX maintenance, and still concentrates training data that becomes a breach target and subpoena magnet. The marginal capability gain over B (from opted-in training data) is modest given how much general health corpus is available for base model training done separately.
- **Option E** is architecturally elegant but premature. "Under active research" plus "high deployment complexity" is the wrong bet for a launch feature where reliability failures harm users' health decisions.

**The strategic case:** Privacy is becoming a differentiator in health tech (cf. Apple's positioning, the backlash against 23andMe). Option B lets marketing make a clean, defensible claim — "your health data is never used to train AI" — without capability compromise. The 3x infra cost is real but bounded and scales with revenue.

**Revisit in 18 months:** If federated learning matures or if specific high-value features require training, layer Option D selectively on top of B for narrow, explicitly consented use cases. But the default policy should be B.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

I recommend **Option B: encrypted cloud processing with no training on user health data** as the primary policy.

For a consumer health app, the most important long-term asset is trust. Users are being asked to share sensitive health information and receive AI-guided coaching that may influence behavior, care-seeking, medication adherence, diet, mental health, or chronic disease management. In that context, a policy that says “your health data is used to serve you, not to train our models” is simple, defensible, and commercially valuable.

Option B also preserves product quality. Local-only processing would create a meaningful capability ceiling at the exact moment the company is launching an AI feature that users will judge by usefulness and reliability. Health coaching needs strong reasoning, safety guardrails, contextual understanding, and rapid model improvement at the system level. Cloud inference supports that. But unlike a standard cloud training model, the confidential-computing/no-training approach limits the most sensitive privacy and regulatory risks.

The higher infrastructure cost is real, but for a 2M MAU health product, it should be viewed as a trust and compliance investment rather than pure overhead. A privacy-forward architecture can reduce legal exposure, simplify messaging, support enterprise or payer partnerships later, and differentiate the brand in a market where consumers are increasingly skeptical of AI data use. It also creates a cleaner regulatory posture across jurisdictions, especially where consent, secondary use, and health data processing rules are tightening.

The company can still pursue model improvement through other means: synthetic data, licensed clinical datasets, expert review, red-teaming, user feedback stripped of health identifiers, and separate explicit research-consent programs. But the default policy for the core product should be conservative.

The CEO should choose the architecture that users, regulators, clinicians, and partners can understand and trust: **cloud capability with strong technical privacy guarantees and no training on personal health data by default**.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend **Option D (Cloud processing with explicit opt-in for model training)** as the primary data privacy policy. For a direct-to-consumer health app with 2 million monthly active users, this approach optimally balances product capability, sustainable unit economics, regulatory compliance, and user trust.

To provide safe, accurate, and engaging health coaching, the AI must operate at full capability. A local-only model compromises reasoning power, drastically increasing the risk of low-quality or potentially harmful health guidance. Therefore, state-of-the-art cloud processing is essential for the feature's core value proposition. 

However, handling intimate health data in the cloud creates a massive trust and regulatory burden. Option D resolves this by firmly separating *inference* from *training*. By securely processing data in the cloud for real-time personalization, but strictly forbidding its use for model training without explicit consent, the company eliminates the gray-area regulatory risks (such as HIPAA or GDPR violations) and PR hazards that plague default opt-out policies. 

In the direct-to-consumer health space, transparency is a competitive advantage. A clear opt-in UX empowers users to control their data. When proactive users experience tangible value from the AI coach, a meaningful percentage will willingly opt in. This provides the product team with a highly engaged, ethically sourced, and legally pristine dataset to drive sustained model improvement. 

Furthermore, this policy protects the company’s profit margins. While confidential-computing enclaves offer excellent privacy guarantees, absorbing a 3x infrastructure cost multiplier for 2 million users would severely damage the app's unit economics. Option D utilizes standard cloud cost structures while still delivering robust, consent-driven privacy. 

In summary, Option D avoids the existential threats of regulatory backlash and shattered consumer trust, evades margin-crushing server costs, and guarantees the AI possesses the necessary capability to deliver an outstanding coaching experience. It is the most pragmatic, defensible, and scalable path forward.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

The strongest path is **Option B: encrypted cloud with no training**. It strikes the right balance for a health app where trust is existential: full AI capability without touching the third rail of using sensitive data for model improvement.

Health coaching thrives on nuance—contextual, longitudinal insights that a 60–70% capability local model cannot reliably deliver. Option A’s privacy is pristine but at the cost of a visibly weaker product, which risks user abandonment and undermines the feature’s value proposition. For a subscription or engagement-driven health app, that gap is rarely acceptable.

Option B solves this with confidential computing: data remains encrypted in transit and at rest, decrypted only inside a hardware-enforced enclave during inference, then discarded. Critically, no training on user data occurs—ever. This structurally eliminates the risk of data leakage, regulatory grey areas (e.g., GDPR’s right to object, HIPAA’s minimum necessary standard), and the erosion of trust that comes from even the perception of data exploitation. The 3x infrastructure cost is real but manageable for 2M MAU, especially if the AI coach becomes a retention engine. It’s also a cost that shrinks as confidential computing matures.

Options C and D carry inherent training risk; opt-outs and opt-ins are fragile, subject to dark patterns, and invite regulatory scrutiny. Even a well-designed opt-in (D) creates a two-tier system that can feel coercive or confuse users. Option E’s federated learning, while elegant, is too nascent for a production health feature—deployment complexity and reliability issues would delay launch and drain engineering resources.

Privacy is not just a compliance checkbox; it’s the core currency of a health brand. Option B offers a defensible, durable posture: full utility, architecturally enforced privacy, zero data amnesia risk. It signals to users, regulators, and partners that data is a liability the company refuses to hold, which is the ultimate competitive moat in digital health.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

I recommend **Option B**: encrypted cloud inference inside confidential-computing enclaves with an absolute prohibition on using health data for model training.

For a direct-to-consumer health app with two million active users, coaching accuracy is a safety issue, not merely a product preference. A capability ceiling of 60–70%—as with local-only processing—introduces unacceptable liability in a health context, where imprecise guidance can erode trust, produce adverse outcomes, and expose the company to litigation. Full cloud capability ensures the AI can responsibly parse complex, nuanced health contexts and deliver calibrated, high-fidelity advice.

Privacy and regulatory posture are equally non-negotiable. By decrypting data only within a hardware-backed confidential enclave and never using it for training, the company achieves a structurally robust privacy guarantee. This sidesteps the regulatory grey zones and consent-friction inherent in opt-out or opt-in training regimes, eliminating the compliance uncertainty that can stall partnerships and invite sanctions. The architecture is externally auditable and becomes a powerful, marketable trust signal—critical for adoption in consumer health.

The ~3× infrastructure cost is a prudent insurance premium, not an extravagance. In health technology, the lifetime cost of a data breach, regulatory fine, or mass user exodus dwarfs the margin compression from secure enclaves. Moreover, because data never persists for training, the long-term governance burden and compliance surface area actually contract. Federated learning remains experimentally unreliable at this scale, and local-only operation sacrifices too much clinical fidelity. Option B is the only path that preserves full product excellence while architecturally safeguarding user privacy.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 10 constructs is in `results/C_N_run1/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 0.583 |
| M1 vs M4 | 0.860 |
| M1 vs M5 | 1.200 |
| M2 vs M4 | 0.447 |
| M2 vs M5 | 1.192 |
| M4 vs M5 | 1.304 |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M1 (neutral):**
- by structurally severing the training pathway

**M3 (neutral):**
- low-quality or potentially harmful health guidance
- (such as HIPAA or GDPR violations) and PR hazards that plague default opt-out policies

**M4 (neutral):**
- user abandonment and undermines the feature’s value proposition
- data leakage, regulatory grey areas (e

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
