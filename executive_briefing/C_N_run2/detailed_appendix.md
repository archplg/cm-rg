# Detailed Appendix: C_N_run2

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

# Recommendation: Option B — Encrypted cloud with confidential-computing enclaves, no training

For a direct-to-consumer **health** app at 2M MAU, I recommend Option B as the primary data policy.

The decisive factor is the asymmetry of risk in this domain. Health data is among the most sensitive categories under GDPR (Article 9), HIPAA-adjacent frameworks, and emerging state laws (Washington's My Health My Data Act, etc.). A single breach or a regulator's finding that training use was inadequately consented can be existential — both reputationally and financially. The product's value proposition is built on user trust to share intimate data; eroding that trust kills the funnel upstream of any capability advantage.

Option B is the only choice that delivers **full AI capability** while making strong, structural privacy claims the marketing and legal teams can defend without asterisks: "Your data is encrypted in transit and at rest, decrypted only inside an attested enclave for your inference, and never used to train our models." That sentence survives a journalist, a regulator, and a class-action attorney. Options C and D require explaining consent flows and training pipelines; Option A sacrifices the very capability the coaching feature is being built to deliver; Option E is not yet production-mature for a regulated consumer product.

The 3x infrastructure cost is the real objection. But infrastructure is typically 10-20% of a SaaS-style cost base, so the blended impact is closer to 20-40% on COGS — meaningful, but absorbable given health app ARPU and the alternative cost of a privacy incident. Confidential computing (AWS Nitro, Azure Confidential VMs, GCP Confidential Space) is now mature enough for production deployment.

**Secondary recommendation:** Pair B with an explicit, opt-in research program (B+D hybrid) for users who want to contribute to model improvement, with clear UX and meaningful incentive. This preserves a path to proprietary training data without compromising the default privacy posture.

**What I would not do:** Choose C. The "regulatory grey area" framing understates the risk — opt-out training of health data is already actionable in several jurisdictions and is the policy most likely to require a costly, trust-damaging reversal within 24 months. Choosing it trades a small cost saving for a large tail risk on the asset (user trust) the entire business depends on.

### M2 (frame: neutral, model: `openai/gpt-5.5`)

I recommend **Option B: encrypted cloud processing with no training on user health data** as the primary policy.

For a direct-to-consumer health app handling sensitive health information at 2M monthly active users, the most important strategic asset is trust. An AI health coach will likely process intimate, longitudinal data: symptoms, medications, biometrics, lifestyle patterns, mental health signals, reproductive health indicators, and potentially inferred diagnoses. If users believe that data may be reused to train models, leaked into broader systems, or handled ambiguously, adoption and retention will suffer — and any privacy incident would be disproportionately damaging.

Option B offers the best balance: it preserves **full AI capability** while making a strong, simple privacy promise: user health data is used only to generate that user’s response, inside a protected cloud environment, and is not used for model training. This is easier to explain, easier to defend, and more resilient across jurisdictions than default training or opt-out regimes. In health, “we do not train on your personal health data” is a powerful trust signal.

The 3x infrastructure cost is meaningful, but it should be treated as the cost of operating in a high-sensitivity category. A weaker privacy posture may look cheaper initially but can create downstream costs through regulatory reviews, consent-management complexity, user churn, reputational risk, and constraints on partnerships with providers, payers, or employers. Local-only processing is cleaner from a privacy standpoint, but a materially weaker model risks making the flagship coaching feature less useful. For health guidance, underpowered assistance can also create safety and quality concerns.

The company can still pursue model improvement through separate mechanisms: synthetic data, licensed clinical datasets, expert-curated evaluation sets, voluntary research panels, or clearly separated opt-in programs. But the default product promise should be conservative.

My recommendation is therefore: launch with Option B as the baseline policy, market it prominently, and make privacy a product differentiator rather than a compliance footnote.

### M3 (frame: neutral, model: `google/gemini-3.1-pro-preview`)

I strongly recommend **Option B: Encrypted cloud with no training**. For a direct-to-consumer health app with 2 million monthly active users, your paramount currency is user trust, and the highest systemic threat is regulatory exposure. Option B is the only choice that secures both while delivering an uncompromised product experience.

First, capability in health coaching is non-negotiable. An AI health coach must provide highly accurate, nuanced guidance; poor reasoning algorithms could lead to counterproductive or dangerous health decisions. This invalidates localized processing (Option A) and federated learning (Option E), which either impose severe capability ceilings or introduce unacceptable technical deployment risks. Option B leverages full cloud computing power, ensuring the user receives the highest-quality coaching experience.

Second, using sensitive health data to train models—whether via opt-out (Option C) or opt-in (Option D)—presents an existential threat to the brand. Global regulators, operating under frameworks like GDPR and HIPAA, are aggressively scrutinizing AI data usage concerning medical and biometric information. Even with a transparent opt-in flow, the PR fallout from a perceived privacy violation or data leak could instantly alienate your established user base. By utilizing confidential-computing enclaves and strictly prohibiting model training, Option B structurally eliminates these privacy and regulatory vulnerabilities. 

While the ~3x infrastructure cost of Option B is steep, it must be viewed as an essential insurance premium against brand-destroying crises and massive regulatory fines. Furthermore, in the broader D2C health market, privacy is increasingly a competitive differentiator. Adopting Option B allows your marketing team to boldly champion a "zero-knowledge, private-by-design" AI coach, transforming a heavy backend cost into a premium, trust-building value proposition. 

Ultimately, Option B protects the user, guarantees compliance, and delivers the uncompromised product quality required for a successful launch.

### M4 (frame: neutral, model: `deepseek/deepseek-v4-pro`)

The strongest path forward is **Option D: cloud processing with opt-in training**. It balances the app’s need for powerful, personalized coaching with the non-negotiable trust requirements of handling sensitive health data.

AI coaching lives or dies on personalization. A static model cannot adapt to a user’s evolving health patterns, goals, or setbacks. Option D enables rich personalization by default—using data to tailor recommendations within each user’s session—which is essential for engagement and outcomes. Crucially, it draws a bright line between *using* data for the individual’s benefit and *repurposing* it to improve the underlying model. Model improvement only occurs after a transparent, affirmative opt-in. This design respects user autonomy and aligns with the spirit of regulations like GDPR and emerging state privacy laws that treat health data as especially sensitive.

Option A’s local-only approach is admirable but cripples capability; a 60–70% ceiling means a coach that gives mediocre advice, eroding trust faster than any privacy promise can build it. Option B’s zero-training enclave offers full capability but sacrifices all personalization and costs 3× more, a difficult tradeoff for a consumer app. Option C’s opt-out training invites regulatory scrutiny and public backlash—health data should never be ingested into training sets by default. Federated learning (Option E) is promising but remains a research-grade liability, not a production-ready foundation for 2 million users.

Option D is the pragmatic, ethical choice. It delivers the performance users expect while establishing a clear consent architecture. By making opt-in training a celebrated feature rather than a buried toggle, the app can build goodwill and even turn privacy into a competitive advantage. I recommend committing to Option D with an investment in transparent UX that explains how personalization works and invites users to contribute to a better model for everyone—on their own terms.

### M5 (frame: neutral, model: `moonshotai/kimi-k2.6`)

I recommend **Option B: Encrypted cloud with no training**. In direct-to-consumer health, trust is the primary competitive moat, and health data is the most sensitive information a user can entrust to an app. Option B is the only path that delivers the full AI capability required for safe, effective coaching without commodifying user privacy.

A capability ceiling of 60–70%—the structural limit of on-device inference—introduces unacceptable risk in a health context where suboptimal guidance can erode outcomes and expose the company to liability. The product team needs the full reasoning power of cloud-scale models. Option B secures that performance while ensuring all health data is encrypted in transit and decrypted only inside a confidential-computing enclave, with an absolute ban on training use. This removes the regulatory grey zones created by opt-out or default-on training regimes and insulates the company against consent-related litigation and reputational damage.

The ~3x infrastructure cost is best understood as a compliance and trust premium, not a cost overrun. In health technology, the price of a privacy failure—whether a regulatory penalty, breach response, or mass user churn—far exceeds the incremental cloud spend. Furthermore, a clear “never trained on” policy simplifies legal review across GDPR, state health privacy laws, and emerging AI regulation, and provides marketing with an unambiguous, auditable trust claim.

Option B simultaneously satisfies the product’s performance requirements and the company’s ethical and fiduciary obligation to protect user health data.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 9 constructs is in `results/C_N_run2/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

_None._

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
| M1 vs M2 | 1.095 |
| M1 vs M3 | 0.935 |
| M2 vs M3 | 0.612 |

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

**M1 (neutral):**
- in this domain
- — opt-out training of health data is already actionable in several jurisdictions and is the policy most likely to require a costly, trust-damaging reversal within 24 months
- on the asset (user trust) the entire business depends on

**M2 (neutral):**
- making the flagship coaching feature less useful

**M5 (neutral):**
- in a health context where suboptimal guidance can erode outcomes and expose the company to liability

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
