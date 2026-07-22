# Reproducibility Appendix
This appendix contains all information needed to reproduce the experiment.

## Run manifest
- Started: `2026-05-21T00:15:51.838864` (Марокко (лето))
- Python: `3.14.3`
- Platform: `Windows-11-10.0.26200-SP0`
- Script SHA-256: `bf92dbb9a1e201e4d32af47305bf606e85800eac508603a6ad7fd7b58c244063`
- Config SHA-256: `76f497730d0f5c5bd57cd5bcc23692b79d7b181c3c067da6a5e9bcaf2bf65bc8`
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
- `A_N_run1` (task A, cond N, run 1): status `complete_with_errors`, seed `2582843996`, started `2026-05-21T00:15:51.914143`, completed `2026-05-21T00:40:12.643114`
- `A_N_run2` (task A, cond N, run 2): status `complete_with_errors`, seed `1896684825`, started `2026-05-21T01:01:31.863068`, completed `2026-05-21T01:24:39.169717`
- `A_N_run3` (task A, cond N, run 3): status `complete_with_errors`, seed `2377072954`, started `2026-05-21T01:24:39.188359`, completed `2026-05-21T01:48:42.561211`
- `A_N_run4` (task A, cond N, run 4): status `complete_with_errors`, seed `3189538891`, started `2026-05-21T01:48:42.582858`, completed `2026-05-21T02:15:43.777982`
- `A_N_run5` (task A, cond N, run 5): status `complete_with_errors`, seed `187028733`, started `2026-05-21T02:15:43.797799`, completed `2026-05-21T02:39:31.913575`
- `A_P_run1` (task A, cond P, run 1): status `complete_with_errors`, seed `1682606017`, started `2026-05-21T00:40:12.656361`, completed `2026-05-21T01:01:31.849229`
- `A_P_run2` (task A, cond P, run 2): status `complete_with_errors`, seed `2778232070`, started `2026-05-21T02:39:31.937811`, completed `2026-05-21T03:04:00.611449`
- `A_P_run3` (task A, cond P, run 3): status `complete_with_errors`, seed `3161029315`, started `2026-05-21T03:04:00.632197`, completed `2026-05-21T03:30:58.869386`
- `A_P_run4` (task A, cond P, run 4): status `complete_with_errors`, seed `2834428565`, started `2026-05-21T03:30:58.893612`, completed `2026-05-21T03:48:26.468360`
- `A_P_run5` (task A, cond P, run 5): status `complete_with_errors`, seed `4029450120`, started `2026-05-21T03:48:26.499863`, completed `2026-05-21T04:30:36.336965`
- `B_N_run1` (task B, cond N, run 1): status `complete_with_errors`, seed `2088540365`, started `2026-05-21T04:30:36.367016`, completed `2026-05-21T04:55:14.370454`
- `B_N_run2` (task B, cond N, run 2): status `complete_with_errors`, seed `955999049`, started `2026-05-20T20:10:57.073105`, completed `2026-05-20T20:31:20.331365`
- `B_N_run3` (task B, cond N, run 3): status `complete_with_errors`, seed `4175949436`, started `2026-05-21T05:17:19.191153`, completed `2026-05-21T05:41:08.224189`
- `B_N_run4` (task B, cond N, run 4): status `complete_with_errors`, seed `4204910723`, started `2026-05-21T05:41:08.260388`, completed `2026-05-21T06:06:18.893617`
- `B_N_run5` (task B, cond N, run 5): status `complete_with_errors`, seed `2106206825`, started `2026-05-21T06:06:18.963947`, completed `2026-05-21T06:24:52.124866`
- `B_P_run1` (task B, cond P, run 1): status `complete_with_errors`, seed `1465623990`, started `2026-05-21T04:55:14.399115`, completed `2026-05-21T05:17:19.154270`
- `B_P_run2` (task B, cond P, run 2): status `complete_with_errors`, seed `141489055`, started `2026-05-21T06:24:52.163734`, completed `2026-05-21T06:43:49.636726`
- `B_P_run3` (task B, cond P, run 3): status `complete_with_errors`, seed `2072627240`, started `2026-05-21T06:43:49.676087`, completed `2026-05-21T07:03:41.446142`
- `B_P_run4` (task B, cond P, run 4): status `complete_with_errors`, seed `4033503338`, started `2026-05-21T07:03:41.487712`, completed `2026-05-21T07:27:30.847989`
- `B_P_run5` (task B, cond P, run 5): status `complete_with_errors`, seed `2056530620`, started `2026-05-21T07:27:30.890132`, completed `2026-05-21T08:05:41.341809`
- `C_N_run1` (task C, cond N, run 1): status `complete_with_errors`, seed `3981572348`, started `2026-05-21T08:05:41.383695`, completed `2026-05-21T08:35:16.062899`
- `C_N_run2` (task C, cond N, run 2): status `complete_with_errors`, seed `4182102602`, started `2026-05-21T09:02:47.053438`, completed `2026-05-21T09:24:59.624589`
- `C_N_run3` (task C, cond N, run 3): status `complete_with_errors`, seed `1830742463`, started `2026-05-21T09:24:59.675490`, completed `2026-05-21T09:47:45.432507`
- `C_N_run4` (task C, cond N, run 4): status `complete_with_errors`, seed `3627798348`, started `2026-05-21T09:47:45.489930`, completed `2026-05-21T10:16:33.703525`
- `C_N_run5` (task C, cond N, run 5): status `complete_with_errors`, seed `3085781281`, started `2026-05-21T10:16:33.754338`, completed `2026-05-21T10:36:39.684733`
- `C_P_run1` (task C, cond P, run 1): status `complete_with_errors`, seed `908279425`, started `2026-05-21T08:35:16.549530`, completed `2026-05-21T09:02:47.002443`
- `C_P_run2` (task C, cond P, run 2): status `complete_with_errors`, seed `2916048243`, started `2026-05-21T10:36:39.760449`, completed `2026-05-21T11:01:28.001408`
- `C_P_run3` (task C, cond P, run 3): status `complete_with_errors`, seed `1858534644`, started `2026-05-21T11:01:28.094462`, completed `2026-05-21T11:22:07.353784`
- `C_P_run4` (task C, cond P, run 4): status `complete_with_errors`, seed `1952947091`, started `2026-05-21T11:22:07.447112`, completed `2026-05-21T11:43:32.301519`
- `C_P_run5` (task C, cond P, run 5): status `complete_with_errors`, seed `268137072`, started `2026-05-21T11:43:32.389760`, completed `2026-05-21T12:09:07.636386`
- `D_N_run1` (task D, cond N, run 1): status `complete_with_errors`, seed `2895000390`, started `2026-05-21T12:09:07.709788`, completed `2026-05-21T12:31:06.453693`
- `D_N_run2` (task D, cond N, run 2): status `complete_with_errors`, seed `3234487946`, started `2026-05-21T12:49:53.235015`, completed `2026-05-21T13:16:23.291152`
- `D_N_run3` (task D, cond N, run 3): status `complete_with_errors`, seed `3211560204`, started `2026-05-21T13:16:23.384050`, completed `2026-05-21T13:29:27.630786`
- `D_N_run4` (task D, cond N, run 4): status `complete_with_errors`, seed `3163413427`, started `2026-05-21T13:29:27.719662`, completed `2026-05-21T13:50:25.115577`
- `D_N_run5` (task D, cond N, run 5): status `complete_with_errors`, seed `348292117`, started `2026-05-21T13:50:25.246206`, completed `2026-05-21T14:08:25.337590`
- `D_P_run1` (task D, cond P, run 1): status `complete_with_errors`, seed `3041168111`, started `2026-05-21T12:31:06.538870`, completed `2026-05-21T12:49:53.119929`
- `D_P_run2` (task D, cond P, run 2): status `complete_with_errors`, seed `2235787682`, started `2026-05-21T14:08:25.453930`, completed `2026-05-21T14:29:41.148098`
- `D_P_run3` (task D, cond P, run 3): status `complete_with_errors`, seed `114259861`, started `2026-05-21T14:29:41.248137`, completed `2026-05-21T14:51:44.942378`
- `D_P_run4` (task D, cond P, run 4): status `complete_with_errors`, seed `2233626644`, started `2026-05-21T14:51:45.045230`, completed `2026-05-21T15:11:31.768912`
- `D_P_run5` (task D, cond P, run 5): status `complete_with_errors`, seed `1481340849`, started `2026-05-21T15:11:31.882190`, completed `2026-05-21T15:40:18.078166`
- `E_N_run1` (task E, cond N, run 1): status `complete_with_errors`, seed `2806444017`, started `2026-05-21T15:40:18.203027`, completed `2026-05-21T16:09:28.405840`
- `E_N_run2` (task E, cond N, run 2): status `complete_with_errors`, seed `2555769846`, started `2026-05-21T16:28:32.171274`, completed `2026-05-21T16:58:02.719526`
- `E_N_run3` (task E, cond N, run 3): status `complete_with_errors`, seed `3710239331`, started `2026-05-21T16:58:02.848012`, completed `2026-05-21T17:34:28.308590`
- `E_N_run4` (task E, cond N, run 4): status `complete_with_errors`, seed `3826224162`, started `2026-05-21T17:34:28.451858`, completed `2026-05-21T18:04:54.530711`
- `E_N_run5` (task E, cond N, run 5): status `complete_with_errors`, seed `2799263121`, started `2026-05-21T18:04:54.666882`, completed `2026-05-21T18:33:50.294043`
- `E_P_run1` (task E, cond P, run 1): status `complete_with_errors`, seed `92530471`, started `2026-05-21T16:09:28.512486`, completed `2026-05-21T16:28:32.054407`
- `E_P_run2` (task E, cond P, run 2): status `complete_with_errors`, seed `3491607552`, started `2026-05-21T18:33:50.432823`, completed `2026-05-21T19:01:50.955067`
- `E_P_run3` (task E, cond P, run 3): status `complete_with_errors`, seed `2278263040`, started `2026-05-21T19:01:51.097137`, completed `2026-05-21T19:21:06.158557`
- `E_P_run4` (task E, cond P, run 4): status `complete_with_errors`, seed `1338103280`, started `2026-05-21T19:21:06.289552`, completed `2026-05-21T19:48:50.097948`
- `E_P_run5` (task E, cond P, run 5): status `complete_with_errors`, seed `423516920`, started `2026-05-21T19:48:50.270390`, completed `2026-05-21T20:10:43.959288`
- `F_N_run1` (task F, cond N, run 1): status `complete_with_errors`, seed `1570521870`, started `2026-05-21T20:10:44.058038`, completed `2026-05-21T20:34:08.471310`
- `F_N_run2` (task F, cond N, run 2): status `complete_with_errors`, seed `667182767`, started `2026-05-21T21:02:57.335898`, completed `2026-05-21T21:26:59.024722`
- `F_N_run3` (task F, cond N, run 3): status `complete_with_errors`, seed `1244117379`, started `2026-05-21T21:26:59.166829`, completed `2026-05-21T21:49:01.282815`
- `F_N_run4` (task F, cond N, run 4): status `complete_with_errors`, seed `2112866637`, started `2026-05-21T21:49:01.409592`, completed `2026-05-21T22:05:55.938342`
- `F_N_run5` (task F, cond N, run 5): status `complete_with_errors`, seed `1251441274`, started `2026-05-21T22:05:56.085891`, completed `2026-05-21T22:30:40.690425`
- `F_P_run1` (task F, cond P, run 1): status `complete_with_errors`, seed `1067869337`, started `2026-05-21T20:34:08.597481`, completed `2026-05-21T21:02:57.232755`
- `F_P_run2` (task F, cond P, run 2): status `complete_with_errors`, seed `3385077229`, started `2026-05-21T22:30:40.836631`, completed `2026-05-21T22:54:57.119737`
- `F_P_run3` (task F, cond P, run 3): status `complete_with_errors`, seed `150145966`, started `2026-05-21T22:54:57.257749`, completed `2026-05-21T23:21:37.498131`
- `F_P_run4` (task F, cond P, run 4): status `complete_with_errors`, seed `2124161299`, started `2026-05-21T23:21:37.667017`, completed `2026-05-21T23:51:07.104581`
- `F_P_run5` (task F, cond P, run 5): status `complete_with_errors`, seed `1016994758`, started `2026-05-21T23:51:07.251242`, completed `2026-05-22T00:12:41.158024`
- `G_N_run1` (task G, cond N, run 1): status `complete_with_errors`, seed `3916967629`, started `2026-05-22T00:12:41.271703`, completed `2026-05-22T00:34:02.596042`
- `G_N_run2` (task G, cond N, run 2): status `complete_with_errors`, seed `476066805`, started `2026-05-22T00:55:40.246864`, completed `2026-05-22T01:14:55.332315`
- `G_N_run3` (task G, cond N, run 3): status `complete_with_errors`, seed `2731307551`, started `2026-05-22T01:14:55.475627`, completed `2026-05-22T01:35:18.031362`
- `G_N_run4` (task G, cond N, run 4): status `complete_with_errors`, seed `553623757`, started `2026-05-22T01:35:18.215724`, completed `2026-05-22T01:59:14.355636`
- `G_N_run5` (task G, cond N, run 5): status `complete_with_errors`, seed `991801814`, started `2026-05-22T01:59:14.509665`, completed `2026-05-22T02:28:11.919210`
- `G_P_run1` (task G, cond P, run 1): status `complete_with_errors`, seed `4285350435`, started `2026-05-22T00:34:02.755348`, completed `2026-05-22T00:55:40.114758`
- `G_P_run2` (task G, cond P, run 2): status `complete_with_errors`, seed `2066959540`, started `2026-05-22T02:28:12.094746`, completed `2026-05-22T02:43:22.606491`
- `G_P_run3` (task G, cond P, run 3): status `complete_with_errors`, seed `3561753284`, started `2026-05-22T02:43:22.780538`, completed `2026-05-22T03:00:50.104044`
- `G_P_run4` (task G, cond P, run 4): status `complete_with_errors`, seed `1492496703`, started `2026-05-22T03:00:50.238767`, completed `2026-05-22T03:22:36.263758`
- `G_P_run5` (task G, cond P, run 5): status `complete_with_errors`, seed `2793082485`, started `2026-05-22T03:22:36.383876`, completed `2026-05-22T03:47:58.492288`

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
  name: archipelago_cross_model_phase2
  description: Phase 2 expansion - 7 tasks for paper-quality stats
  total_budget_usd: 100
  estimated_budget_usd: 30
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
  notes: OpenAI frontier
- id: google/gemini-3.1-pro-preview
  fallback_id: google/gemini-2.5-pro
  family: google
  short_name: M3
  notes: Google frontier - Procrustes outlier in Phase 1; monitor in Phase 2
- id: deepseek/deepseek-v4-pro
  fallback_id: deepseek/deepseek-v4-flash
  family: deepseek
  short_name: M4
  notes: Chinese frontier
- id: moonshotai/kimi-k2.6
  fallback_id: moonshotai/kimi-k2.5
  family: moonshot
  short_name: M5
  notes: Chinese frontier thinking-model
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
  is_repeat_task: true
- id: B
  brief_file: tasks/task_B_brief.md
  domain: team_diagnostic
  is_repeat_task: true
- id: C
  brief_file: tasks/task_C_brief.md
  domain: product_ethics
  is_repeat_task: true
- id: D
  brief_file: tasks/task_D_brief.md
  domain: climate_adaptation
  is_repeat_task: true
- id: E
  brief_file: tasks/task_E_brief.md
  domain: ai_governance
  is_repeat_task: true
- id: F
  brief_file: tasks/task_F_brief.md
  domain: product_launch_strategy
  is_repeat_task: true
- id: G
  brief_file: tasks/task_G_brief.md
  domain: medical_triage_ethics
  is_repeat_task: true
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
    D:
      M1: H
      M2: C
      M3: Q
      M4: S
      M5: E
    E:
      M1: C
      M2: Q
      M3: S
      M4: E
      M5: H
    F:
      M1: Q
      M2: S
      M3: E
      M4: H
      M5: C
    G:
      M1: S
      M2: E
      M3: H
      M4: C
      M5: Q
repetitions:
  base_runs_per_cell: 1
  extra_runs_for_repeat_task: 4
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
