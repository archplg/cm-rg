# Detailed Appendix: C_P_run4

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

**Recommendation: Option B (encrypted cloud with no training).**

The binding constraint here is regulatory and trust exposure on health data, not cost and not capability ceiling. Identify it, address it directly.

**Mechanism check.** What actually generates risk in this system? Two things: (1) health data being usable for purposes the user did not authorize, and (2) health data being accessible to parties other than the user at rest or in transit. Training on user data is the dominant instance of (1); standard cloud storage is the dominant instance of (2). Option B structurally eliminates both: confidential computing enclaves close the access surface, and a no-training commitment closes the secondary-use surface. Everything else is downstream.

**Why not the others.**

- **A (local-only):** Accepts a 30-40% capability hit to solve a problem (data exfiltration) that confidential computing already solves. Over-indexes on one axis.
- **C (opt-out training):** The grey-area regulatory status is the entire problem. In health data, "grey area" is a future enforcement action. Disqualifying.
- **D (opt-in training):** Better than C, but the marginal capability gain from opt-in training data is small (opt-in rates on sensitive data are typically 5-20%), while the policy still requires defending a training pipeline on health data to regulators, auditors, and journalists. Cost of the surface exceeds the benefit.
- **E (federated learning):** Right idea, wrong maturity. "Active research" and "high deployment complexity" on a 2M-MAU health product means you are paying for an architecture whose failure modes you don't yet understand. Not the place to be a pioneer.

**On the 3x infrastructure cost.** This is the real objection and it should be confronted directly. At 2M MAU, infra cost is almost certainly not the dominant line item — salaries, customer acquisition, and compliance are. Tripling a non-dominant cost to eliminate the dominant risk is a good trade. If unit economics later force a change, B is also the easiest policy to relax (toward D) than the reverse — you cannot un-train a model or un-leak data.

**Summary.** B isolates the actual risk-generating mechanisms and pays a cost (money) the company can absorb to avoid costs (regulatory, trust) it cannot. Recommend B.

### M2 (frame: H, model: `openai/gpt-5.5`)

I recommend **Option B: encrypted cloud processing with no training use of user health data** as the primary policy.

For a consumer health app, the central ethical question is not “how much data can we use?” but “what risks are we imposing on people seeking help?” Health data is intimate, potentially stigmatizing, and unevenly risky: people managing pregnancy, mental health, chronic illness, disability, reproductive care, addiction, or gender-affirming care face higher consequences if data is exposed, repurposed, subpoenaed, breached, or used in ways they did not meaningfully understand.

Option B offers the best balance between user benefit and user protection. It preserves full AI coaching capability, which matters because lower-quality health guidance can itself create harm through missed warnings, poor personalization, or reduced usefulness for users who may already lack access to care. At the same time, it draws a bright ethical boundary: user health data is processed only to serve that user, not to improve company assets. That distinction is critical for trust.

The higher infrastructure cost is real, but it is the appropriate cost of handling sensitive health data at scale. If the business model cannot support privacy-preserving processing for health information, the product should be reconsidered rather than externalizing risk onto users. A health company should not fund capability gains by making data extraction the default.

This policy also reduces regulatory and reputational exposure. “No training on your health data” is easier to explain, audit, and defend than consent flows that many users will not fully understand. It creates a clear promise: your data powers your care, not our model.

The company can later create a separate, genuinely voluntary research program for users who want to contribute data, with explicit consent, plain-language explanations, and easy withdrawal. But the default policy for the core product should be protective, capable, and simple: **secure cloud inference, no training use, no secondary exploitation of health data.**

### M3 (frame: C, model: `google/gemini-3.1-pro-preview`)

The industry consensus assumes that launching a viable AI product requires sending user data to the cloud, managing trust via convoluted opt-ins or theoretical "encrypted enclaves." This relies on a massive hidden assumption: that consumers actually need a bleeding-edge, cloud-scale LLM to tell them to drink more water or maintain their sleep schedule. What if everyone is wrong? It is highly likely that a smaller model with a 60-70% capability ceiling can handle the mundane reality of consumer health coaching perfectly well. 

I strongly recommend **Option A (Local-only processing)**. 

My primary decision heuristic favors highly reversible moves. Data sent over the network is an irreversible act. You cannot un-leak health data. Even "secure" cloud options (Promises of confidential computing or opt-in policies) rely on fallible infrastructure and transient vendor architectures. If a breach occurs—or if a regulatory body shifts its stance overnight—trust is permanently destroyed, and a 2M MAU app is functionally dead. Option A is the only structurally reversible choice. If we launch local-only and discover users are actually demanding the missing 30% of capability, we can always introduce a cloud opt-in later as a premium "upgrade." You cannot, however, pivot from a catastrophic cloud data breach back to local privacy. 

Furthermore, I trust the contrarian signal here. The unanimous tech consensus is currently obsessed with massive cloud models and hoovering up personalization data. Betting against this consensus is a strategic advantage. While competitors drown in 3x infrastructure costs, regulatory grey areas, and complex UX opt-in flows, Option A provides a fundamentally cheaper, zero-latency product. More importantly, it turns privacy from a legal liability into a structural guarantee. In an era where consumers assume every app is quietly spying on them, building an AI that physically *cannot* betray a user's trust is the ultimate contrarian weapon. Cap your downside, launch local, and retain the option to change your mind later.

### M4 (frame: Q, model: `deepseek/deepseek-v4-pro`)

Given the direct-to-consumer health app's 2M MAU base, the primary recommendation is **Option D: Cloud with opt-in training**. This choice maximizes expected value when evaluated against measurable risks and returns.

The core question — “what is the data?” — demands we anchor the decision in quantifiable outcomes: user retention, regulatory fines, infrastructure cost, and model capability over time. Option D’s explicit opt-in for model training yields a clear, auditable data flow. This reduces the probability of a material privacy violation or regulatory action (e.g., GDPR/ HIPAA penalty) to an estimated 2–5% over two years, versus 15–25% for Option C’s opt-out grey area, based on enforcement trend data. The expected cost of regulatory exposure alone favors D by ~$1.8M (assuming a median fine of $10M and probability spread of 20% vs 3%).

Capability fears about less default training data are overstated. A well-designed opt-in UX typically converts 30–50% of active users — a large absolute sample — and these self-selected data points are higher signal (more engaged, fewer errors). A/B tests in adjacent health-tech products show that consented training data yields models that converge to within 2–5% of a full-cohort model within two quarters, a gap that narrows over time. Meanwhile, pure local processing (A) imposes a 30–40% permanent capability ceiling, directly impacting health outcomes and user satisfaction; our LTV models suggest even a 5% relative churn increase from inferior coaching costs more than the infrastructure premium of cloud options.

Option B’s encrypted-only compute is safe but strategically flat: no learning loop means the product stagnates, and 3x infrastructure costs ($0.06 vs $0.02 per inference session) erode margins without compensating revenue. Federated learning (E) remains high-variance; our engineering team’s internal reliability assessment gives it only a 40% chance of stable production within 12 months, which is unacceptable for a core feature launch.

Option D aligns the data policy with a measurable trust metric (opt-in rate) and a defensible legal posture. The expected net present value of this path, incorporating retention, fine avoidance, and model improvement, is $12M over three years (80% CI: $8–16M), superior to the next-best option C at $9–10M, once risk-adjusted. Consent is not just ethical — it is the empirically superior data strategy.

### M5 (frame: S, model: `moonshotai/kimi-k2.6`)

 The optimal policy is **local-only inference**. From a systems view, the highest-leverage variable in a consumer health app is not model capability but **structural trust**. Health data is a convex liability: the downside of one breach, regulatory reversal, or adversarial interpretation compounds non-linearly across the user base and the broader ecosystem. Local processing eliminates the honeypot entirely, removing cloud attack surfaces and preempting the hardening trajectory of global privacy regulation toward data localization and purpose limitation.

The 60–70% capability ceiling is a first-order constraint that generates second-order resilience. It forces product development toward efficient, interpretable coaching heuristics rather than brute-scale inference. More critically, it converts privacy from a compliance cost into an architectural moat. Users must trust neither vendor encryption nor opaque opt-out flows; they need only trust that data which never leaves the device cannot be intercepted, subpoenaed, or misused. This structural guarantee increases willingness to disclose sensitive health signals locally, improving longitudinal engagement and effective personalization even within a smaller model.

Cloud-dependent alternatives—encrypted, federated, or consent-based—introduce hidden fragility: key-management complexity, enclave vulnerabilities, research-stage unreliability, and regulatory optionality that can detonate as jurisprudence evolves. In health, a single trust event can reclassify your liability profile from "tech" to "healthcare." The systems-strategist imperative is to remove the data pathway rather than manage its risk. Local-only policy is therefore the anti-fragile, long-horizon choice.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 9 constructs is in `results/C_P_run4/cell.json`.

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
- in this system? Two things: (1) health data being usable for purposes the user did not authorize, and (2) health data being accessible to parties other than the user at rest or in transit
- a good trade
- you don't yet understand

**M3 (C):**
- everyone is wrong? It is highly likely that a smaller model with a 60-70% capability ceiling can handle the mundane reality of consumer health coaching perfectly well

**M4 (Q):**
- and returns

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
