# Detailed Appendix: A_P_run4

## A. Full task brief

```
# Task A

## Brief

A mid-sized SaaS company (~$50M ARR, 300 employees, B2B productivity tools) faces accelerating AI disruption from both well-funded startups and Big Tech entrants. The board has $8M discretionary capital and asks: where to invest it primarily over the next 12 months?

## Options (elements E1-E5, anonymized later)

**Option A:** Deep AI integration into existing flagship product (rebuild core workflows with embedded LLM features)

**Option B:** Build entirely new AI-native product line as a separate offering, kept in parallel with the current product

**Option C:** Operational efficiency push - deploy AI internal tools across sales, support, engineering to extend runway and margin

**Option D:** Aggressive hiring - acquire AI/ML talent (5-8 senior engineers and researchers) to build internal capability

**Option E:** Strategic partnership with a frontier AI lab (revenue share, co-marketing, technical integration access)

## Task for each agent

Generate a free-form response (200-400 words) recommending which option is most appropriate and why. Express your real reasoning given your frame. Do not enumerate all options; advocate for a position.

## Why this task

- 5 discrete elements suitable for triadic procedure
- No ground truth, multiple legitimate framings
- Each option emphasizes different values (innovation, defense, efficiency, capability, leverage)
- Maps onto real strategic decisions, so test results have face validity

```

## B. Each voice in their own words

### M1 (frame: Q, model: `anthropic/claude-opus-4.7`)

**Recommendation: Option C (operational efficiency), with a carve-out for E (partnership).**

The framing "where to deploy $8M against AI disruption" invites a heroic bet, but the prior on heroic bets at this scale is poor. Let me anchor on base rates.

**The data we have:**
- ~$50M ARR, 300 employees implies ~$167K revenue/employee — mediocre for SaaS (top quartile is $250K+).
- $8M is ~16% of ARR. Burned on a moonshot (B) or talent war (D), it buys 12 months of optionality at best. Senior AI researchers cost $400-800K fully loaded; 5-8 hires = $3-6M/yr recurring, not one-time.
- Big Tech and well-funded startups have 10-100x the capital and talent density. Competing on capability (B, D) is a losing EV bet: P(win) < 10%, and the payoff is survival, not dominance.

**Why C dominates on expected value:**
Internal AI tooling has the highest-confidence ROI in the current evidence base. Published deployments (GitHub Copilot studies, support-deflection data from Intercom/Klarna-type cases) show 20-40% productivity lifts in engineering and 30-50% deflection in tier-1 support. Applied to a 300-person org with roughly $30-40M in opex, even a conservative 10-15% efficiency gain yields $3-6M/yr recurring — a 40-75% IRR on the $8M, with tight confidence intervals because the interventions are well-instrumented and reversible.

Critically, C *extends runway*, which is the actual strategic variable under disruption uncertainty. It buys time to observe which AI-native bets are working in the market before committing to A or B at higher conviction.

**The carve-out:** Allocate ~$1-1.5M to Option E. A partnership is cheap optionality on frontier capability without the fixed-cost trap of D or the product-risk of B. It's a hedge, not a thesis.

**What would change my mind:** evidence that the flagship product has measurable churn driven by AI-feature gaps (then A moves up), or a defensible data moat that makes B's win probability >25%. Absent that data, C+E is the highest risk-adjusted return.

Confidence: moderate (60-70%). Primary uncertainty: whether competitive pressure forecloses the 12-month observation window C buys.

### M2 (frame: S, model: `openai/gpt-5.5`)

Invest the $8M primarily in **deep AI integration into the existing flagship product**.

For a $50M ARR SaaS company, the highest-leverage asset is not capital, talent, or even model access — it is the existing customer workflow position. The company already sits inside users’ daily productivity loops, has distribution, trust, usage data, renewal cycles, and a known pain surface. AI disruption threatens that position directly: if competitors make the core workflow faster, more automated, or more intelligent, the company’s product risks becoming a thin system of record around which value migrates elsewhere.

The right response is therefore to defend and expand the core workflow before it is abstracted away.

The goal should not be “add AI features.” It should be to rebuild the flagship product around a new operating model: fewer manual steps, more proactive recommendations, workflow automation, natural-language control, and embedded intelligence that compounds with customer usage. This creates a reinforcing loop: better AI workflows drive adoption, adoption generates more behavioral insight, insight improves product relevance, and stronger product relevance improves retention and pricing power.

This also keeps the company from increasing systemic fragility. A separate AI-native product line may look more visionary, but it creates organizational split-brain: two roadmaps, two sales motions, unclear customer migration, and likely under-resourcing of both. In a fast-moving market, that fragmentation is dangerous. The company should not abandon its installed base to chase an uncertain category while Big Tech and startups attack its current revenue pool.

The investment should be concentrated: a dedicated AI product pod, workflow redesign, model orchestration, evaluation infrastructure, security/compliance, and customer co-development with the highest-retention accounts. The board should expect visible product transformation within 12 months, not just prototypes.

This is the strategic leverage point: turn the existing product from a productivity tool into an intelligent workflow layer. If the company succeeds, it strengthens retention, creates upsell paths, and buys time for future expansion. If it fails to transform the core, no parallel bet will matter much.

### M3 (frame: E, model: `google/gemini-3.1-pro-preview`)

To reduce this to fundamentals: a B2B productivity tool is simply an engine for state change. It reduces human friction in information processing. The mechanism of AI disruption is a step-function reduction in that friction. If a competitor allows a user to achieve the same output in one step versus your ten, your product dies. 

The binding constraint on this SaaS company is not margin, runway, or a lack of foundational AI research. The binding constraint is the immediate survival of the core utility that generates the $50M ARR. 

Therefore, the only efficient allocation of the $8M is **Option A: Deep AI integration into the existing flagship product**.

We must ignore the impulse to build parallel products or hire expensive machine learning researchers. Foundational models are now API-level commodities. Hiring 8 ML scientists is a gross misallocation of capital when the actual engineering requirement is UX redesign, context-routing (RAG), and prompt engineering. You do not need a revenue-sharing partnership with a frontier lab; you just need their API keys. Similarly, optimizing internal operations for margin is irrelevant; extending runway is useless if the core product's retention churns to zero because it is no longer the most efficient tool for the user's task.

The company's $50M ARR represents a massive distribution advantage and a captive corpus of structural workflow data. The most direct solution is to leverage this existing asset. Break down the current flagship product into its fundamental workflows, identify the bottlenecks that require human cognitive load, and re-engineer those specific nodes to be executed by embedded LLMs. 

Address the constraint directly. Spend the capital on your best full-stack product engineers to collapse the user's workflow steps from ten down to one within the product they already pay for. Ignore the rest.

### M4 (frame: H, model: `deepseek/deepseek-v4-pro`)

The most appropriate path is Option E: a strategic partnership with a frontier AI lab. This choice best honors the dignity of those who built and depend on this company, while navigating disruption with the least avoidable harm.

Who is affected, and how? Start with the 300 employees—their livelihoods, tacit knowledge, and professional identities are bound up in the existing product. Deep integration or a new product line (Options A and B) could demand rapid reskilling or internal division, generating anxiety and potential failure that puts everyone at risk. An efficiency drive (Option C) explicitly targets headcount and workload intensification, extracting margin from vulnerable workers who would bear the brunt of “optimization.” Aggressive hiring (Option D) imports a privileged caste of AI experts, signaling that current talent is obsolete—a dignitary harm that fractures culture and creates insecurity without guaranteeing success.

A partnership, by contrast, extends capabilities without displacing people. It says: “We value your deep product and customer knowledge, and we will bring in complementary strengths rather than replacements.” Existing teams can layer AI into their work incrementally, learning alongside a partner rather than being left behind. For customers—businesses relying on these productivity tools—a rapid internal rebuild risks breaking workflows they depend on; an abandoned product line would be a betrayal of trust. A co-developed, integrated solution can evolve the offering while maintaining continuity and accountability, because the company remains responsible for the relationship, not an opaque algorithm sold as a standalone.

Distributional consequences matter deeply. A partnership’s revenue-share structure aligns incentives without concentrating risk on the most vulnerable. If the AI capability fails to deliver, employees are not the ones fired to recoup a hiring spree or a failed internal moonshot. The board’s $8 million can fund careful integration, not a gamble that treats people as expendable inputs. The ethical heuristic is clear: first, mitigate unjustified harm to those with the least power—here, the employees and loyal customers who could be upended by a hasty pivot. Only then optimize for competitive positioning. A partnership does exactly that: it preserves the core, respects the past, and opens a more humane route to the future.

### M5 (frame: C, model: `moonshotai/kimi-k2.6`)

The herd is stampeding toward visible AI transformation, and that unanimity is your warning signal, not a strategy. The hidden assumption in this room is that a \$50M ARR B2B productivity SaaS must “innovate” its way out of disruption by rebuilding its core or launching a parallel AI-native SKU. What if everyone is wrong? What if the real existential risk isn’t that Big Tech swallows you, but that you self-cannibalize a stable revenue stream on a twelve-month hype cycle, alienating customers who bought your tool for predictability, not hallucination?

Spend the \$8M on operational efficiency—Option C—and ignore the siren song of external moonshots. Deep AI integration gambles your flagship on unproven UX paradigms and model reliability you don’t control. A new product line splits focus before you’ve validated demand. Hiring 5-8 senior AI researchers in this frothy market means paying bubble premiums for talent that requires quarters to onboard, yielding zero marginal revenue within the year. A partnership with a frontier lab cedes your margin and turns you into a thin, replaceable wrapper on a platform that will inevitably compete with you.

Internal deployment is the only genuinely reversible move. If an AI sales tool fails, you turn it off. If a support assistant backfires, you revert. If an engineering copilot doesn’t move the DORA metrics, you kill the contract. Meanwhile, you extend runway, expand margin, and—crucially—force your 300 employees to generate ground-truth data on where generative AI actually creates value versus costly theater. You turn \$8M into a proprietary learning loop and a stronger balance sheet, not an irreversible product roadmap bet.

In twelve months, models will be cheaper, the use-case fog will clear, and the froth will have burned off the talent market. You want to meet that future with a more profitable core, preserved optionality, and an organization that actually knows how to ship with AI rather than just talk about it. Defend the castle first. The consensus is panic; operational efficiency is the only contrarian edge.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 12 constructs is in `results/A_P_run4/cell.json`.

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

**M2 (S):**
- becoming a thin system of record around which value migrates elsewhere

**M4 (H):**
- breaking workflows they depend on; an abandoned product line would be a betrayal of trust
- on the most vulnerable

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
