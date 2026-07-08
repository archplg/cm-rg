# archipelago_audit

A behavioral interpretability layer for multi-agent LLM systems.

## What it does

When you run an ensemble of LLM agents on a decision, this library lets you ask:

- Did they really agree, or are they pretending to?
- What dimensions of the problem did they collectively underweight?
- What risks did minority agents raise that majority-voting drowned out?
- Should an operator block this decision and route to human review?

## What it does NOT do

- It does not run your agents for you. Use OpenRouter, LangChain, CrewAI, your stack.
- It does not improve agent accuracy. It improves your visibility into how agents reasoned.
- It is not a substitute for human judgment on consequential decisions.

## Status

Alpha. Built from a research experiment on 5 frontier models across 3 task types.

## Citation

If you use this in research, please cite the accompanying paper (in preparation).
