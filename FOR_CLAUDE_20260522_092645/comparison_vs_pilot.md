# Pilot vs Cross-Model comparison

Pilot reference values (Claude Opus 4.7, role-played 5 ways):
- Task A: disagreement=0.31, PC1+PC2=0.776
- Task B: disagreement=0.14, PC1+PC2=0.757

Cross-model results:
- A_N_run1: disagreement=0.627, PC1+PC2=0.785
- A_N_run2: disagreement=1.246, PC1+PC2=0.819
- A_N_run3: disagreement=1.029, PC1+PC2=0.637
- A_N_run4: disagreement=0.739, PC1+PC2=0.829
- A_N_run5: disagreement=0.863, PC1+PC2=0.697
- A_P_run1: disagreement=0.354, PC1+PC2=0.939
- A_P_run2: disagreement=0.362, PC1+PC2=0.933
- A_P_run3: disagreement=0.552, PC1+PC2=0.974
- A_P_run4: disagreement=0.349, PC1+PC2=0.730
- A_P_run5: disagreement=0.503, PC1+PC2=0.871
- B_N_run1: disagreement=0.066, PC1+PC2=0.999
- B_N_run2: disagreement=0.446, PC1+PC2=0.994
- B_N_run3: disagreement=0.387, PC1+PC2=0.993
- B_N_run4: disagreement=0.619, PC1+PC2=0.950
- B_N_run5: disagreement=0.092, PC1+PC2=1.000
- B_P_run1: disagreement=0.276, PC1+PC2=0.956
- B_P_run2: disagreement=0.362, PC1+PC2=0.981
- B_P_run3: disagreement=0.410, PC1+PC2=0.938
- B_P_run4: disagreement=0.348, PC1+PC2=0.852
- B_P_run5: disagreement=0.416, PC1+PC2=0.982

Key question: does cross-model raise the disagreement signal above 0.5 (pilot threshold for premature convergence)?
