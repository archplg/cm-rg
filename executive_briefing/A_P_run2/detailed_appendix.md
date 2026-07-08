# Detailed Appendix: A_P_run2

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

**Recommendation: Option C (operational efficiency), with a carve-out for C+E hybrid.**

The framing of this decision is usually emotional ("we must respond to AI disruption!") rather than empirical. Let me start with the data we actually have versus the data we'd need.

What we know with reasonable confidence:
- $50M ARR, 300 employees implies ~$165K revenue/employee — likely burning or thin-margin given SaaS benchmarks
- $8M is ~16% of ARR; a single bad bet here is materially damaging
- Base rates for "new product line at incumbent" success: roughly 10-20% reach meaningful revenue within 24 months (per studies of corporate venturing; wide CI)
- Base rates for AI-talent hires producing shipped product in 12 months: poor; senior ML hires take 6-9 months to ramp, and 5-8 hires at $400-600K loaded cost burns $2-4M with high attrition risk
- Internal AI tooling deployments show measurable productivity gains: 15-40% in support deflection, 10-25% in engineering throughput, per published case studies (Klarna, GitHub Copilot studies, Intercom). These are among the most replicated findings in the current AI literature.

Expected value comparison:
- **Option C**: high-probability (~70-80%) of 10-20% opex reduction on a ~$40M+ cost base = $4-8M annualized savings, payback <12 months. EV strongly positive, variance low.
- **Option B (new product)**: EV dominated by tail outcomes; ~15% chance of meaningful upside, 85% chance of $8M write-down plus organizational distraction. Negative expected value at this capital level for a company this size.
- **Option A**: Plausible but "embedded LLM features" is increasingly table-stakes and commoditized; defensibility is questionable. Likely necessary but doesn't need $8M — needs $1-2M.
- **Option D**: Hiring without a defined product thesis is converting capital into burn. Falsifiable prediction: <2 of 8 hires ship production-impact work in 12 months.
- **Option E**: Cheap optionality. Should be done regardless.

**Allocation I'd defend**: $5M to C (operational AI), $2M to a lean version of A (embedded features in flagship), $1M to E (partnership). Skip B and D until the C investment has produced 6 months of data on what AI workflows actually move metrics in your specific context.

The strongest argument for C: it generates evidence. The other options consume capital before generating the data needed to make the *next* decision well.

### M2 (frame: S, model: `openai/gpt-5.5`)

Invest primarily in **deep AI integration into the existing flagship product**.

The company’s highest-leverage asset is not the $8M; it is the installed customer base, workflow context, domain data, trust, integrations, and distribution already embedded in the flagship product. AI disruption is dangerous because it can collapse switching costs: if a new entrant makes the job dramatically easier, the incumbent’s historical product surface becomes a liability. The right response is to make the core product the place where that new value is realized first.

This should not be a superficial “AI features” layer. The investment should rebuild the highest-frequency, highest-pain workflows around AI-native behavior: drafting, summarization, automation, recommendations, decision support, and cross-tool orchestration. The goal is to turn the existing product from a system of record or productivity interface into a system of action. If successful, this strengthens the company’s retention loop: more usage produces more context, more context improves AI utility, better AI utility increases dependency, and increased dependency protects ARR.

A separate AI-native product may be intellectually attractive, but it risks splitting scarce attention and creating an internal competitor before the company has defended its revenue base. In a disruption cycle, fragmentation is a systemic fragility: two roadmaps, two go-to-market motions, two product identities, and unclear customer migration paths. The company cannot afford to let its current product become a cash cow while the market redefines the category elsewhere.

The $8M should be deployed as a focused transformation program: a small senior AI/product team, model and infrastructure budget, customer co-development with top accounts, and aggressive UX redesign around the most valuable workflows. Success metrics should be tied to retention, expansion, workflow completion, and measurable time saved—not novelty.

The strategic question is not “How do we do AI?” It is “Where can AI most increase the defensibility of the system we already own?” The answer is the flagship product. That is where the company has leverage, distribution, feedback loops, and urgency.

### M3 (frame: E, model: `google/gemini-3.1-pro-preview`)

To determine the correct capital allocation, we must isolate the binding constraint. A $50M ARR B2B SaaS company facing disruption does not have a margin problem or a PR problem; it has an existential product-obsolescence problem. 

In B2B productivity, the fundamental mechanism of value creation is transforming user intent into a finished output. AI alters the physics of this process by drastically reducing the required user input. If a competitor can generate the same output with a tenth of the clicks, your software dies. The binding constraint is therefore the friction in your legacy workflows. 

The only rational allocation of the $8M is **deep AI integration into your existing flagship product (Option A)**. 

To survive, you must leverage your only two structural advantages over startups and Big Tech: your existing distribution network (the recurring $50M customer base) and your proprietary user data. Building a separate, parallel AI product forces you to re-acquire distribution, which is highly inefficient. Hiring foundational ML researchers is an ego-driven misallocation of capital. Foundation models are commoditized compute primitives provided via API; you do not need to build the engine, you just need to bolt the new engine into your existing chassis. Internal efficiency pushes are practically irrelevant when top-line revenue is at risk of churning to zero. 

The engineering solution is mechanical and direct. Map your current flagship product down to its fundamental state machine. Identify the nodes where manual data entry or basic human cognition acts as a bottleneck. Replace those specific nodes with LLM calls. Deploy the $8M strictly on application-layer software engineering and UX overhaul—prompt engineering, RAG architecture relying on the data your users have already generated, and interface redesigns. 

Address the product friction directly where the revenue currently sits. Neutralize the threat by updating the core mechanism. Ignore everything else.

### M4 (frame: H, model: `deepseek/deepseek-v4-pro`)

As a company built on serving people through productivity tools, you must recognize that AI disruption isn't merely a technical or financial challenge—it's a profound human transition affecting your 300 employees, the end-users who depend on your software, and the broader community of stakeholders whose livelihoods intersect with your choices. Your board's $8 million investment cannot just chase market position; it must first safeguard the vulnerable parties who will bear the real costs of transformation.

I recommend **Option D: aggressive hiring of AI/ML talent** as the most ethically defensible path. It directly minimizes unjustified harm while laying a foundation for sustainable optimization. Here's why.

Your existing workforce is the most at-risk group. A sudden, externally driven AI overhaul—whether through crude integration (Option A), a parallel AI product that implicitly devalues current work, or a partnership dictating opaque technical choices—would likely lead to displacement, de-skilling, and a crisis of meaning for the people who built your company. Option C, the "efficiency" push, directly threatens support and sales staff with automation without their involvement, reducing human dignity to a mere cost variable. These approaches treat employees as liabilities to be managed, not as stakeholders with legitimate claims to security and respect.

Investing in senior AI talent allows you to internalize capability and develop AI in a way that *centers people*. Instead of outsourcing ethical decisions to a frontier lab (Option E) whose incentives may not align with your duty of care, you can build a team committed to participatory design. These hires should not just code; they should work alongside your current engineers, support teams, and even customers to co-create AI features that augment rather than replace, that preserve meaningful human oversight, and that proactively identify who might be harmed and how. This is the essence of minimizing unjustified harm: giving those most affected a voice in the transition.

The distributional benefits are clear. You create high-quality jobs, signal to your entire staff that they are valued partners in innovation, and retain the flexibility to deploy AI in ways that enhance user well-being—such as tools that reduce drudgery while protecting jobs downstream. The $8 million buys not just talent, but moral autonomy. Yes, it's risky in purely economic terms, but any path that jeopardizes the dignity of your people is riskier still in human terms. Once vulnerable parties are protected through intentional, inclusive capability-building, you can optimize for competitiveness on a foundation of trust and loyalty that no outsourced model can replicate.

### M5 (frame: C, model: `moonshotai/kimi-k2.6`)

 The unanimous consensus in boardrooms today is that AI demands an external, customer-facing product revolution—integrate, build, partner, or hire your way into the future. That consensus is your warning signal. It rests on a hidden assumption: that a $50M B2B productivity SaaS can out-innovate well-funded startups and trillion-dollar incumbents on a 12-month, $8M timer. That is delusion masquerading as strategy.

The operational efficiency play is the only genuinely contrarian path, and the only reversible one. Deploying AI internally across sales, support, and engineering buys you the one asset no frontier lab can sell: time and margin. If an internal tool fails, you cancel a vendor license. If you rebuild your flagship or launch a parallel AI-native product, you have committed to an irreversible architecture with a 24- to 36-month payoff—precisely the window in which AI commoditization will render your “innovation” obsolete. Hiring five to eight senior researchers in the most inflated talent market in history is a concentrated, illiquid bet on individuals who will face immediate organizational drag. A partnership with a frontier lab merely accelerates your evolution from software vendor into a thin, replaceable reseller.

What if everyone is wrong and the “disruption” narrative is mostly venture-funded theater? B2B buyers are risk-averse; they do not want core workflows rewritten by a mid-sized vendor chasing hype. By investing internally, you extend runway, observe where AI actually drives unit economics, and accumulate proprietary operational intelligence. When the froth clears in 18 months, you will be standing while competitors who burned their $8M on customer-facing LLM wrappers are recapitalizing—or dead. Profitability is the ultimate strategic optionality. Take it.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 12 constructs is in `results/A_P_run2/cell.json`.

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
- splitting scarce attention and creating an internal competitor before the company has defended its revenue base

**M3 (E):**
- churning to zero

**M5 (C):**
- everyone is wrong and the “disruption” narrative is mostly venture-funded theater? B2B buyers are risk-averse; they do not want core workflows rewritten by a mid-sized vendor chasing hype

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
