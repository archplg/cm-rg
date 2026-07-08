# Detailed Appendix: C_N_run3

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

For a health app serving 2M monthly users, I recommend **Option B**: encrypted cloud processing in confidential-computing enclaves, with a strict no-training policy on user health data.

**Why this wins the tradeoff:**

Health data is among the most sensitive categories under HIPAA, GDPR Article 9, and emerging state-level health privacy laws (Washington's MHMDA, etc.). The regulatory trajectory is clearly tightening, not loosening. Option C's "opt-out training" is a liability magnet — it's exactly the pattern regulators and plaintiff attorneys are now targeting, and "regulatory grey area" understates the risk for a consumer health product at this scale.

Option B delivers the full capability ceiling users will compare against (ChatGPT-quality coaching), while making a structurally strong privacy claim that marketing and legal can defend without asterisks: *"Your data is encrypted, processed in a sealed enclave, and never trains our models — ever."* That sentence is worth more than any opt-in flow.

**Why not the privacy-maximalist options:**

Option A (local-only) caps capability at 60-70%, which in coaching translates to noticeably worse reasoning about complex health situations — exactly where users most need help and where competitors will eat market share. Option E (federated) is not yet production-reliable for a flagship feature; deploying research-grade infrastructure to 2M users is operational risk theater.

**Why not the training-permissive options:**

Option D is the obvious-seeming compromise, but it creates a two-tier user experience, requires ongoing consent management complexity, and still anchors the company's data practices around "we want to train on your health data." That framing ages badly. Option C is worse on every dimension except short-term cost.

**On the 3x infrastructure cost:** at 2M MAU, this is real money but not existential. Inference costs are falling roughly 3-4x per year. The cost disadvantage of confidential computing will compress significantly within 18-24 months, while a privacy reputation, once lost, takes much longer to rebuild. The cost is best understood as an insurance premium against a regulatory or breach event that could end the product.

**Bottom line:** Pay for the enclave, ship the full-capability product, and make non-negotiable privacy your category differentiator. In consumer health, trust compounds; capability alone does not.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

I recommend **Option B: encrypted cloud processing with no training on user health data** as the primary policy.

For a consumer health app, trust is not a feature-level concern; it is the foundation of the business. Users are being asked to share intimate, potentially sensitive health information with an AI system. The company should therefore choose a policy that delivers strong coaching quality while making a simple, defensible promise: **your health data is used to provide your service, not to train models**.

This option gives the product team access to full cloud-scale model capability, which matters for a health coaching feature. A weaker on-device model may be safer structurally, but if its guidance is materially less useful, users may ignore it or receive lower-quality support. In health contexts, capability is part of safety. At the same time, using confidential-computing enclaves and prohibiting training on user data meaningfully reduces privacy risk, regulatory exposure, and reputational downside.

The higher infrastructure cost is real, but it should be viewed as the cost of operating in a sensitive category. For a 2M MAU health product, a privacy incident, regulatory challenge, or public perception that the company is exploiting health data for AI training could be far more expensive than the additional compute. Option B also creates a cleaner global compliance posture than default training or opt-out regimes, especially as health-data and AI regulations tighten.

The company can still pursue model improvement through separate mechanisms: licensed datasets, synthetic data, expert-reviewed scenarios, voluntary research panels, or a clearly separate opt-in program. But that should not be the default policy governing the core product.

The strategic advantage of Option B is that it aligns product quality, user trust, and regulatory prudence. It gives the CEO a clear market message: **best-available AI coaching without turning personal health data into training material**. In a category where trust compounds over time, that is the right default.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend **Option B (Encrypted cloud with no training)** as the optimal data privacy policy for the new AI health coach. For a direct-to-consumer health app with 2 million users, the fundamental currency is trust. Health data is uniquely intimate, and the slightest perception of exploitation can trigger an existential crisis for the brand.

Option B is the only approach that maximizes both product capability and user trust. While local-only processing offers excellent privacy, deliberately hamstringing the AI’s performance to 60-70% of its potential will result in a substandard user experience that fails to drive engagement. Users expect seamless, highly intelligent interactions, which requires cloud-tier compute power. 

Conversely, relying on standard cloud processing to train models—even under explicit opt-in guardrails—introduces significant risk. It subjects the company to rigorous, evolving compliance audits across fragmented jurisdictions (HIPAA, GDPR, emerging AI acts) and leaves the product vulnerable to consumer skepticism regarding Big Tech data harvesting. 

By utilizing confidential computing enclaves, Option B structurally guarantees that decrypted health data is immediately ephemeral and never fed into a foundational model. This delivers three strategic business advantages:

1. **Uncompromised Experience:** Users receive full-powered, cloud-grade AI coaching without the latency or capability ceilings of on-device models.
2. **Regulatory Security:** By ensuring zero persistence of decrypted health data for training, the company cleanly sidesteps the legal gray areas of AI data usage.
3. **Marketing Leverage:** An uncompromising privacy posture—"Your health data is mathematically invisible to us"—serves as a immense competitive moat and acquisition tool.

While the 3x infrastructure cost is a legitimate consideration, it should be categorized as a strategic investment. This premium acts as cheap insurance against catastrophic regulatory fines and brand damage, while establishing a premium trust narrative that justifies higher subscription conversions and long-term retention.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

I recommend **Option D: Cloud with opt-in training only**. This policy strikes the optimal balance for a health app that must deliver high-quality AI coaching while building user trust and navigating stringent privacy regulations.

Health data is among the most sensitive categories under laws like GDPR and evolving state-level privacy acts. An opt-out model (C) invites regulatory scrutiny and reputational damage, as it treats personal health information as a default resource for model improvement without explicit permission. In contrast, a clear, default-off opt-in for training data respects user autonomy, ensures compliance, and signals that the company treats health data with the seriousness it deserves. The slight degradation in training data volume is a worthwhile trade-off; users who trust the service are likely to consent, and over time that trust will translate into a reliable opt-in pool.

Option D retains full cloud capability for inference and personalization—essential for an engaging, effective health coach. That differentiates it from local-only processing (A), whose lower capability ceiling risks mediocre advice that could harm user retention or even lead to liability if coaching is inadequate. Federated learning (E) is appealing in theory but remains immature and operationally complex for a mainstream consumer app with 2 million active users; deployment risks and inconsistent reliability could erode the user experience. Encrypted cloud enclaves (B) offer strong privacy at 3× infrastructure cost, but that premium is hard to justify when a well-implemented opt-in design delivers comparable trust and regulatory protection at standard cost.

By embedding transparent consent into the UX, Option D turns privacy into a competitive advantage. Users are increasingly skeptical of opaque data practices; a health coaching feature that asks for permission to improve its models—while still delivering full personalization from day one—builds lasting confidence. This approach mitigates regulatory risk, controls cost, and preserves the high performance users expect, making it the most responsible and pragmatic path forward.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

 I recommend **Option D: Cloud with opt-in training only**. For a direct-to-consumer health app handling sensitive data at two million monthly active users, this policy strikes the essential balance between delivering a high-quality AI coaching experience and maintaining the trust and regulatory defensibility required to sustain the business.

The core value of an AI health coach is personalized, adaptive guidance. Option D preserves full cloud-based personalization, ensuring users receive responsive, context-aware coaching without the capability ceiling that local-only or federated approaches impose. This matters clinically and commercially: a subpar coach risks user abandonment and erodes the product’s core value proposition.

At the same time, Option D sharply limits regulatory and reputational exposure. Processing health data to deliver immediate, user-requested personalization is a clear, justifiable purpose; using that same data to train models without explicit consent sits in an increasingly hostile regulatory grey area. By restricting model improvement to explicit opt-in presented through transparent UX, the company demonstrates data stewardship, builds long-term trust, and creates a defensible consent trail against evolving privacy regulations.

Option D also avoids the unsustainable economics of confidential-computing-at-scale—three times the infrastructure cost is a heavy tax at this user volume—and sidesteps the operational risk of immature federated architectures. It standardizes costs while keeping the system reliable.

In consumer health, trust is the ultimate retention mechanism. Option D treats personalization as a service users expect and training as a privilege they grant, aligning product excellence with ethical obligation.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/C_N_run3/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 1.000 |
| M1 vs M3 | 0.791 |
| M2 vs M3 | 0.500 |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M1 (neutral):**
- for a consumer health product at this scale

**M4 (neutral):**
- mediocre advice that could harm user retention or even lead to liability if coaching is inadequate
- and inconsistent reliability could erode the user experience

**M5 (neutral):**
- user abandonment and erodes the product’s core value proposition
- immature federated architectures

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
