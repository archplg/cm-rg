GITHUB REPO BUNDLE

Структура:
- README.md - главный README (показывается на github.com/archplg/cm-rg)
- DATASET_CARD.md - копия HF dataset card
- .gitignore
- scripts/ - 9 Python скриптов (run_experiment, analyze_*, verify, build_dataset, etc.)
- configs/ - 2 YAML конфига (phase2j, phase2k)
- tasks/ - 13 task briefs (A-J + 10-option variants A10/D10/G10)
- analysis_outputs/ - results JSON/MD/CSV (без сырого raw data - оно на HF)

PUSH КОМАНДА:
  cd 03_github_repo
  git init
  git add .
  git commit -m "CM-RG v1.0"
  git remote add origin https://github.com/archplg/cm-rg.git
  git push -u origin main
  git tag v1.0
  git push origin v1.0  # для Zenodo DOI

Pre-requisites:
- Пустое репо https://github.com/archplg/cm-rg создано
- SSH key или PAT настроен

См. 00_DEPLOY_GUIDE.md в корне для полной инструкции.
