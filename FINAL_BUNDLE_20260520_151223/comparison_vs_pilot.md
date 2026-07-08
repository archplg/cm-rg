# Pilot vs Cross-Model comparison

Pilot reference values (Claude Opus 4.7, role-played 5 ways):
- Task A: disagreement=0.31, PC1+PC2=0.776
- Task B: disagreement=0.14, PC1+PC2=0.757

Cross-model results:
- B_N_run3: disagreement=0.136, PC1+PC2=1.000
- B_P_run2: disagreement=0.946, PC1+PC2=1.000
- B_P_run3: disagreement=0.462, PC1+PC2=0.986

Key question: does cross-model raise the disagreement signal above 0.5 (pilot threshold for premature convergence)?
