# Data Ingestion Commands

Here are the ingestion commands for the 3 useful cases:

## 1. Ingest only clean data

```bash
python -m app.ingestion.processor DATA/true_data true
```

This wipes Qdrant first, then indexes only the clean documents from `DATA/true_data`.

## 2. Ingest only 10 noisy files
 
```bash
python -m app.ingestion.processor DATA/noisy_sample_10 noisy
```

## 3. Ingest only 15 noisy files

```bash
python -m app.ingestion.processor DATA/noisy_sample_15 noisy
```

> Use `--wipe` when you want a fresh Qdrant collection. If you want to append noisy files after clean data, omit `--wipe` on the noisy ingestion command.

## Pipeline / Architecture

The diagram shows the following flow:

- Golden Dataset
  - 15 RAG QA samples
  - 6 guardrail samples
  - `eval/golden_dataset.json`

- FastAPI / Streamlit App
  - 2-step dashboard

- Step 1: **Data Ground Truth**
  - `eval/groundtruth.py`

- Step 2: **Run Live Pipeline**
  - `eval/api.py`

- Step 3: **RAG Pipeline**
  - Guardrail + LangChain + Retrieval + Response
  - `app/main.py`
  - `app/api.py`

- Step 4: **RAG Metrics**
  - Faithfulness
  - Answer Relevancy
  - Context Precision
  - Context Recall
  - Answer Correctness
  - `RAGAS metrics`

- Step 5: **Real Hallucination**

- Evaluation / dashboard components:
  - `eval/metrics.py`
  - `eval/ui.py`
  - `eval/services/evaluation.py`
  - `eval/services/groundtruth.py`

- Evaluation outputs:
  - `eval/metrics.py`
  - `eval/api.py`
  - `eval/ui.py`

- Final Results Dashboard
  - Overall Score + Errors

- Result files:
  - `eval/metrics.py`
  - `eval/api.py`
  - `eval/ui.py`

