# Deviations from pre-registration

**D1 (documented before wave-2 data collection, 2026-07-21).** Wave 1 hit a
full ceiling: all four models scored 20/20. Consequences: H-A is a tie at
ceiling (uninformative), H-C is untestable (no incorrect answers, no
non-converged items). Arm 2 on wave-1 items was skipped as uninformative
(every condition would measure 100%). This ceiling is itself a finding: on
cleanly-specified computational items of this class, the whole 2026 Claude
family - including the cheap tier - no longer makes errors.

**D2: exploratory wave 2.** Ten substantially harder items
(`wave2_items.py`: exact 6x6-digit multiplication, a 118-step Collatz
trajectory, digit sum of 3^50, substring counting over a 2000-range, circular
seating with two adjacency bans, constrained strings, CRT, all-odd-digit
sums, digit-avoiding sequences, grid-square counting), ground truth computed
by code. Labeled exploratory: items were designed AFTER seeing wave-1
results (to escape the ceiling), but the following predictions are locked
BEFORE any wave-2 model call:

1. Accuracy leaves the ceiling: haiku in the 30-60% band; sonnet/opus/fable
   in the 50-90% band. W2 (Collatz, 118 exact iterations, no tools) near 0%
   for every model.
2. H-C becomes testable and confirms: items where haiku matches the trio
   majority are >= 20 percentage points more accurate than items where it
   does not, with both classes non-empty.
3. H-A unchanged: Panel R (opus, fable, sonnet) >= Panel D (haiku, fable,
   sonnet) - the capability confound dominates.
4. H-B unchanged: persona panel vs neutral panel approximately tie (margin
   < 3 items) on computational items.

Arm 2 runs on wave 2 only: fable x 3 personas (Q, S, C) and fable x 3
independent neutral runs, one batch of 10 items each.

**D3 (documented after wave-2 arm-1, before arm-2 and scoring).** The W10
ground truth was WRONG (off-by-one in the generator: 85 instead of 133). It
was caught precisely by the mechanism under test: all four models unanimously
converged on 133 against the "gold" answer, which triggered an audit of the
generator; an independent brute-force enumeration confirmed 133. Ground truth
corrected before scoring; no model answers were changed. Two lessons recorded:
(1) unanimous cross-model convergence against a reference answer is a strong
signal to audit the reference - the convergence signal works in both
directions; (2) wave-2 prediction 1 was miscalibrated: models handled even the
118-step Collatz trace flawlessly - the 2026 Claude family is far stronger at
exact long iteration than assumed.
