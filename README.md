# TfL Analytics Mart

An end-to-end data pipeline built on public TfL data.

**Current status: local ingestion only.** The project currently fetches live tube line statuses from the TfL API, prints a readable status summary, saves the response locally with basic metadata, and includes simple pytest coverage for the local functions. Azure, BigQuery, and dbt layers are planned but not yet built.

---

## What it does (right now)

`fetch_tfl.py` calls the [TfL Unified API](https://api.tfl.gov.uk) endpoint for London Underground line statuses. It checks that the API returned line status data, prints each tube line's current status to the terminal, then saves a timestamped JSON file locally:

```
data/raw/tfl/tfl_lines_2026-06-20_14-30-00.json
```

Each run creates a new file. The `data/raw/tfl/` folder is gitignored so raw JSON files are not committed.

The saved JSON file contains:

```json
{
  "utc_fetched_at": "2026-06-20_14-30-00",
  "source_url": "https://api.tfl.gov.uk/Line/Mode/tube/Status",
  "data": []
}
```

The `data` field contains the full TfL API response. The metadata fields make it clear when the file was fetched and which source endpoint produced it.

The current tests use fake data and do not call the real TfL API.

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

By default, files are saved under `data/raw/tfl/`. You can choose a different output folder with:

```bash
python fetch_tfl.py --output-dir data/raw/tfl
```

**Example output:**

```
Bakerloo : Good Service
Central : Good Service
Northern : Minor Delays
Saved 11 lines to data/raw/tfl/tfl_lines_2026-06-20_14-30-00.json
```

---

## Tests

Run the current test suite with:

```bash
python -m pytest tests/ -v
```

The tests in `tests/test_fetch_tfl.py` check local behavior only: saving JSON with metadata, printing readable line statuses, and rejecting an empty API response using fake TfL-style data.

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
| Testing | pytest | Started |
| Raw storage | Azure Blob Storage | Planned |
| Data warehouse | Google BigQuery | Planned |
| Transformation | dbt Core | Planned |
| Orchestration | GitHub Actions | Planned |
