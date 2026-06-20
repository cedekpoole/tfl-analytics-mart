# TfL Analytics Mart

An end-to-end data pipeline built on public TfL data.

**Current status: local ingestion only.** The pipeline fetches live tube line statuses from the TfL API and saves them as JSON files locally. Azure, BigQuery, and dbt layers are planned but not yet built.

---

## What it does (right now)

`fetch_tfl.py` calls the [TfL Unified API](https://api.tfl.gov.uk) endpoint for London Underground line statuses, then saves the response as a timestamped JSON file:

```
data/raw/tfl/tfl_lines_2026-06-20_14-30-00.json
```

Each run creates a new file. The `data/raw/tfl/` folder is gitignored so raw files are never committed.

---

## Setup

Requires Python 3.8+.

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python fetch_tfl.py
```

**Example output:**

```
Saved 11 lines to data/raw/tfl/tfl_lines_2026-06-20_14-30-00.json
```

---

## Planned architecture

The following layers are not yet built.

```
TfL Unified API
      │
      ▼
Python ingestion script        ← built
      │
      ▼
Azure Blob Storage             ← planned
      │
      ▼
BigQuery                       ← planned
      │
      ▼
dbt (staging → marts)          ← planned
      │
      ▼
GitHub Actions (orchestration) ← planned
```

---

## Stack

| Layer | Tool | Status |
|---|---|---|
| Ingestion | Python + `requests` | Done |
| Raw storage | Azure Blob Storage | Planned |
| Data warehouse | Google BigQuery | Planned |
| Transformation | dbt Core | Planned |
| Orchestration | GitHub Actions | Planned |
