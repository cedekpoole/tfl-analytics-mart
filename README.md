# TfL Analytics Mart

An end-to-end data pipeline that ingests live Transport for London data, stores it in Azure Blob Storage, models it in BigQuery with dbt, and orchestrates everything via GitHub Actions.

---

## Architecture

```
TfL Unified API
      │
      ▼
Python ingestion script
      │  fetches live tube line status
      ▼
Azure Blob Storage
      │  raw JSON, partitioned by date
      ▼
BigQuery (raw dataset)
      │  loaded from Blob via external table or load job
      ▼
dbt (transform layer)
      │  staging → intermediate → marts
      ▼
Analytics-ready tables
```

---

## Stack

| Layer | Tool |
|---|---|
| Ingestion | Python + `requests` |
| Raw storage | Azure Blob Storage |
| Data warehouse | Google BigQuery |
| Transformation | dbt Core |
| Orchestration | GitHub Actions |

---

## Data source

[TfL Unified API](https://api.tfl.gov.uk) — public REST API providing real-time and static data across all TfL modes. No API key required for up to 50 requests per minute.

Endpoint used: `GET /Line/Mode/tube/Status`

Returns the current service status for every London Underground line (e.g. Good Service, Minor Delays, Part Suspended).

---

## Project structure

```
fetch_tfl.py   # ingestion script — calls TfL API, prints line statuses
README.md
```

> This project is being built incrementally. The structure will expand as each layer is added.

---

## Running the ingestion script

**Requirements:** Python 3.8+

```bash
pip install requests
python fetch_tfl.py
```

**Example output:**

```
Bakerloo: Good Service
Central: Good Service
Circle: Minor Delays
...
```
