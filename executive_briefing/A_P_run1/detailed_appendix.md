# Detailed Appendix: A_P_run1

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

**Recommendation: Option C (operational efficiency), with a carve-out to pilot Option A.**

The framing "AI disruption" is doing too much work in this brief. Before committing $8M to a strategic bet, I want to know: what is the actual churn rate? What percentage of churn cites AI-competitor switching in exit interviews? What's the current gross margin and runway? Absent that data, I anchor on base rates and option value.

Base rates for the alternatives are unflattering. New product lines at incumbent SaaS firms (Option B) have historically low success rates — I'd estimate 10-20% reach material revenue within 24 months, and $8M is likely under-capitalized for a true AI-native build competing against well-funded startups. Aggressive senior AI hiring (Option D) at a $50M ARR company faces brutal unit economics: 5-8 senior researchers at fully-loaded ~$600-800K each burns the budget in 18 months with no shipped product and high flight risk. Frontier lab partnerships (Option E) sound like leverage but in practice deliver commoditized capability your competitors also access — low differentiation, and you become a distribution channel for the lab.

Option C is the only choice with measurable, near-term, falsifiable ROI. Internal AI tooling in sales (lead scoring, outreach), support (deflection, summarization), and engineering (code assist, test generation) has documented productivity gains in the 15-30% range across multiple published studies and vendor case studies. On a 300-person base with ~$30-40M opex, even a conservative 10% efficiency gain returns $3-4M annually — a 1.5-2 year payback on the full $8M, with 80% confidence interval roughly [1x, 4x] return. Critically, it *extends runway*, which is the actual scarce resource when facing a disruption you can't yet scope.

The carve-out: allocate ~$1.5M of the $8M to embed LLM features in the top 2-3 flagship workflows (Option A, scoped). This is defensive table-stakes and generates customer-facing signal on willingness-to-pay for AI features — data you need before any larger bet.

Confidence in C-primary: ~65%. Key risk: if churn data shows active AI-driven defection >5% quarterly, reweight toward A.

### M2 (frame: S, model: `openai/gpt-5.5`)

Invest primarily in **deep AI integration into the existing flagship product**.

For a $50M ARR SaaS company, the highest-leverage asset is not blank-slate innovation; it is the existing customer base, workflow data, trust, distribution, and embedded position in customers’ operating routines. AI disruption becomes existential when competitors use AI to make the current workflow feel obsolete. The defensive and offensive move is therefore to change the workflow before someone else does.

The company should use the $8M to rebuild the core product experience around AI-enabled outcomes: automation of repetitive work, intelligent recommendations, natural-language interfaces, proactive workflow completion, and cross-product context. The goal should not be “add AI features,” but to compress time-to-value for the customer so significantly that the product’s category definition shifts. If the current product helps users manage work, the AI-integrated version should help users complete work.

This option also creates the strongest reinforcing loop. Existing users generate feedback, feedback improves product quality, improved quality increases retention and expansion, expansion funds further AI development, and deeper usage strengthens the company’s data and workflow advantage. That loop is much harder for startups to replicate and much less dependent on external platform partners than a partnership-led strategy.

A separate AI-native product may look bolder, but it risks splitting attention, starving the core, and creating internal competition for scarce technical and go-to-market bandwidth. In a disruption cycle, fragmentation is dangerous. The company needs strategic coherence: one product narrative, one customer migration path, one roadmap that tells the market, “we are transforming the category we already understand.”

The investment should include selective AI hiring and internal tooling, but only as support mechanisms for the flagship transformation. The board should measure success through adoption of AI-powered workflows, retention among exposed accounts, expansion revenue, support deflection, and customer-reported productivity gains.

The central risk is not failing to experiment. It is allowing the core product to become a legacy surface while the market’s expectations reset around AI-native workflows. The company should use its incumbent advantages while they still compound.

### M3 (frame: E, model: `google/gemini-3.1-pro-preview`)

To survive AI disruption, we must reduce the problem to its fundamentals. A $50M ARR B2B productivity SaaS is simply a mechanical system that converts user time into business output. Disruption occurs when a competing system performs this conversion with less friction. Therefore, the binding constraint for this company is the imminent decay of the flagship product’s utility function. If the core product becomes too slow relative to AI-native alternatives, the $50M ARR evaporates via churn. Margins and new verticals do not matter if the core engine dies. 

The only rational allocation of the $8M is deep AI integration into your existing flagship product (Option A). 

What is the actual mechanism of defense here? Your primary assets are existing distribution, trapped data, and deeply mapped user context. Startups have access to intelligence but lack this distribution and context; Big Tech has distribution but lacks specialized B2B workflow capture. By embedding LLM capabilities directly into the core workflows you already own, you immediately collapse the friction for your users. You neutralize the startup threat by upgrading the tool your customers are already paying for, extracting immediate leverage from your existing database and UI.

Do not waste capital hiring ML researchers or building parallel products. Building a new product from scratch abandons your only structural advantage. Hiring researchers fundamentally misunderstands the current technical reality: foundational intelligence is now a commoditized API input, not a proprietary layer you need to build in-house. The required engineering task is applied product integration—plumbing external intelligence APIs into your existing state machines—not fundamental research. 

Address the binding constraint directly: your users' current workflows are becoming obsolete. Over the next 12 months, spend the $8M on pure applied engineering to rebuild those exact workflows with embedded AI. Secure the core retention mechanism, use commoditized models as simple inputs, and ignore the rest.

### M4 (frame: H, model: `deepseek/deepseek-v4-pro`)

As a humanist-ethicist analyst, my primary question is always: **who is affected and how?** Centering stakeholders, dignity, and distributional consequences, I must look beyond the boardroom's financial calculus and examine the human impact of each path.

My decision heuristic demands I first minimize **unjustified harm to vulnerable parties**—and in this context, that points directly to the company's 300 employees. They are the most proximate vulnerable group, their livelihoods and professional meaning tethered to the decisions made in the next 12 months. Options A, B, and D all carry a high risk of inflicting this harm through displacement or hollowing-out.

Option A (deep integration) is a siren song. It frames the work as a technical rebuild, but it implicitly renders swaths of existing design, product, and engineering knowledge obsolete. It tells dedicated employees that their craft, which built a $50M company, is now legacy debt to be automated away. It’s a betrayal of their contribution and a psychological blow to dignity. Option B (new product line) is a dangerous distraction that creates a two-tiered workforce, starving the core product of talent and eventually leading to its decline and the unemployment of those who maintain it. Option D (aggressive hiring) would import a new aristocracy of AI/ML engineers, embedding a message that current staff are second-class and will inevitably be replaced when the new hires build their replacements.

The path that minimizes unjustified harm is **Option C: the operational efficiency push**. This is not merely a choice for margin; it is a commitment to **augmentation over automation**. By deploying AI tools internally to support—not supplant—sales, support, and engineering staff, the company invests in making its people more effective and their work less toilsome. This respects the dignity of existing employees, honoring their institutional knowledge while equipping them for a changing landscape. It extends the runway, creating a shelter from the storm of disruption. This breathing room is a moral imperative; it provides a window to design a just transition—a future where the business evolves with its people, retraining and redirecting them, rather than simply discarding them.

The distributional consequences are optimal: employees retain agency, gain new skills, and see their daily frustrations with drudge work alleviated. The company becomes more resilient without the moral injury of mass displacement. The board should invest in its humans first, using AI to strengthen the enterprise from the inside out, honoring the social contract with the people who are the company. Only from this fortified, ethically sound base can a humane, long-term response to disruption be planned.

### M5 (frame: C, model: `moonshotai/kimi-k2.6`)

 The entire board is operating under a hidden assumption: that customers are begging for AI-infused workflows and that a \$50M ARR company can out-feature both Fortune 500 labs and venture-backed startups spending ten times its budget. What if everyone is wrong? What if the current AI moment is less a product revolution and more a margin event—at least for incumbents who survive the hysteria?

The unanimous consensus screams for splashy product bets—rebuild the flagship, launch a native AI sibling, or hire a phalanx of ML researchers who will burn cash for eighteen months before shipping anything. These are concentrated, irreversible wagers. Once you bolt LLMs into core workflows, you inherit hallucination risk, ballooning inference COGS, and customer confusion that you cannot undo in twelve months. A parallel product line fragments an already finite focus. And hiring five to eight senior AI engineers in this market consumes the bulk of the \$8M in compensation alone, leaving zero margin for error.

Option C is the only move that respects the arithmetic. Deploy AI internally across sales, support, and engineering not as surrender, but as asymmetric defense. You extend runway, capture genuine productivity data on where AI actually works versus where it merely demos well, and preserve capital for a future product bet when the competitive fog clears. It is fully reversible: turn off an internal copilot, and nothing customer-facing breaks.

Furthermore, letting Big Tech and startups fight the feature wars while you systematically lower your breakeven is the ultimate contrarian signal. When their burn rates force retrenchment next year, you will have a leaner, more profitable core and the liquidity to acquire their stranded customers or pick winning tech off the shelf for pennies on the dollar. In AI’s gold rush, sell the shovels—to yourself—and keep the \$8M out of the bonfire.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 11 constructs is in `results/A_P_run1/cell.json`.

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
- splitting attention, starving the core, and creating internal competition for scarce technical and go-to-market bandwidth
- not failing to experiment

**M4 (H):**
- inflicting this harm through displacement or hollowing-out

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
