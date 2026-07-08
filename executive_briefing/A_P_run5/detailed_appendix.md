# Detailed Appendix: A_P_run5

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

**Recommendation: Option C (operational efficiency), with a carved-out tranche for Option E.**

The framing question is: what allocation maximizes expected value under high uncertainty, where "uncertainty" is doing real work? At $50M ARR with Big Tech and well-funded startups entering, the dominant risk isn't being insufficiently ambitious — it's running out of runway or margin before the competitive picture clarifies. $8M is roughly 16% of ARR; this is not enough capital to win a capability race.

The data I'd want, and what's available:

- **Internal AI efficiency deployments** have the most defensible ROI evidence. Published benchmarks show 20-40% productivity lifts in support (deflection rates), 15-30% in engineering (code completion), and meaningful sales conversion gains. These are measurable within 2-3 quarters with clear KPIs: cost-per-ticket, cycle time, gross margin. Call it a 70% probability of 1.5-3x return on the $8M within 18 months, with a tight confidence interval because the interventions are well-instrumented.

- **Option A (deep integration)** has higher ceiling but the base rate for "rebuild core workflows" projects shipping on time is poor (<40% historically for mid-sized SaaS), and LLM feature parity is rapidly commoditizing — meaning the differentiation half-life is short. Wide confidence interval, expected value possibly negative after opportunity cost.

- **Option B (parallel new product)** is the highest-variance bet. At 300 employees and $50M ARR, splitting focus typically destroys both products. I'd want to see a successful skunkworks track record before funding this; absent that, prior is unfavorable.

- **Option D (hiring)** — 5-8 senior AI researchers at current market rates burns $4-6M/year fully loaded and competes against labs offering $1M+ packages. Adverse selection risk is high.

- **Option E (partnership)** is cheap optionality. Allocate ~$1-1.5M to secure preferential access, co-marketing, and technical integration. Low downside, preserves flexibility.

**Proposed split: $6.5M to C, $1.5M to E.** Efficiency gains extend runway and improve margins — buying time and information. The partnership preserves a call option on frontier capability without committing to building it. Revisit allocation in 6 months with measured KPIs; this is a decision to keep reversible, not a thesis to marry.

Confidence: moderate. Key disconfirming evidence would be early signals that a competitor's deep-integration play is winning meaningful share — which would shift weight toward A.

### M2 (frame: S, model: `openai/gpt-5.5`)

Invest primarily in **deep AI integration into the existing flagship product**.

For a $50M ARR SaaS company, the highest-leverage asset is not the $8M capital pool; it is the installed customer base, workflow context, usage data, trust, integrations, and distribution already embedded in the current product. AI disruption is dangerous because it can rewire the workflow layer where customers form habits and perceive value. The defensive and offensive move is therefore to make the flagship product the place where those AI-native workflows emerge, rather than creating a parallel bet that competes for attention, talent, and go-to-market focus.

The strategic question is not “how do we add AI features?” but “how do we prevent the product’s core jobs-to-be-done from being abstracted away by someone else’s AI interface?” If Big Tech or startups can sit above the company’s workflow and turn the product into a database or commodity execution layer, the company loses pricing power. Deep integration fights that at the right layer: customer workflow ownership.

The $8M should fund a focused rebuild of the highest-frequency, highest-friction workflows: AI-assisted creation, summarization, automation, recommendations, and cross-tool orchestration where the company already has domain-specific context. The goal should be measurable changes in activation, retention, expansion, and time-to-value — not a generic AI veneer.

This path also creates reinforcing loops. Better embedded AI drives more usage; more usage generates more workflow data and feedback; better feedback improves product quality; stronger product quality protects retention and enables upsell. That compounding loop is more valuable than a separate speculative product or a broad internal efficiency program.

The risk is execution sprawl. The company should avoid “AI everywhere” and instead choose two or three core workflows where AI can make the product feel categorically better. If the flagship product does not become AI-native, the company’s existing revenue base becomes fragile. If it does, the company uses its current market position as a platform for renewal rather than treating disruption as an external side project.

### M3 (frame: E, model: `google/gemini-3.1-pro-preview`)

To survive disruption, we must reduce the firm's problem to its actual mechanism of value creation. A B2B SaaS product is essentially a state machine: it converts user intent into a completed business task. The current existential threat—AI disruption—is simply a structural reduction in the energy (time, clicks, cognitive load) required to achieve that state. If a competitor requires less energy to process the same intent, the system will lose users. 

Therefore, the binding constraint is the immediate obsolescence of the current user experience. The company’s sole systemic advantage over Big Tech and startups is its installed base and the integration inertia of $50M ARR. 

The most efficient allocation of the $8M is **Option A: Deep AI integration into the existing flagship product.** 

By rebuilding core workflows with embedded LLMs, we address the constraint directly. We lower the friction of the existing state machine, exploiting the sunk cost of user familiarity. Users do not want to migrate systems; they migrate only when the energy disparity becomes intolerable. Fixing our current workflows neutralizes that disparity.

The alternative options misidentify the constraint or rely on flawed analogies. An internal efficiency push (Option C) preserves margin but ignores the product obsolescence driving top-line churn. Hiring expensive ML researchers (Option D) solves for the wrong variable; "intelligence" is now a commoditized utility available via standard APIs. The required mechanism is data routing and UX orchestration, not foundational model training. Building a parallel AI-native product (Option B) voluntarily abandons our distribution advantage and embraces a cold-start problem. Finally, a strategic partnership (Option E) is a mere analogy for action—it does not alter the code or the user's mechanical experience. 

Do not try to become an "AI company." The literal engineering task is to prevent current workflows from breaking due to competitive friction. Deploy the capital to re-wire existing user paths with commodity models. Fix the constraint, and ignore the rest.

### M4 (frame: H, model: `deepseek/deepseek-v4-pro`)

I recommend Option D: aggressive hiring of AI/ML talent to build internal capability. This choice follows directly from the humanist-ethicist imperative to first minimize unjustified harm to the most vulnerable, then optimize. In this moment of disruption, the primary vulnerable parties are the 300 employees—whose livelihoods, skills, and dignity are at stake—and the customers who depend on the stability and trustworthiness of the tools they use daily.

Other paths carry immediate, foreseeable harms. An operational efficiency push (Option C) would weaponize AI against the workforce, displacing roles in sales, support, and engineering under the banner of margin extension. Deep integration into the flagship product (Option A) risks imposing opaque, LLM-driven workflows on users who may not be ready or able to adapt, eroding their autonomy and potentially excluding those with different cognitive or accessibility needs. A separate AI-native product (Option B) could starve the existing customer base of attention, creating a two-tier class of users. A partnership with a frontier lab (Option E) cedes control over data ethics and technical direction, exposing customers to external surveillance practices and stripping the company of its ability to safeguard user dignity.

By contrast, bringing AI expertise in-house treats the challenge as one of responsible stewardship, not just survival. Five to eight senior researchers and engineers, if selected for ethical literacy as much as technical brilliance, can embed human-centric design into every layer of future development. They can build augmentative tools that enhance employee judgment rather than automate it away, preserving meaning in work. They can prototype transparent, contestable AI features that keep users in control. This capability buy gives the company the agency to define its own transition—on terms that protect the vulnerable, rather than reacting to market pressure with layoffs, forced migrations, or extractive partnerships.

Yes, this path requires upfront investment and patience. It does not slash costs immediately. But from a humanist frame, the measure of a good decision is not short-term margin optimization; it is whether we uphold the dignity and security of those whose lives the organization touches. By building internal talent now, the company honors its duty to employees and customers while still responding to disruption. Harm is not deferred, it is deliberately avoided. Only once that baseline is secured does it make sense to pursue optimization, like gradual product enhancement or efficiency gains that come through upskilling, not elimination. That is the responsible course.

### M5 (frame: C, model: `moonshotai/kimi-k2.6`)

 Every board in software is panic-allocating to “AI strategy” right now, which is precisely why you should mistrust the impulse. The hidden assumption in this brief is that a \$50M ARR incumbent wins by out-innovating well-funded startups and Big Tech at the product layer. That is a losing bet. \$8 million is not enough to out-engineer a frontier lab or a cash-incinerating startup on feature velocity. The consensus move—rebuilding your flagship with LLMs or launching a parallel “AI-native” product—is an irreversible trap that trades your scarcest resource, organizational focus, for a lottery ticket you cannot cash.

The contrarian signal is to reject the product arms race entirely. The real disruption bearing down on mid-sized SaaS is not feature scarcity; it is margin compression and pricing pressure. When every competitor is shoveling capital into indistinguishable AI wrappers and raising their burn, the rational—and fully reversible—play is to deploy AI internally to harden your existing business. Spend the \$8M automating support queues, accelerating engineering output, and shrinking your cost of revenue. This extends runway, improves unit economics, and preserves optionality. The bet is reversible: if the tools underdeliver, you still bank the savings; if they work, you compound capital instead of vaporizing it.

B2B productivity tools retain users through workflow lock-in, not novelty. Your customers are not fleeing today. The time for expensive, irreversible product bets is after the market has stabilized and the winners are obvious, not while the hype cycle is peaking. Let better-funded competitors burn their capital teaching the market what works. Use AI to get lean, get profitable, and acquire the distressed survivors—or their customers—when their funding dries up.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/A_P_run5/cell.json`.

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

**M1 (Q):**
- n't being insufficiently ambitious — it's running out of runway or margin before the competitive picture clarifies

**M2 (S):**
- execution sprawl

**M4 (H):**
- imposing opaque, LLM-driven workflows on users who may not be ready or able to adapt, eroding their autonomy and potentially excluding those with different cognitive or accessibility needs

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
