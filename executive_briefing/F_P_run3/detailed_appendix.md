# Detailed Appendix: F_P_run3

## A. Full task brief

```
# Task F: Creative product launch strategy

## Context

You are advising the founding team of an early-stage consumer hardware startup. They are launching a novel home device: a tabletop unit that uses generative AI + tactile actuators to teach woodworking by guiding a learner's hands through joinery cuts in real time. Price point $1200. Target market: hobbyist makers (estimated 8M in primary geography), with secondary market in design education.

The team has $4M marketing budget for the first 12 months and one chance to position the brand. The product is genuinely novel (no direct competitor exists). The same product, with the same specs and price, can be launched in five distinct ways - each tells a fundamentally different story and recruits a different first user base.

The team is unanimously confident the product works, but split on positioning. **Choose one as the primary launch identity.** The choice will define the brand voice, channel strategy, packaging, the type of user the company gets first, and the kind of company it becomes over the next 5 years.

## Options

**Option A: "Mastery" framing - the path to true skill**
Position as the serious learner's tool: a way to build genuine craft hands-on, faster than apprenticeship, without the danger or guilt of wasted material. Channels: woodworking magazines, maker shows, craft schools. Aesthetic: oiled walnut, leather, slow-shutter video. Outcomes: deep brand commitment from a passionate niche; strong word-of-mouth in the maker community. Risks: niche TAM (~200K serious hobbyists); slow growth; perceived as elitist; expensive customer education.

**Option B: "Therapy" framing - hands as the cure for screen fatigue**
Position against the screen-saturated life: a way to come back to your body, to make something real, to leave the dopamine treadmill. Channels: wellness podcasts, design press, urban professional newsletters. Aesthetic: warm light, hands shown without faces, ambient acoustic music. Outcomes: huge TAM (anyone with screen fatigue ≈ everyone); cultural relevance; high price tolerance (wellness premium). Risks: mostly aspirational purchases (low usage rate); product capabilities under-emphasized; competitive with meditation apps and Pilates studios.

**Option C: "Accessibility" framing - woodworking for the previously excluded**
Position around removing barriers: people whose disabilities, lack of space, lack of mentors, or fear has kept them away from physical making. Channels: disability community press, library/community center partnerships, accessibility advocates. Aesthetic: diverse hands, captioned everything, varying lighting setups. Outcomes: aligned with social mission; press coverage; grant funding eligible; deep loyalty. Risks: tension with $1200 price; perception of tokenism if mishandled; complex content moderation; smaller commercial market than positioned.

**Option D: "Future-of-work" framing - the new vocational pipeline**
Position as the bridge to a real career in skilled trades during a documented carpenter shortage. Channels: trade school partnerships, career counseling, parents-of-teens publications, B2B sales to vocational programs. Aesthetic: workshop floors, finished pieces sold, paychecks. Outcomes: B2B revenue (institutional sales smooth cashflow); aligned with economic narrative; government contract potential. Risks: long sales cycles; bureaucratic procurement; B2C suffers from B2B brand; competing with established vocational tool brands.

**Option E: "Discovery" framing - the gateway to a creative practice**
Position as the start of something open-ended: not woodworking specifically, but the experience of making physical objects with your hands as gateway to a wider creative practice. Channels: design publications, gift-giving guides, museum stores, mid-century-modern aficionado communities. Aesthetic: morning kitchen tables, half-finished projects in plain view, gifts being unwrapped. Outcomes: broad cultural appeal; gift-purchase friendly; flexibility to expand product line. Risks: brand specificity is weak; competes with every other creative hobby; first users buy but don't engage deeply; high return rate risk.

## What to provide

Choose one as the primary launch identity. Provide 200-400 words of reasoning. Advocate; do not enumerate. Address: why this framing, why not the most plausible alternative, what kind of company you are signing up to become over the next 5 years.

```

## B. Each voice in their own words

### M1 (frame: Q, model: `anthropic/claude-opus-4.7`)

# Recommendation: Option A ("Mastery")

**The data argues for narrow before broad.** With $4M and one positioning shot, the binding constraint isn't TAM — it's signal-to-noise in acquisition and retention. A $1200 tabletop device with a novel interaction model has no benchmark CAC, no proven activation rate, and no LTV curve. Under that uncertainty, the rational move is to launch into the segment where willingness-to-pay is highest, return rates lowest, and word-of-mouth coefficient measurable. Serious hobbyists satisfy all three: they already spend $1200+ on single tools, they self-identify in dense communities (Fine Woodworking has ~150K subs; r/woodworking ~3M; maker shows have known attendance), and they post build logs publicly — which means your retention and outcome data becomes free marketing. A 200K SAM at even 2% penetration is 4,000 units × $1200 = $4.8M revenue, recoverable against budget. That's a falsifiable, plausibly-achievable 12-month target with a 90% CI I'd put at roughly $2M–$8M.

**Why not B ("Therapy"), the most seductive alternative?** Because the wellness frame fails the operationalization test. Its TAM is "everyone with screen fatigue," which in practice means no one in particular — you cannot buy that audience efficiently, and the category is dominated by incumbents (Calm, Peloton, Headspace) with 100× your budget. Worse, wellness-framed hardware has a documented failure mode: high aspirational purchase, low sustained usage, high return rate, catastrophic NPS once the novelty fades (see Peloton's churn curve post-2021, Mirror's writedown). At $1200 with a learning curve, an aspirational buyer is a refund waiting to happen. You'd be optimizing for a vanity metric (units shipped quarter one) that destroys the company in quarter four.

**The company you become:** A premium-craft instrument brand — closer to Festool or Lie-Nielsen than to Peloton. Slower revenue growth (expect 30-50% YoY, not 200%), but defensible margins, low churn, and a moat built on craftsman credibility that later expands *downward* into broader markets. Crucially, you can pivot from Mastery to Discovery in year 3 with credibility intact; the reverse path is closed. Optionality favors starting narrow.

### M2 (frame: S, model: `openai/gpt-5.5`)

Choose **Option A: “Mastery” — the path to true skill.**

This product should launch where its magic is most legible: among people who already believe skill matters. A $1200 tactile AI woodworking device is not primarily a wellness object, a gift object, or a vocational procurement item. It is a machine that earns trust only when users feel it is helping them become more capable with their hands. The strongest launch loop is therefore: serious learner uses it, produces visible progress, shows the work, gains status in a maker community, and recruits the next serious learner. That loop is slower than mass-market aspiration, but it is much less fragile.

The most tempting alternative is the “Therapy” framing because the cultural current is real: screen fatigue, embodied living, analog hobbies. But that positioning creates a dangerous mismatch. It attracts people who want the identity of making more than the discipline of learning. For hardware, that is fatal: low usage becomes buyer’s remorse, buyer’s remorse becomes returns, and returns become a brand narrative that the product is expensive décor. Worse, it underplays the actual technological achievement. You would be selling relief when your defensible asset is guided skill acquisition.

“Mastery” does not mean small forever. It means starting with the users who can validate the device in the harshest environment: people who know what good joinery feels like, who can tell whether the guidance is real, and who will forgive rough edges if the learning curve genuinely bends. That creates the credibility required to later expand into education, wellness, accessibility, and broader creative practice without sounding opportunistic.

Over five years, this commits the company to becoming the trusted platform for embodied learning: serious, beautiful, technically excellent, and culturally rooted in craft. Not a gadget company. Not a lifestyle brand with actuators. A company that helps people acquire physical skill in an age where skill is increasingly mediated, simulated, and outsourced. That is the durable position.

### M3 (frame: E, model: `google/gemini-3.1-pro-preview`)

To determine the correct launch positioning, we must reduce the product to its fundamental mechanism: it is an electro-mechanical actuator loop designed to physically encode specialized motor skills into human muscle memory. It teaches joinery.

The binding constraint for an unproven $1200 hardware device with a $4M runway is not top-of-funnel awareness; it is proof of utility. A hardware startup survives its first year only if early adopters actually use the device, generate verifiable output, and evangelize the capability. 

Therefore, **Option A ("Mastery")** is the only viable path. It directly aligns the product’s mechanical reality with a user base that already values the output and is habituated to spending $1,200 on stationary tools (e.g., table saws, planers). We are selling a machine that accelerates physical competence. The messaging must be precise, literal, and targeted at the 200,000 operators who will actually activate the actuators week over week. 

The most dangerous alternative is Option B ("Therapy"). Marketers love Option B because the TAM is theoretically infinite. This is an abstraction trap. Positioning a haptic AI robotics platform as an antidote to screen fatigue relies on a flawed, aspirational analogy. If you sell a highly specific, $1200 joinery tool to stressed urban professionals seeking "mindfulness," the actual utilization rate will approach zero. They are buying the *idea* of woodworking, not the mechanics of it. They will abandon the device when the physical friction outweighs the novelty, resulting in catastrophic return rates and a dead secondary market. 

By choosing Option A, you are deciding the structural reality of the firm over the next five years. You are not building a cultural lifestyle brand or a wellness app. You are signing up to become a precision tooling enterprise. You will allocate future capital to engineering increasingly capable kinematic systems, expanding from hobbyist joinery into advanced fabrication tech, and capturing the high-margin prosumer market by delivering ruthlessly effective, strictly functional hardware.

### M4 (frame: H, model: `deepseek/deepseek-v4-pro`)

We launch under the Accessibility framing. This is the only path that takes seriously the question “who is affected and how?”—not as an afterthought, but as the engine of the product’s identity. The core stakeholders are not just the current hobbyist community, but the vast landscape of people who have been systematically shut out of physical craft: individuals with disabilities, those in cramped urban spaces without mentors, people whose fears or past failures taught them their hands aren’t “made for this.” A $1,200 price tag is in obvious tension with this mission. That tension is not a flaw; it’s a discipline. It forces the company to build grant partnerships, community subsidies, and sliding-scale access from day one, baking economic justice into the business model rather than treating it as charity. Done sincerely, this framing minimizes the profound dignity harm of a product that quietly reinforces privilege—a harm all other options risk by default.

The most plausible alternative, the Mastery framing, seduces with deep niche commitment. Yet it takes the current distribution of who “deserves” craft education as given, carving a moat around an already-resourced few. It signs the company up to become an elite brand that polishes exclusivity into a virtue, leaving structural barriers entirely untouched. The Wellness framing, by contrast, pivots toward the screen-fatigued masses, but its true vulnerable party is the exhausted knowledge worker who spends $1,200 seeking a cure and winds up with guilt and an unused device—a direct, unjustified harm to someone already depleted. Accessibility refuses that waste and that exclusion simultaneously.

Over five years, this choice molds the company into something rare: a hardware maker whose product is inseparable from a distributional mission. The brand becomes synonymous with lowering barriers. Every software update, every new joint library, every partnership with a community center or disability advocate asks: who still can’t access this, and how do we reach them? The risk of tokenism is real, but the antidote is governance—embedded advisory roles, co-design, transparent reporting—not retreat. The upside is a fiercely loyal community that experiences the device not as a luxury gadget, but as a key to a practice they were told they could never belong to. That is the company I want to build: one that wins by measuring its success not in units alone, but in the widened radius of who gets to make something real with their hands.

### M5 (frame: C, model: `moonshotai/kimi-k2.6`)

 Choose **Option E: Discovery**. The team’s unanimous confidence that the product “works” is the single most dangerous input in this decision. Unanimity in early-stage hardware is not validation; it is a blindness signal. You have not built a woodworking master, a therapy device, or a vocational pipeline. You have built a tactile actuator with a language model attached. You do not yet know what it is for, and selecting a narrow identity now—Mastery, Therapy, Accessibility, or Trade—is an irreversible commitment to a user whose exacting expectations you will almost certainly fail.

The “gateway” framing is the only reversible move. It recruits gift-givers, design-curious dabblers, and museum-store browsers who arrive with low expectations and high forgiveness. If the firmware is rough, the object still sits beautifully on a kitchen table; if the AI interprets a joint too literally, it reads as honest quirk rather than pedagogic betrayal. You are not selling an outcome; you are selling permission to begin something physical and abandon it without guilt. That is a durable market for a v1 product with unproven retention and unseen failure modes.

Reject the obvious alternative, Option B. “Screen fatigue” is the consensus TAM seduction of the decade, and it is a graveyard. The perceived market—everyone with a phone—is an illusion. The moment a wellness buyer compares a $15 meditation app against your $1,200 box that demands sawdust, friction, and cleanup, the dopamine math collapses. High price tolerance means nothing when aspiration meets storage-clutter regret.

By choosing Discovery, you sign up to become a company of creative infrastructure, not educational outcomes. In five years you are either the brand that owns the “beautiful beginning” of physical making, or you are dead. But if you die, you die having learned what users actually built, rather than choking on promises you never should have made.

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of 14 constructs is in `results/F_P_run3/cell.json`.

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
- high aspirational purchase, low sustained usage, high return rate, catastrophic NPS once the novelty fades (see Peloton's churn curve post-2021, Mirror's writedown)

**M4 (H):**
- tokenism is real, but the antidote is governance—embedded advisory roles, co-design, transparent reporting—not retreat

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
