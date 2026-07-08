# Reproducibility Appendix
This appendix contains all information needed to reproduce the experiment.

## Run manifest
- Started: `2026-05-20T17:37:39.625247` (Марокко (лето))
- Python: `3.14.3`
- Platform: `Windows-11-10.0.26200-SP0`
- Script SHA-256: `bf92dbb9a1e201e4d32af47305bf606e85800eac508603a6ad7fd7b58c244063`
- Config SHA-256: `0f4e7d2d52715a4d6f9e56ac878446faa6238c5a812812feb84a87301319276e`
- Analyzer SHA-256: `b0ee942d65142ddba7a7e279208db7d4b6f6e6da21036ad5698438f9f3cb0465`

### Package versions
- `requests` = `2.32.5`
- `yaml` = `6.0.3`
- `pandas` = `2.3.3`
- `numpy` = `2.4.0`
- `sklearn` = `1.8.0`
- `scipy` = `1.17.1`
- `matplotlib` = `3.10.8`
- `seaborn` = `0.13.2`

## Models used (snapshot at run start)

### M1 (anthropic)
- Primary ID: `anthropic/claude-opus-4.7`
- Fallback ID: `anthropic/claude-sonnet-4.6`
- Context length: 1000000
- Pricing (USD/token): input=`0.000005`, output=`0.000025`

### M2 (openai)
- Primary ID: `openai/gpt-5.5`
- Fallback ID: `openai/gpt-5.4`
- Context length: 1050000
- Pricing (USD/token): input=`0.000005`, output=`0.00003`

### M3 (google)
- Primary ID: `google/gemini-3.1-pro-preview`
- Fallback ID: `google/gemini-2.5-pro`
- Context length: 1048576
- Pricing (USD/token): input=`0.000002`, output=`0.000012`

### M4 (deepseek)
- Primary ID: `deepseek/deepseek-v4-pro`
- Fallback ID: `deepseek/deepseek-v4-flash`
- Context length: 1048576
- Pricing (USD/token): input=`0.000000435`, output=`0.00000087`

### M5 (moonshot)
- Primary ID: `moonshotai/kimi-k2.6`
- Fallback ID: `moonshotai/kimi-k2.5`
- Context length: 262144
- Pricing (USD/token): input=`0.00000073`, output=`0.00000349`

## Cells executed
- `A_N_run1` (task A, cond N, run 1): status `complete_with_errors`, seed `1922324602`, started `2026-05-20T16:06:45.788513`, completed `2026-05-20T16:32:25.662272`
- `A_P_run1` (task A, cond P, run 1): status `complete_with_errors`, seed `104112784`, started `2026-05-20T16:32:35.027078`, completed `2026-05-20T16:50:07.199136`
- `B_N_run1` (task B, cond N, run 1): status `complete_with_errors`, seed `1346548351`, started `2026-05-20T16:50:14.535217`, completed `2026-05-20T17:19:37.163244`
- `B_N_run2` (task B, cond N, run 2): status `complete_with_errors`, seed `866705477`, started `2026-05-20T17:37:39.705975`, completed `2026-05-20T17:55:15.517878`
- `B_N_run3` (task B, cond N, run 3): status `complete_with_errors`, seed `3194823768`, started `2026-05-20T00:26:39.898538`, completed `2026-05-20T00:34:16.972378`
- `B_P_run1` (task B, cond P, run 1): status `complete_with_errors`, seed `179577108`, started `2026-05-20T17:19:54.938260`, completed `2026-05-20T17:37:30.525564`
- `B_P_run2` (task B, cond P, run 2): status `complete_with_errors`, seed `2156002978`, started `2026-05-20T00:41:48.362123`, completed `2026-05-20T00:50:06.304260`
- `B_P_run3` (task B, cond P, run 3): status `complete_with_errors`, seed `2483770396`, started `2026-05-20T00:50:06.318570`, completed `2026-05-20T01:01:04.334260`
- `C_N_run1` (task C, cond N, run 1): status `complete_with_errors`, seed `3233545189`, started `2026-05-20T01:01:04.348230`, completed `2026-05-20T01:09:47.546206`
- `C_P_run1` (task C, cond P, run 1): status `complete_with_errors`, seed `639448267`, started `2026-05-20T01:09:47.563097`, completed `2026-05-20T01:24:53.897378`

## Random seeds
Each cell uses a deterministic seed derived from its `cell_id` (see `random_seed` field in `cell.json`). The same seed governs:
- Element label permutation (anonymization step)
- Triad assignment to agents

## Full prompts
Every API call's full system prompt and user prompt are stored in `logs/api_calls/<cell_id>/<phase>_<model>_<attempt>.json`. These files also contain the full raw API response and the request payload sent.

## Configuration
Complete configuration used in this run:

```yaml
experiment:
  name: archipelago_cross_model_v1
  description: Cross-model replication of Archipelago-for-Agents pilot
  total_budget_usd: 80
  estimated_budget_usd: 45
  output_dir: ./results
  log_dir: ./logs
openrouter:
  base_url: https://openrouter.ai/api/v1
  api_key_env: OPENROUTER_API_KEY
  retries_per_call: 3
  retry_backoff_seconds:
  - 2
  - 5
  - 15
  request_timeout_seconds: 120
models:
- id: anthropic/claude-opus-4.7
  fallback_id: anthropic/claude-sonnet-4.6
  family: anthropic
  short_name: M1
  notes: Anthropic frontier
- id: openai/gpt-5.5
  fallback_id: openai/gpt-5.4
  family: openai
  short_name: M2
  notes: OpenAI frontier. May require fallback if 5.5 API not yet public.
- id: google/gemini-3.1-pro-preview
  fallback_id: google/gemini-2.5-pro
  family: google
  short_name: M3
  notes: Google frontier. Preview status May 2026. Fallback updated 2026-05-19 from
    gemini-3-pro (not in catalog) to gemini-2.5-pro (stable, same Pro-tier, 1M context,
    $1.25/$10).
- id: deepseek/deepseek-v4-pro
  fallback_id: deepseek/deepseek-v4-flash
  family: deepseek
  short_name: M4
  notes: Chinese frontier closed-train, different RLHF distribution
- id: moonshotai/kimi-k2.6
  fallback_id: moonshotai/kimi-k2.5
  family: moonshot
  short_name: M5
  notes: Chinese frontier; open-weight, different training
parameters:
  free_response:
    temperature: 1.0
    max_tokens: 3000
  constructs:
    temperature: 1.0
    max_tokens: 2000
  ratings:
    temperature: 0.0
    max_tokens: 2500
tasks:
- id: A
  brief_file: tasks/task_A_brief.md
  domain: strategic_capital_allocation
- id: B
  brief_file: tasks/task_B_brief.md
  domain: team_diagnostic
  is_repeat_task: true
- id: C
  brief_file: tasks/task_C_brief.md
  domain: product_ethics
conditions:
- id: N
  name: neutral
  system_prompt: You are an analyst. Read the brief carefully and provide your best-reasoned
    recommendation.
  use_personas: false
- id: P
  name: persona
  use_personas: true
  persona_assignment:
    A:
      M1: Q
      M2: S
      M3: E
      M4: H
      M5: C
    B:
      M1: S
      M2: E
      M3: H
      M4: C
      M5: Q
    C:
      M1: E
      M2: H
      M3: C
      M4: Q
      M5: S
repetitions:
  base_runs_per_cell: 1
  extra_runs_for_repeat_task: 2
pipeline:
  n_triads_per_agent: 3
  n_elements: 5
  rating_scale:
  - 1
  - 7
  triad_assignment_strategy: balanced_random
preflight:
  verify_api_key: true
  verify_model_ids: true
  estimate_cost: true
  require_user_confirmation: true
  dry_run_mode: false
```
