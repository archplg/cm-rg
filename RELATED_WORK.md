# Related Work — annotated bibliography for Archipelago cross-model paper

A growing reference index. Each entry includes citation, summary, and **specific cross-references to our experiment design and findings**.

---

## Sun, Dillion, Gray, Lyu, Zhang, Li (2026) — Expectation cues bias LLM judgment

**Citation:**
```
@inproceedings{sun2026expectation,
  title={From Expectation to Evaluation: Expectation Cues Systematically Bias LLM and Human Judgment},
  author={Sun, Yiteng and Dillion, Danica and Gray, Kurt and Lyu, Mengtao and Zhang, Zhuorui and Li, Fan},
  booktitle={Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems},
  year={2026},
  publisher={ACM},
  doi={10.1145/3772318.3790492},
  address={Barcelona, Spain}
}
```

**One-sentence summary:** Both humans and LLMs (GPT-4o, Llama-3.3-70B, DeepSeek-r1) exhibit assimilation effects — when a suggestion is primed with "this is from a world-class expert" vs "this is from a basic assistant", evaluation scores shift in the direction of expectation; effect magnitude is largest under moderate (not extreme) expectation-quality mismatches.

**Experimental design:**
- 3×3 factorial (expectation: high/moderate/low × quality: high/moderate/low)
- Experiment 1 (N=720 per modality): expectation BEFORE evaluation
- Experiment 2 (N=540 per modality): expectation BETWEEN initial and revised evaluation
- 12 topics (social issues + personal challenges)
- Expectation manipulation grounded in Stereotype Content Model (SCM) - competence-dimension priming
- Two researchers manually curated quality variation to ensure controlled differences

**Key quantitative findings:**
- LLMs and humans both show **assimilation** (shift toward primed expectation)
- Strongest distortion at **moderate expectation-quality discrepancies** (asymmetric "violation curve")
- Humans adjust **unconsciously**; LLMs adjust in **consistent and traceable manner** (key methodological asymmetry)
- Chain-of-thought reasoning does not reduce the bias
- LLMs are **less anchored on initial judgment** than humans — more willing to revise

**Relevance to our experiment (5 specific cross-references):**

### CR-1: Justifies our Phase 2 anonymization design
Their finding that quality-attribution cues (e.g., "from an expert") systematically bias LLM evaluation supports our deliberate choice to **strip author identity** before raters see responses. In our Phase 2, free responses from 5 models are shuffled and labeled E1-E5; raters in Phase 4 know nothing about which model produced which response. This isolates the construct elicitation from quality-attribution anchoring.

> **Paper draft language**: "To prevent quality-attribution bias of the kind documented by Sun et al. (2026), our Phase 2 anonymization strips author identity from each response before raters evaluate them. Each response is presented under anonymous labels E1-E5 with content-only summaries."

### CR-2: Distinguishes our persona prompts from their authority claims
Their expectation cues are **explicit quality claims** ("world-class advisor"). Our personas (Q/S/E/H/C) are **epistemological framings without quality attribution** ("You are a Quantitative analyst" — not "You are a TOP analyst"). Our null persona effect (paired t-test p=0.855) **distinguishes** framing-only manipulation from quality-attribution manipulation.

> **Paper draft language**: "Unlike Sun et al. (2026), whose manipulations included explicit competence claims ('world-class', 'basic'), our persona prompts assign epistemological frames without quality attribution. Our null average persona effect suggests that framing-only manipulation is mechanistically distinct from authority-based priming, and that conditional-on-task effects (Sec X.Y) reveal a more nuanced pattern."

### CR-3: Strengthens our argument that Repertory Grid is robust on LLMs
Their finding that LLMs are **less anchored than humans** on initial judgment supports our use of Repertory Grid (Kelly 1955) — a method originally designed for human raters and historically suffering from human-rater self-anchoring — when transposed to LLM raters.

> **Paper draft language**: "Our application of Repertory Grid to LLM agents leverages a methodological advantage documented by Sun et al. (2026): LLMs exhibit lower anchoring than humans, making them less susceptible to the within-rater consistency biases that have challenged human Repertory Grid studies."

### CR-4: CoT doesn't help — relevant to our Phase 3 design
Their finding that Chain-of-Thought does NOT reduce expectation bias is relevant to our Phase 3 (triadic construct elicitation), which is essentially structured CoT. We do NOT rely on CoT for de-anchoring — we rely on **anonymization** (Phase 2). This means our design choice is **methodologically correct** in light of their finding.

> **Paper draft language**: "Because Sun et al. (2026) demonstrate that Chain-of-Thought prompting does not mitigate expectation bias, our pipeline does not rely on within-prompt reasoning for de-biasing. Instead, we use structural anonymization (Phase 2) to remove source attribution at the input level."

### CR-5: New confound to acknowledge — implicit task-brief authority
Their work prompts a self-reflective limitation: every one of our 7 task briefs (A-G) contains **implicit authority framing**. Task A: "You are advising the board of a private SaaS company"; Task G: "You are advising the medical leadership of a regional health system". This framing **elevates** the perceived stakes — it's an implicit competence cue. Models might be raising their effort uniformly across all tasks, which could explain partial of our 49.5% task-variance finding.

> **Paper draft language**: "Following Sun et al. (2026), we note an implicit authority framing in our task briefs: each is presented as a high-stakes advisory context. This may inflate cross-task variance via task-dependent activation of the same authority-bias mechanism. A natural extension would replicate our design with low-authority framings (e.g., 'a draft from an intern') as a control."

---

## Slot for next addition

Future relevant work to incorporate here as we find it:
- Huh et al. (2024) Platonic Representation Hypothesis — we cite as opposed finding
- Original Kelly's Personal Construct Psychology / Repertory Grid — methodological foundation
- Cross-model LLM ensembling (mixture-of-agents) — practical application
- LLM-as-judge benchmarks (HELM, MT-Bench)

---

## Cross-references summary table

| Their finding | Our design / finding it touches | Where it goes in our paper |
|---|---|---|
| Quality cues bias LLM evaluation | Phase 2 anonymization (motivation) | Methods: anonymization rationale |
| Effect strongest at moderate mismatches (asymmetric) | Our task-dependent persona effect | Discussion: task-conditional analysis |
| LLMs less anchored than humans | Repertory Grid robustness on LLMs | Discussion: methodological contribution |
| CoT does not de-bias | Why we don't rely on CoT | Methods: de-biasing strategy |
| Implicit authority framing matters | Our task brief framing as confound | Limitations + future work |
