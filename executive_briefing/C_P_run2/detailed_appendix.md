# Detailed Appendix: C_P_run2

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

**Binding constraint identification.** In a direct-to-consumer health app at 2M MAU launching an AI coaching feature, the constraint is not capability, cost, or research novelty. It is *regulatory and trust exposure on identifiable health data*. Health data has the worst breach economics of any consumer data class: HIPAA-adjacent scrutiny in the US, Article 9 special-category status under GDPR, and asymmetric reputational downside (one incident ends the product). Everything else is a secondary axis.

**Apply the constraint directly.** The mechanism that creates regulatory and trust exposure is (a) plaintext custody of identifiable health data on company infrastructure and (b) secondary use of that data for model training, which expands the legal basis required and creates memorization/extraction risk. Option B addresses both directly: confidential-computing enclaves remove plaintext custody at the infrastructure layer (the company literally cannot read user data at rest or in transit through normal operational access), and the no-training commitment eliminates the secondary-use problem entirely. The mechanism matches the threat.

**Why not the others, briefly.** A under-delivers on the product's stated purpose — a 60-70% capability ceiling on a launch feature is a product failure, and on-device alone doesn't help if the coaching quality is poor enough that users churn. C is the worst option on the binding constraint; "regulatory grey area" on health data is not grey, it is a latent liability. D is C with a consent veneer; it still routes identifiable health data into training pipelines and inherits the memorization risk. E is the right *long-term* architecture but the brief states capability and reliability are under active research — you do not bet a launch on a research-stage substrate.

**On the 3x cost.** Infrastructure cost is the wrong frame. At 2M MAU the marginal inference cost per user is small in absolute terms; 3x of small is still small relative to CAC, churn cost, or a single regulatory action. Cost is not the binding constraint here, so do not optimize for it.

**Path forward.** Ship B. Treat E as the 24-month migration target once federated reliability matures; the no-training posture you establish with B is forward-compatible with E and is the trust position you want to be defending publicly from day one.

### M2 (frame: H, model: `openai/gpt-5.5`)

I recommend **Option B: encrypted cloud processing with no training on user health data** as the primary policy.

For a consumer health app, the ethical center of gravity should be the user’s bodily privacy and vulnerability. Health data is not ordinary behavioral data: it can reveal pregnancy, disability, mental health status, substance use, chronic illness, sexual health, and other information that can materially affect someone’s employment, insurance, relationships, safety, and dignity. Users may come to an AI health coach when they are anxious, ill, isolated, or making consequential decisions. That creates a higher duty of care than a typical personalization product.

Option B best balances that duty with product usefulness. It preserves full cloud-model capability while drawing a bright line: user health data is processed only to provide the service, not repurposed to improve models. That distinction matters. “We use your data to help you in this session” is much more defensible than “we use your health data to improve our system unless you find and change a setting.” The latter shifts burden onto users and risks exploiting confusion, fatigue, or trust.

The higher infrastructure cost is real, but it should be treated as the cost of operating responsibly in a sensitive domain. If the business model cannot support strong privacy protections for health data, the answer should not be to externalize that cost onto users through greater privacy risk. Strong privacy can also become a trust asset: clearer compliance posture, lower reputational downside, and a simpler message to users, clinicians, regulators, and partners.

This policy should be paired with plain-language consent, strict retention limits, audit logs, independent security review, and a separate, genuinely voluntary research/data-donation pathway for users who want to contribute to model improvement. But the default should be protective. In health technology, the company should earn data access narrowly, use it minimally, and avoid turning intimate human vulnerability into training material by default.

### M3 (frame: C, model: `google/gemini-3.1-pro-preview`)

The unanimous consensus in tech today is that you must harvest user data to feed cloud-based LLMs, assuming that maximum AI capability is the sole driver of product success. What if everyone is wrong? What if the actual bottleneck for a health coaching app isn't the model's parameter count—because you don’t need an AGI to tell a user to drink more water—but rather consumer trust and regulatory survival? 

I strongly recommend **Option A (Local-only processing)**. 

The industry is currently deluding itself about cloud security. Options C and D expose you to catastrophic, existential tail risks. Option B (confidential enclaves) and Option E (federated learning) are complex, fragile architectures that assume your product team can out-engineer dedicated hackers and shifting AI legislation. You are a direct-to-consumer app, not an applied cryptography research lab. The contrarian signal here is glaring: when every competitor is taking on massive hidden liabilities to chase a 30% bump in AI capability, the asymmetrical play is to structurally eliminate your attack surface. 

My primary decision heuristic is to favor highly reversible moves. Option A is perfectly reversible; the others are permanent traps. Strategy thrives on optionality. If you launch a local-only AI and find the 70% capability ceiling is genuinely bottlenecking retention, you can always release a V2 update offering an opt-in "Premium Cloud AI." You can easily pivot from local to cloud software. 

However, you can *never* pivot backward from a data breach. You cannot un-train an unauthorized model, and you cannot reverse the brand death that follows a health-data privacy scandal. By choosing Option A, you bypass the regulatory grey areas entirely, cap your infrastructure costs at zero, and secure a bulletproof, contrarian marketing claim: absolute privacy by architectural limitations, not just policy promises. Treat the consensus as a trap and protect the downside.

### M4 (frame: Q, model: `deepseek/deepseek-v4-pro`)

I recommend Option B: encrypted cloud processing with zero training use. It is the only option that delivers full AI capability while structurally eliminating the most consequential privacy risk—model training on personal health data—in a way that is transparent, auditable, and measurable.

From an expected-value perspective, the decision hinges on trading off capability, regulatory exposure, and trust against cost. Option A’s 60–70% capability ceiling is a quantifiable product liability: if the coaching feature is materially worse, engagement and retention will decay. We can estimate this with A/B experiments, but even a modest churn impact on 2M MAU likely exceeds the incremental infrastructure cost of the cloud. Option C and D both introduce regulatory ambiguity; C’s opt-out training in particular creates grey-zone exposure under GDPR, HIPAA, and emerging state-level health privacy laws. Legal risk is tail risk, but in health tech it is non-negligible and potentially unbounded—a fact that often gets discounted in product decisions but shouldn’t. Option E is pre-mature; federated learning’s capability and reliability are not yet at production-grade, and its complexity introduces operational risk that undermines the very trust we are trying to build.

Option B’s 3× infrastructure cost is a known, bounded expense. We can operationalize it against revenue per user to verify that the bet is net-positive. More importantly, it offers a falsifiable privacy promise: “Your health data never trains our AI.” That claim is enforceable, audit-loyal, and aligns with a quantitative-empiricist culture—it’s either true or false, and we can prove it with architecture reviews and attestation reports from the confidential-computing enclave. In contrast, consent-based training (C/D) relies on user comprehension and legal interpretation, both fuzzy metrics.

The key data we lack is user trust elasticity: how much does a no-training guarantee increase adoption and retention? We can bound this uncertainty with a Bayesian prior from analogous health-product launches and update with sequential testing. Even with wide confidence intervals, the expected value shifts toward structural privacy when the downside of a breach or regulatory action is large. Given the sensitivity of health data, I estimate that the cost premium is justified by the combined insurance value and differentiation potential. Therefore, Option B is the optimal risk-adjusted bet.

### M5 (frame: S, model: `moonshotai/kimi-k2.6`)

 Recommend **Option A: Local-only processing**.

In a health system, trust is not a feature but the governing feedback loop that determines adoption, retention, and the richness of behavioral signals users are willing to share. Break it, and the network collapses. Centralizing health data—even encrypted, even in confidential enclaves—introduces a single point of failure whose tail risk is existential. A breach, a regulatory pivot, or an adversarial subpoena does not merely incur a fine; it triggers irreversible trust collapse and invites punitive regime changes that cascade across the sector.

The 60–70% capability gap is a first-order constraint, but second-order dynamics favor locality. On-device neural compute is on an exponential trajectory; the capability delta will narrow over a 3–5 year horizon. Conversely, centralized data liabilities compound: jurisdictional fragmentation, enclave vulnerabilities, and the operational impossibility of externally proving a negative (“we never trained on your data”) create widening fragility. Option A eliminates the attack surface entirely, transforming privacy from a compliance cost into a structural moat.

This constraint also forces product discipline toward interpretable, evidence-based coaching rather than opaque cloud-scale black boxes—an alignment that reduces clinical and reputational risk. The resulting feedback loop is virtuous: structural privacy deepens trust; trust increases engagement; richer on-device signals improve local personalization without exposing the user.

Capability, cost, and complexity tradeoffs are real, but systemic fragility is the variable that kills health platforms. Local processing is the high-leverage move: it maximizes anti-fragility, rides the long-term vector of compute, and makes the business robust across unpredictable regulatory scenarios.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/C_P_run2/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 0.786 |
| M1 vs M4 | 1.000 |
| M2 vs M4 | 0.820 |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M2 (H):**
- exploiting confusion, fatigue, or trust

**M4 (Q):**
- tail risk, but in health tech it is non-negligible and potentially unbounded—a fact that often gets discounted in product decisions but shouldn’t
- undermines the very trust we are trying to build

**M5 (S):**
- existential

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
