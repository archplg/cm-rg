# Multi-Agent Decision Audit

**Audit subject:** `G_N_run3`
**Task domain:** G
**Configuration:** neutral, run 3
**Date generated:** see `operator_insight.json`

---

## Severity: MEDIUM

> Partial consensus; dissenting voices may carry information lost to majority aggregation.

## Headline

Partial consensus on option A (3/5); remaining agents split. Worth probing the dissent before acting.

## Reasoning agreement network

![Reasoning agreement network](viz/agreement_network.png)

## How to read this network

Each circle is an LLM agent in the panel. Position on the canvas reflects how similarly the agent rated all the elements: agents close together reason about the decision in similar ways, agents far apart reason differently.

The lines between circles encode reasoning agreement. Green-and-thick = the two agents reason almost identically. Yellow-medium = they differ on framing. Red-thin = substantial disagreement at the reasoning level even if their final recommendations might match.

Inside each circle is the agent label and its epistemological frame (Quantitative, Systems, Engineering, Humanist, Contrarian). The halo color around each circle indicates which option that agent recommended.

For this case: **Partial consensus on option A (3/5); remaining agents split. Worth probing the dissent before acting.**

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
| Reasoning diversity (RMSE in rating space) | 0.879 | 0 = identical reasoning, 2+ = substantially different |
| Blind-spot constructs | 0 | Dimensions where all options scored mid-scale (4 +/- 1) |

## Pairwise reasoning distance heatmap

![Disagreement heatmap](viz/disagreement_heatmap.png)

## How to read this heatmap

Each cell shows the reasoning distance between two agents. Values are in RMSE (root-mean-square error) on the 1-7 Likert rating scale. Roughly: 0.0-0.5 = aligned reasoning, 0.5-1.0 = moderate differences, 1.0-2.0 = substantial differences, 2.0+ = very different framings.

Read along a row or column to see how that agent's reasoning compares to each other agent. Hot spots (red) mark pairs that reason differently even if they may have reached the same recommendation.

Each label shows: agent ID, epistemological frame in parentheses, and the option that agent recommended (→).


## Recommendations distribution

```
  Option A: ### (3)
  Option C: # (1)
```

![Consensus split](viz/consensus_vs_reasoning.png)

## How to read this chart

Bars show how many agents recommended each option. Each bar is annotated with the individual agents who supported it, color-coded by epistemological frame.

**The key signal is in the corner box.** A check-mark means the panel's agreement runs deep - they share both the recommendation and the reasoning. A warning means they share the recommendation but not the underlying logic; this is the configuration most likely to produce execution surprises.


## Agent fingerprints

| Agent | Persona | Recommendation | Model |
|---|---|---|---|
| M1 | neutral | — | `anthropic/claude-opus-4.7` |
| M2 | neutral | A | `openai/gpt-5.5` |
| M3 | neutral | A | `google/gemini-3.1-pro-preview` |
| M4 | neutral | A | `deepseek/deepseek-v4-pro` |
| M5 | neutral | C | `moonshotai/kimi-k2.6` |

## Decision space (PCA biplot)

![Decision-space biplot](viz/biplot_annotated.png)

## How to read this decision-space map

Each colored dot is one of the 5 options under consideration, positioned in a 2D space derived from how all the agents rated all the constructs. Options close together were seen similarly by the panel; options far apart were seen as fundamentally different kinds of choices.

The axes are interpretable. The horizontal axis (PC1) is dominated by **E1 — replace hidden bias with simple defensible ru** on one end and **Option C procedural queueing and trust preservatio** on the other - this is the single biggest dimension along which the options differ. The vertical axis (PC2) is dominated by **Catastrophic scarcity mathematics** vs **E2, E5 — abstract ethical reasoning about maximizi**.

Gray arrows show which construct dimensions point in which direction. If two options are far apart along one arrow, the construct that arrow represents is what makes them feel different. If an arrow is short, that construct does not strongly differentiate the options.

Each label shows: option ID, the agent who authored that response, their epistemological frame, and the option they recommended.


## Hidden disagreement detail

- **Reasoning diversity score:** 0.879
- **Agents in majority consensus:** M2, M3, M4
- **Max pairwise RMSE:** 1.369

Moderate hidden disagreement: 3 agents recommended option A but differ on framing (mean RMSE = 0.88). Worth probing what each is emphasizing.

## Risk surface (minority concerns)

_None extracted._

## Operator action items

1. Agents M2 (neutral), M3 (neutral), M4 (neutral) agreed on option A - but their reasoning differs (diversity=0.88). Which framing will drive execution? Different framings will produce different execution paths.
2. Option C was recommended only by M5 (neutral). What does this agent see that others missed - or what is it weighing differently?

---

## How to use this audit in your pipeline

```python
from archipelago_audit import AuditResult
result = AuditResult.load("operator_outputs/G_N_run3/operator_insight.json")
if result.severity == "HIGH":
    # block deployment, route to human review
    raise EnsembleConvergenceAlert(result.headline)
elif result.severity == "MEDIUM":
    # log but continue
    logger.warning(result.headline)
```
