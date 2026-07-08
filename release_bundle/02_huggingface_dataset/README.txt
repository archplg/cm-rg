HUGGINGFACE DATASET UPLOAD

Содержимое:
- README.md - dataset card (показывается на HF Hub)
- CITATION.cff - citation file
- LICENSE - CC-BY 4.0 text
- metadata.json - build metadata
- data/cells.parquet (98 rows)
- data/responses.parquet (684 rows)
- data/constructs.parquet (1,861 rows)
- data/ratings.parquet (110,882 rows)
- data/api_calls.parquet (2,004 rows)

UPLOAD КОМАНДА (новая, hf вместо deprecated huggingface-cli):
  cd 02_huggingface_dataset
  hf auth login
  hf upload sergeydolgov/cross-model-repertory-grid . --repo-type=dataset

Pre-requisites:
- HF account создан, email подтверждён
- Пустой dataset уже создан на https://huggingface.co/datasets/sergeydolgov/cross-model-repertory-grid
- hf access token имеет "write" права

См. 00_DEPLOY_GUIDE.md в корне для полной инструкции.
