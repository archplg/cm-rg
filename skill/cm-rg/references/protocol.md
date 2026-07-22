# CM-RG protocol reference

Prompts below are copied **verbatim** from the Archipelago Phase 2L pipeline
(`run_phase2l.py`, June 2026). Do not paraphrase them: the published baselines
(mean inter-rater r = 0.200 across 36 models; within-family r ~0.34-0.45) were
measured with these exact instructions, and comparability is the point.

## Phase 1 - free response

System prompt, neutral condition (the default):

```
You are an analyst. Read the brief carefully. Provide your best-reasoned recommendation in 300-500 words. Be specific - advocate clearly for one approach. Brief follows.
```

User message: the full task brief text.

Persona condition (optional, for persona-effect designs) - prepend one of:

```
Q: You are a Quantitative analyst. Prioritize data, models, and measurable outcomes.
S: You are a Strategic advisor. Prioritize long-term positioning and competitive dynamics.
E: You are an Ethical evaluator. Prioritize stakeholder welfare and fairness.
H: You are a Humanistic counselor. Prioritize relationships, identity, and meaning.
C: You are a Conservative steward. Prioritize risk reduction and continuity.
```

Subagent framing: when the "model" is a subagent in an agent harness, add an
operational wrapper AFTER the system prompt content, e.g. "Do not use any
tools. Return only the recommendation text, nothing else." - operational
instructions are allowed; evaluative instructions beyond the template are not.

Sampling: temperature 1.0 where controllable (diversity is wanted in Phase 1
and 3), max ~800 tokens.

## Phase 2 - anonymization (computational, no model calls)

Run `scripts/anonymize.py`. It applies these regex substitutions (ported
verbatim), collapses whitespace, then shuffles element order with a seed and
assigns labels E1..EN:

1. `(?i)\b(I\s+am\s+|I'm\s+)(claude|gpt|chatgpt|gemini|llama|mistral|deepseek|grok|qwen|kimi|glm|nemotron|command|granite)\b[^.]*\.` -> removed
2. `(?i)\b(as\s+an\s+ai\s+(language\s+)?model|as\s+a\s+language\s+model)\b[^.]*\.` -> removed
3. `(?i)\b(I\s+should\s+(note|mention|clarify)|it's\s+worth\s+noting)\b[^.]*\.` -> removed
4. `(?i)\b(developed\s+by|trained\s+by|built\s+by)\s+(anthropic|openai|google|meta|mistral|deepseek|xai|alibaba|moonshot|zhipu|nvidia|cohere|ibm)\b[^.]*\.` -> removed
5. `(?i)\b(Claude|GPT-?\d?\.?\d?|Gemini|LLaMA|Mistral|DeepSeek|Grok|Qwen|Kimi|GLM|Nemotron|Command|Granite)\b` -> `[MODEL]`
6. `(?i)\b(Anthropic|OpenAI|Google DeepMind|DeepMind|Meta AI|Mistral AI|xAI|Alibaba|Moonshot|Zhipu|NVIDIA|Cohere|IBM Research)\b` -> `[LAB]`

The element-label mapping (`mapping.json`) never appears in any later prompt.

Addition for arbitrary model lists (OpenRouter runner): the fixed patterns
above only know famous model names. `run_openrouter.py` additionally redacts
each participating model's full slug, org prefix and name part
(`dynamic_redact`), so self-identification by models outside the fixed list is
stripped too. This is an anonymization-strengthening addition, not a prompt
change - grids remain comparable.

## Phase 3 - triadic elicitation

System prompt:

```
You are participating in a Personal Constructs research study. You will see three anonymized advisory responses to the same brief. Your task: identify constructs - bipolar dimensions on which responses differ. Use the triadic method: for each construct, two responses share a quality that the third lacks.

Output ONLY valid JSON in this format:
[{"pole_a": "decisive", "pole_b": "deliberative", "context": "decision style"}, ...]

Provide 8-12 constructs. Each pole should be a single adjective or short noun phrase. Do not include any text outside the JSON array.
```

User message:

```
Three anonymized responses:

[E2]
<text>

[E4]
<text>

[E1]
<text>

Identify 8-12 constructs.
```

Triad assignment - each rater gets one distinct triad, deterministic
(seed 42 in the reference pipeline). For small N use:

| N elements | Triads in order (rater 1, 2, 3, ...) |
|---|---|
| 3 | (E1,E2,E3) for every rater |
| 4 | (E1,E2,E3) (E1,E2,E4) (E1,E3,E4) (E2,E3,E4) |
| 5 | (E1,E2,E3) (E2,E3,E4) (E3,E4,E5) (E4,E5,E1) (E5,E1,E2) |
| 6 | (E1,E2,E3) (E2,E3,E4) (E3,E4,E5) (E4,E5,E6) (E5,E6,E1) (E6,E1,E2) |

A rater may see a triad containing its own anonymized response - that is by
design (it cannot know which one it is).

Temperature 1.0 where controllable, max ~600 tokens.

## Phase 4 - cross-rating

System prompt:

```
You are rating advisory responses on a personal constructs grid. You will see a list of CONSTRUCTS (bipolar dimensions) and a list of anonymized RESPONSES. Rate each response on each construct using a 1-7 scale where 1=strongly pole_a, 7=strongly pole_b, 4=neutral.

Output ONLY valid JSON: {"ratings": [[1, 4, 7, ...], ...]} where outer array is per-response, inner array is per-construct in the listed order. No text outside the JSON.
```

User message: numbered construct list (`1. decisive vs deliberative (decision
style)`), then the anonymized responses with their E-labels, then: `Rate all
N responses on all K constructs.`

Batching: at most 50 constructs per call (output token limits). Temperature
0.0 where controllable (stability is wanted in ratings). Every rater rates
every element - including, unknowingly, its own response.

Parsing: models sometimes wrap JSON in markdown fences or reasoning tags.
Strip `<thinking>`-style tags and ``` fences before `json.loads`; if the
result still fails, extract the outermost balanced `{...}` containing a
"ratings" key. Re-ask once on failure; after that, record the cell as null
and disclose the gap in the report.

## Provenance

Method: Kelly, G. A. (1955), The Psychology of Personal Constructs.
Pipeline and prompts: Archipelago Research, CM-RG Phase 2L (June 2026),
github.com/archplg/cm-rg. If you modify any prompt, you are running a variant:
label results as such and do not compare them against the published baselines.
