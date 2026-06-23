# TfL Analytics Mart

An evolving data pipeline built on public TfL data.

**Current status: ingestion and raw cloud storage.** The project fetches live
tube line statuses from the TfL API, validates the response, saves a timestamped
JSON snapshot locally, and uploads the same file to a private Azure Blob Storage
container. BigQuery, dbt, and automated orchestration are planned but not yet
built.

---

## What it does

`fetch_tfl.py` calls the [TfL Unified API](https://api.tfl.gov.uk) endpoint for
London Underground line statuses. It:

1. Fetches the current status of each Tube line.
2. Validates that the response contains the required fields.
3. Prints a readable status summary to the terminal.
4. Saves a timestamped JSON snapshot locally.
5. Uploads that snapshot to the private `raw-tfl` Azure Blob container.

Local files are saved using this structure:

```
data/raw/tfl/tfl_lines_2026-06-20_14-30-00.json
```

Each run creates a new timestamped file. Raw JSON files under
`data/raw/tfl/` are gitignored and are not committed to the repository.

The saved JSON file contains:

```json
{
  "utc_fetched_at": "2026-06-20_14-30-00",
  "source_url": "https://api.tfl.gov.uk/Line/Mode/tube/Status",
  "data": []
}
```

The `data` field contains the full TfL API response. The metadata fields make it clear when the file was fetched and which source endpoint produced it.

The script does not save or upload a file if the API response is empty or
missing the required line-status fields.

The current tests use fake data and do not call the real TfL API.

---

## Setup

Requires Python 3.8+.

```bash
python -m pip install -r requirements.txt
```

The Azure upload uses passwordless authentication through the Azure CLI rather
than storing an account key in the project.

Install the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
and sign in:

```bash
az login
```

The signed-in Azure user must have the **Storage Blob Data Contributor** role
for the storage account.

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
Uploaded tfl_lines_2026-06-20_14-30-00.json to Azure Blob Storage
```

---

## Tests

Run the current test suite with:

```bash
python -m pytest -v
```

Pytest automatically discovers test files under `tests/`. The tests use fake
data and check local behavior only: saving JSON with metadata, printing readable
line statuses, and rejecting invalid TfL-style data. They do not call the TfL
API or upload files to Azure.

---

## Architecture

The ingestion and raw-storage layers are implemented. The remaining layers are
planned.

```
TfL Unified API
      │
      ▼
Python ingestion script        ← built
      │
      ▼
Azure Blob Storage             ← built
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
| Testing | pytest | Done for current local functions |
| Raw storage | Azure Blob Storage | Done |
| Data warehouse | Google BigQuery | Planned |
| Transformation | dbt Core | Planned |
| Orchestration | GitHub Actions | Planned |
