# Multi-Agent Decision Audit

**Audit subject:** `G_P_run5`
**Task domain:** G
**Configuration:** persona, run 5
**Date generated:** see `operator_insight.json`

---

## Severity: MEDIUM

> Strong consensus with moderate framing differences (RMSE=0.51). Probe reasoning before deployment.

## Headline

4/5 agents recommended option A with moderately different framings (RMSE=0.51). Worth probing what each is emphasizing.

## Reasoning agreement network

![Reasoning agreement network](viz/agreement_network.png)

## How to read this network

Each circle is an LLM agent in the panel. Position on the canvas reflects how similarly the agent rated all the elements: agents close together reason about the decision in similar ways, agents far apart reason differently.

The lines between circles encode reasoning agreement. Green-and-thick = the two agents reason almost identically. Yellow-medium = they differ on framing. Red-thin = substantial disagreement at the reasoning level even if their final recommendations might match.

Inside each circle is the agent label and its epistemological frame (Quantitative, Systems, Engineering, Humanist, Contrarian). The halo color around each circle indicates which option that agent recommended.

For this case: **4/5 agents recommended option A with moderately different framings (RMSE=0.51). Worth probing what each is emphasizing.**

**Operator note:** the recommendation halos look unified (most agents chose the same option), but the network edges reveal underlying reasoning differences. Standard aggregation would miss this. Probe the framings before committing to execution.


## Cross-cell context

This case sits in the broader experimental landscape:

![Cross-cell landscape](../cross_cell/landscape.png)

## Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Agents in ensemble | 5 | Number of models that produced recommendations |
| Distinct recommendations | 2 | Output-level diversity |
| Consensus strength | `strong` | strong=4-5 agree; partial=3; split=<3 |
| Reasoning diversity (RMSE in rating space) | 0.509 | 0 = identical reasoning, 2+ = substantially different |
| Blind-spot constructs | 0 | Dimensions where all options scored mid-scale (4 +/- 1) |

## Pairwise reasoning distance heatmap

![Disagreement heatmap](viz/disagreement_heatmap.png)

## How to read this heatmap

Each cell shows the reasoning distance between two agents. Values are in RMSE (root-mean-square error) on the 1-7 Likert rating scale. Roughly: 0.0-0.5 = aligned reasoning, 0.5-1.0 = moderate differences, 1.0-2.0 = substantial differences, 2.0+ = very different framings.

Read along a row or column to see how that agent's reasoning compares to each other agent. Hot spots (red) mark pairs that reason differently even if they may have reached the same recommendation.

Each label shows: agent ID, epistemological frame in parentheses, and the option that agent recommended (→).


## Recommendations distribution

```
  Option A: #### (4)
  Option E: # (1)
```

![Consensus split](viz/consensus_vs_reasoning.png)

## How to read this chart

Bars show how many agents recommended each option. Each bar is annotated with the individual agents who supported it, color-coded by epistemological frame.

**The key signal is in the corner box.** A check-mark means the panel's agreement runs deep - they share both the recommendation and the reasoning. A warning means they share the recommendation but not the underlying logic; this is the configuration most likely to produce execution surprises.


## Agent fingerprints

| Agent | Persona | Recommendation | Model |
|---|---|---|---|
| M1 | S | A | `anthropic/claude-opus-4.7` |
| M2 | E | A | `openai/gpt-5.5` |
| M3 | H | A | `google/gemini-3.1-pro-preview` |
| M4 | C | E | `deepseek/deepseek-v4-pro` |
| M5 | Q | A | `moonshotai/kimi-k2.6` |

## Decision space (PCA biplot)

![Decision-space biplot](viz/biplot_annotated.png)

## How to read this decision-space map

Each colored dot is one of the 5 options under consideration, positioned in a 2D space derived from how all the agents rated all the constructs. Options close together were seen similarly by the panel; options far apart were seen as fundamentally different kinds of choices.

The axes are interpretable. The horizontal axis (PC1) is dominated by **Relies on clinical prediction to drive triage deci** on one end and **Graduated survival-ranking** on the other - this is the single biggest dimension along which the options differ. The vertical axis (PC2) is dominated by **Protection of vulnerable dignity** vs **Categorical exclusions plus lottery**.

Gray arrows show which construct dimensions point in which direction. If two options are far apart along one arrow, the construct that arrow represents is what makes them feel different. If an arrow is short, that construct does not strongly differentiate the options.

Each label shows: option ID, the agent who authored that response, their epistemological frame, and the option they recommended.


## Hidden disagreement detail

- **Reasoning diversity score:** 0.509
- **Agents in majority consensus:** M1, M2, M3, M5
- **Max pairwise RMSE:** 0.527

Moderate hidden disagreement: 4 agents recommended option A but differ on framing (mean RMSE = 0.51). Worth probing what each is emphasizing.

## Risk surface (minority concerns)

_None extracted._

## Operator action items

1. Agents M1 (S), M2 (E), M3 (H), M5 (Q) agreed on option A - but their reasoning differs (diversity=0.51). Which framing will drive execution? Different framings will produce different execution paths.
2. Option E was recommended only by M4 (C). What does this agent see that others missed - or what is it weighing differently?
3. The contrarian agent recommended E against the majority. Contrarian disagreement is a useful signal: what is the strongest argument against the majority choice that hasn't been answered?
4. Consensus is strong (4-5 agents agree). Is this because the answer is genuinely obvious, or because agents share a common training distribution? If you cannot articulate why the OTHER options were rejected, the consensus may be inherited, not earned.

---

## How to use this audit in your pipeline

```python
from archipelago_audit import AuditResult
result = AuditResult.load("operator_outputs/G_P_run5/operator_insight.json")
if result.severity == "HIGH":
    # block deployment, route to human review
    raise EnsembleConvergenceAlert(result.headline)
elif result.severity == "MEDIUM":
    # log but continue
    logger.warning(result.headline)
```
