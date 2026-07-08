ARXIV SUBMISSION FILES

Содержимое:
- paper_draft_v1.md - главный paper draft (~12 pages)
- arxiv_abstract_v1.md - abstract + key numbers + sub-claims confidence table

Конвертация в PDF/LaTeX перед submission:
  pandoc paper_draft_v1.md -o paper_v1.pdf --pdf-engine=xelatex

Что заполнять на arxiv.org/submit:
- Title: "Cross-Model Repertory Grid: Lab-Specific Persona Volatility in Frontier LLM Ensembles"
- Categories: cs.CL (primary) + cs.AI, cs.LG (cross-list)
- Authors: Sergey Dolgov (ORCID 0000-0001-5455-7048)
- Abstract: первые 250 слов из abstract секции paper_draft

Submission ТОЛЬКО после external review (см. 06_for_external_reviewer/).

См. 00_DEPLOY_GUIDE.md в корне для полной инструкции.
