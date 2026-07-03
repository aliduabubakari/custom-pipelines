# Custom Pipelines — Documentation

## Contents

| Document | Description |
|---|---|
| [`DATASET_CREATION.md`](./DATASET_CREATION.md) | Complete methodology for how the 100 pipelines were created — from source datasets through generation to post-processing refinement |

## Quick Links

- **Repository:** [github.com/aliduabubakari/custom-pipelines](https://github.com/aliduabubakari/custom-pipelines)
- **Source Dataset:** [DataScience-Instruct-500K](https://huggingface.co/datasets/RUC-DataLab/DataScience-Instruct-500K)
- **Generation Model:** [DeepAnalyze-8B](https://huggingface.co/RUC-DataLab/DeepAnalyze-8B)
- **Paper:** [DeepAnalyze: Agentic Large Language Models for Autonomous Data Science](https://arxiv.org/abs/2510.16872)

## Pipeline Architecture

Every pipeline follows a standardized structure:

```
NNN_pipeline_name/
├── Dockerfile              # Container build specification
├── requirements.txt        # Python dependencies (auto-detected)
├── pipeline.yaml           # Argo Workflow definition
├── pipeline.md             # Full documentation with business context
├── data/                   # Input datasets
└── scripts/                # Python scripts (6–16 per pipeline)
```

## Pipeline Categories

- **Category A (001–013):** Hand-curated from real-world ML projects
- **Category B (014–100):** LLM-generated from DeepAnalyze-8B trajectories
