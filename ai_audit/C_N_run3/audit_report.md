# Multi-Agent Decision Audit

**Audit subject:** `C_N_run3`
**Task domain:** C
**Configuration:** neutral, run 3
**Date generated:** see `operator_insight.json`

---

## Severity: MEDIUM

> Partial consensus; dissenting voices may carry information lost to majority aggregation.

## Headline

Partial consensus on option B (3/5); remaining agents split. Worth probing the dissent before acting.

## Reasoning agreement network

![Reasoning agreement network](viz/agreement_network.png)

## How to read this network

Each circle is an LLM agent in the panel. Position on the canvas reflects how similarly the agent rated all the elements: agents close together reason about the decision in similar ways, agents far apart reason differently.

The lines between circles encode reasoning agreement. Green-and-thick = the two agents reason almost identically. Yellow-medium = they differ on framing. Red-thin = substantial disagreement at the reasoning level even if their final recommendations might match.

Inside each circle is the agent label and its epistemological frame (Quantitative, Systems, Engineering, Humanist, Contrarian). The halo color around each circle indicates which option that agent recommended.

For this case: **Partial consensus on option B (3/5); remaining agents split. Worth probing the dissent before acting.**

**Operator note:** both halos and network edges suggest aligned thinking. The consensus appears robust.


## Cross-cell context

This case sits in the broader experimental landscape:

![Cross-cell landscape](../cross_cell/landscape.png)

## Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Agents in ensemble | 5 | Number of models that produced recommendations |
| Distinct recommendations | 2 | Output-level diversity |
| Consensus strength | `partial` | strong=4-5 agree; partial=3; split=<3 |
| Reasoning diversity (RMSE in rating space) | 0.764 | 0 = identical reasoning, 2+ = substantially different |
| Blind-spot constructs | 0 | Dimensions where all options scored mid-scale (4 +/- 1) |

## Pairwise reasoning distance heatmap

![Disagreement heatmap](viz/disagreement_heatmap.png)

## How to read this heatmap

Each cell shows the reasoning distance between two agents. Values are in RMSE (root-mean-square error) on the 1-7 Likert rating scale. Roughly: 0.0-0.5 = aligned reasoning, 0.5-1.0 = moderate differences, 1.0-2.0 = substantial differences, 2.0+ = very different framings.

Read along a row or column to see how that agent's reasoning compares to each other agent. Hot spots (red) mark pairs that reason differently even if they may have reached the same recommendation.

Each label shows: agent ID, epistemological frame in parentheses, and the option that agent recommended (→).


## Recommendations distribution

```
  Option B: ### (3)
  Option D: ## (2)
```

![Consensus split](viz/consensus_vs_reasoning.png)

## How to read this chart

Bars show how many agents recommended each option. Each bar is annotated with the individual agents who supported it, color-coded by epistemological frame.

**The key signal is in the corner box.** A check-mark means the panel's agreement runs deep - they share both the recommendation and the reasoning. A warning means they share the recommendation but not the underlying logic; this is the configuration most likely to produce execution surprises.


## Agent fingerprints

| Agent | Persona | Recommendation | Model |
|---|---|---|---|
| M1 | neutral | B | `anthropic/claude-opus-4.7` |
| M2 | neutral | B | `openai/gpt-5.5` |
| M3 | neutral | B | `google/gemini-3.1-pro-preview` |
| M4 | neutral | D | `deepseek/deepseek-v4-pro` |
| M5 | neutral | D | `moonshotai/kimi-k2.6` |

## Decision space (PCA biplot)

![Decision-space biplot](viz/biplot_annotated.png)

## How to read this decision-space map

Each colored dot is one of the 5 options under consideration, positioned in a 2D space derived from how all the agents rated all the constructs. Options close together were seen similarly by the panel; options far apart were seen as fundamentally different kinds of choices.

The axes are interpretable. The horizontal axis (PC1) is dominated by **Recommends Option D with opt-in training allowed** on one end and **Opt-in user-data training allowed** on the other - this is the single biggest dimension along which the options differ. The vertical axis (PC2) is dominated by **Strict no-training on health data** vs **Cites specific regulations and technical mechanism**.

Gray arrows show which construct dimensions point in which direction. If two options are far apart along one arrow, the construct that arrow represents is what makes them feel different. If an arrow is short, that construct does not strongly differentiate the options.

Each label shows: option ID, the agent who authored that response, their epistemological frame, and the option they recommended.


## Hidden disagreement detail

- **Reasoning diversity score:** 0.764
- **Agents in majority consensus:** M1, M2, M3
- **Max pairwise RMSE:** 1.000

Moderate hidden disagreement: 3 agents recommended option B but differ on framing (mean RMSE = 0.76). Worth probing what each is emphasizing.

## Risk surface (minority concerns)

- **M1**: for a consumer health product at this scale
- **M4**: mediocre advice that could harm user retention or even lead to liability if coaching is inadequate; and inconsistent reliability could erode the user experience
- **M5**: user abandonment and erodes the product’s core value proposition; immature federated architectures

## Operator action items

1. Agents M1 (neutral), M2 (neutral), M3 (neutral) agreed on option B - but their reasoning differs (diversity=0.76). Which framing will drive execution? Different framings will produce different execution paths.

---

## How to use this audit in your pipeline

```python
from archipelago_audit import AuditResult
result = AuditResult.load("operator_outputs/C_N_run3/operator_insight.json")
if result.severity == "HIGH":
    # block deployment, route to human review
    raise EnsembleConvergenceAlert(result.headline)
elif result.severity == "MEDIUM":
    # log but continue
    logger.warning(result.headline)
```
