# CM-RG paper — для внешнего рецензирования

Здравствуйте,

Привожу к вашему сведению paper draft и сопровождающие материалы для CM-RG (Cross-Model Repertory Grid). 
Главные пункты, на которые хотелось бы получить обратную связь:

1. **Sections 5.1 — Lab vs Persona reversal**. Phase 1 (n=42) показал Lab > Persona × 2.3.
   Phase 2K (n=18,140 paired) показал обратное (0.07×). В Section 5.1 разобраны 4 механизма
   reversal'a. Достаточно ли убедительно объяснение? Что-то ещё нужно проговорить?

2. **Section 5.2 — Cohere outlier triangulation**. Cohere выделен 3 способами:
   PCA +26 units, mixed-effects β=+0.48 (p=1.6e-35, n=110K), persona-volatility SD=3.20.
   Не overclaim ли формулировка «structural outlier»?

3. **Section 2 — Related work**. Достаточно ли полное сравнение с JudgeLM/JudgeBench/MT-Bench/Chatbot Arena?
   Не упустил ли я какой-то crucial reference?

4. **Limitations** (Section 7) — 9 пунктов. Не пропустил ли важное ограничение?

Файлы в этой папке:
- paper_draft_v1.md — главный paper (~12 pages)
- arxiv_abstract_v1.md — abstract + key numbers + confidence ratings
- analysis_phase2j/REPORT.md — детали Phase 2J (Opus 4.7 vs 4.8 sanity check)
- analysis_phase2k/paired_ratio.json — raw данные Phase 2K
- analysis_combined/REPORT.md — все 5 фаз вместе
- analysis_combined/metrics.json — все числа
- analysis_combined/mixed_effects.json — Cohere mixed-effects models

Время на review: ~2-4 часа на главные секции.

Спасибо!
Сергей Долгов
sergey@archplg.co.uk
ORCID: 0000-0001-5455-7048
