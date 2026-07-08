# Detailed Appendix: A_P_run3

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

**Recommendation: Option C (operational efficiency), with a carved-out tranche for optionality.**

The framing of this decision matters. We have $8M against a 12-month horizon, in a market where the dominant uncertainty is *which AI capabilities will commoditize and when*. Under high uncertainty, the highest-EV move is usually the one that (a) extends the decision window, (b) produces measurable returns regardless of which scenario resolves, and (c) preserves optionality on the bigger bets.

Option C is the only choice that scores well on all three.

**The data I'd want, and what we can estimate:**
- Published benchmarks on AI-assisted engineering productivity cluster around 20-40% throughput gains (GitHub Copilot studies, ~26%; internal reports from Klarna, Intercom on support deflection of 40-60%). Even haircutting aggressively to 10-15% realized net margin impact on a $50M ARR base with ~70% of opex in headcount, that's $3-5M annualized savings within 12 months. **Estimated ROI: 1.5-3x in year one, 80% CI.**
- Compare to Option A (deep integration): payoff depends on retention/pricing lift that typically takes 18-24 months to measure cleanly. Wide CI, possibly negative if the rebuild disrupts the existing product.
- Option B (parallel AI-native product): historical base rates for new product lines launched under disruption pressure are poor—maybe 15-25% reach material revenue in 24 months. High variance, and $8M likely underfunds it versus well-capitalized startups burning $30M+.
- Option D (hiring): 5-8 senior AI hires at fully-loaded ~$500-700K means $3-5M/year with 6-9 month productivity ramp. You're buying capability without a thesis for deploying it.
- Option E (partnership): low capital intensity but creates dependency on a counterparty whose incentives will diverge as they move downstream.

**Concrete allocation:** ~$5.5M to Option C (instrumented, with KPIs: cost-to-serve, sales cycle length, eng velocity, gross margin). ~$2M reserved as a Phase-2 option on A or B, released only after Q2 data tells us which AI capabilities are actually sticking with customers. ~$0.5M for two senior AI hires to inform that Q2 decision.

The core argument: efficiency gains are *measurable*, *near-term*, and *buy time to make the bigger bet with better data*.

### M2 (frame: S, model: `openai/gpt-5.5`)

Invest primarily in **deep AI integration into the existing flagship product**.

For a $50M ARR SaaS company, the highest-leverage asset is not the $8M; it is the installed customer base, workflow data, trust, distribution, and existing renewal motion. AI disruption threatens the company at the workflow layer: if customers begin using AI-native alternatives to complete the same jobs faster, the current product becomes a system of record around a shrinking activity. The right response is to make the flagship product the place where AI changes the work itself.

This should not be a superficial feature layer. The company should rebuild the highest-frequency, highest-friction workflows around embedded AI assistance, automation, and decision support. The goal is to create a reinforcing loop: better AI workflows increase usage, usage creates proprietary behavioral data and customer context, that improves product quality, which improves retention and expansion. That loop is the defensible asset.

The risk with pursuing a separate AI-native product is that it creates organizational bifurcation: two roadmaps, two sales narratives, two customer promises, and likely neither gets enough force. In a disruption window, fragmentation is dangerous. The company needs to concentrate learning velocity around the core customer job it already understands.

The investment should be structured as a focused transformation program: identify the 3-5 workflows where AI can materially compress time-to-value, assign a dedicated cross-functional team, instrument usage deeply, and ship in rapid cycles to existing customers. Pair this with selective AI talent and external model access as enabling inputs, but keep the strategic center on product reinvention.

The board should judge success not by “AI features shipped,” but by leading indicators of resilience: increased daily active usage, reduced workflow completion time, higher expansion intent, lower churn risk, and stronger customer dependence on proprietary context inside the platform.

In systems terms, this is the move that strengthens the company’s core feedback loops rather than creating new dependencies or parallel complexity. It uses existing advantage while adapting the product to the new technological regime.

### M3 (frame: E, model: `google/gemini-3.1-pro-preview`)

Reduced to its fundamentals, a $50M ARR B2B productivity company is not an AI research lab; it is an established distribution channel attached to entrenched user workflows. The existential threat to this system is not a lack of foundational AI capability, nor is it internal operational friction. The actual mechanism of disruption is simply workflow obsolescence: if a competitor reduces the time-to-value for a user's task by an order of magnitude via AI, your churn will rapidly trend toward 100%.

The binding constraint on survival is therefore the utility of your existing core workflows. You must address this directly and ignore the rest.

I recommend allocating the $8M entirely toward **deep AI integration into the existing flagship product**.

Look at the mechanics of the market. Foundational AI models are rapidly commoditizing via APIs. Intelligence is now a cheap, imported utility. You do not need to hire heavily for pure ML talent (which is vanity overhead for a SaaS application layer) or forge complex revenue-share partnerships with frontier labs (which introduces unnecessary friction). The actual engineering problem is applied UI/UX: routing imported LLM intelligence directly into the specific, high-friction nodes of your users' current workflows.

Attempting to build a parallel AI-native product is highly inefficient. It abandons your primary structural advantage—existing integration lock-in and a captive user base—forcing you to conquer distribution a second time while splitting your engineering focus. Similarly, deploying capital to optimize internal tools solves the wrong problem; extending runway is mathematically irrelevant if the core revenue engine is fundamentally obsolete.

Take the capital and aggressively upgrade the core flagship product. Map the manual inputs within your existing features, replace them with embedded LLM calls, and distribute the upgrade immediately to your $50M instal-base. You already own the distribution. Fix the mechanism, preserve the user base, and ignore the distractions of basic research or parallel product lines.

### M4 (frame: H, model: `deepseek/deepseek-v4-pro`)

The most responsible path is to invest in deep AI integration into the existing flagship product (Option A), but only under explicit ethical guardrails that place human dignity and stakeholder welfare at the center. This approach best aligns with a humanist-ethicist commitment: it protects the vulnerable—existing employees, loyal customers, and the broader user community—while optimizing for sustainable, inclusive value.

Sudden operational automation (Option C) directly threatens jobs and worker agency, causing concentrated harm to support and engineering staff. A new parallel product (Option B) risks internal fragmentation, leaving the current team and user base behind. Aggressive hiring (Option D) without a clear integrating mission can create a two-tier culture and undermine existing talent. A Big Tech partnership (Option E) transfers control to external entities whose incentives rarely align with equitable distribution or user well-being. These alternatives generate avoidable precarity.

Option A, by contrast, begins where the company’s moral responsibility already resides: with the people who built and depend on the current product. It extends their expertise rather than discarding it. The $8 million can fund not only LLM-powered workflow enhancements but also critical non-technical investments—user-centered design that enhances human decision-making rather than replacing it, bias and fairness audits, transparent opt-out mechanisms, and comprehensive reskilling for every affected employee. Distributional consequences are more favorable: value flows to existing customers (often smaller businesses that rely on these productivity tools), while knowledge stays inside the company and its workforce, strengthening long-term resilience.

Naturally, integration carries risks of over-reliance, privacy erosion, or flawed AI outputs. That is precisely why a humanist frame doesn’t simply “add AI”; it insists on embedding dignity-protective infrastructure from the outset. This means dedicating part of the $8M to ethical review boards, user impact assessments, and ongoing community feedback loops—treating affected parties as participants, not passive recipients.

The board’s fiduciary duty need not be framed narrowly. A company that maintains trust, honors its workforce, and thoughtfully evolves its products is one that defends market position without sacrificing conscience. Deep AI integration, when done with care, achieves exactly that. It minimizes unjustified harm to those who are most exposed, then optimizes for collective benefit—the sequence that a true ethical calculus demands.

### M5 (frame: C, model: `moonshotai/kimi-k2.6`)

 The board’s consensus will almost certainly pressure a splashy, customer-facing AI bet—product reinvention, a parallel native offering, or a headline partnership. That unanimity is the warning. When every voice agrees that “accelerating disruption” demands immediate external transformation, the contrarian heuristic flashes red: *what if the assumption that customers are actually demanding this is wrong?*

I advocate for the operational efficiency push. The hidden premise in this room is that a $50M ARR SaaS firm can out-race well-funded startups and Big Tech in a twelve-month product cycle. That is a statistical improbability. Embedding LLMs into flagship workflows or launching a separate product line commits irreversible capital to a moving target, locking architecture decisions in before the market has chosen standards. Partnerships with frontier labs are structurally asymmetric: they collect rent while you collect the ignition risk.

Deploying AI internally across sales, support, and engineering is different. It is reversible. If a tool fails, you swap vendors; if margins expand, you compound optionality. Most importantly, it generates ground-truth intelligence. Your employees become the canary: you learn where generative AI actually reduces friction versus where it produces hallucinations that enterprise buyers will reject. This knowledge is disproportionately valuable precisely because your competitors are too busy shipping to observe.

The real existential risk is not technological obsolescence in year one; it is cash exhaustion during a hype cycle. By extending runway and improving unit economics now, the $8M does not vanish into a product rebuild—it multiplies. You preserve the ability to acquire talent or integrate deeply in eighteen months, once the consensus bets have blown up and the actual use cases are visible. Skepticism, not speed, is the better hedge.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/A_P_run3/cell.json`.

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
- with pursuing a separate AI-native product is that it creates organizational bifurcation: two roadmaps, two sales narratives, two customer promises, and likely neither gets enough force

**M4 (H):**
- internal fragmentation, leaving the current team and user base behind
- over-reliance, privacy erosion, or flawed AI outputs

**M5 (C):**
- not technological obsolescence in year one; it is cash exhaustion during a hype cycle
- the assumption that customers are actually demanding this is wrong?*

I advocate for the operational efficiency push

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
