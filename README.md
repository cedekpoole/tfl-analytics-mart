# TfL Analytics Mart

An evolving data pipeline built on public TfL data.

**Current status: ingestion and raw cloud loading.** The project fetches live
Tube line statuses from the TfL API, validates the response, saves a timestamped
JSON snapshot locally, uploads the same file to a private Azure Blob Storage
container and appends the snapshot to a raw BigQuery table.

dbt has been initialised and connected to BigQuery, but TfL transformation
models have not been built yet. Automated orchestration is still planned.

---

## What it does

`fetch_tfl.py` calls the [TfL Unified API](https://api.tfl.gov.uk) endpoint for
London Underground line statuses. It:

1. Fetches the current status of each Tube line.
2. Validates that the response contains the required fields.
3. Prints a readable status summary to the terminal.
4. Saves a timestamped JSON snapshot locally.
5. Uploads that snapshot to the private `raw-tfl` Azure Blob container.
6. Appends the same snapshot to the raw BigQuery table.

Local files are saved using this structure:

```text
data/raw/tfl/tfl_lines_2026-06-20_14-30-00.json
```

Each run creates a new timestamped file. Raw JSON files under
`data/raw/tfl/` are gitignored and are not committed to the repository.

The saved JSON file contains one JSON object followed by a newline:

```json
{
  "utc_fetched_at": "2026-06-20T14:30:00+00:00",
  "source_url": "https://api.tfl.gov.uk/Line/Mode/tube/Status",
  "data": []
}
```

The `data` field contains the full TfL API response. The metadata fields make
it clear when the file was fetched and which source endpoint produced it.

The BigQuery raw table is:

```text
tfl-analytics-mart.raw_tfl.line-status-snapshots
```

Each script run appends one row to this table. One row represents one API
snapshot; the nested `data` column contains the Tube line status payload for
that fetch.

The script does not save, upload, or load a file if the API response is empty
or missing the required line-status fields.

The current tests use fake data and do not call the real TfL API.

---

## Setup

Create and activate a local Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

### Azure Authentication

The Azure upload uses passwordless authentication through the Azure CLI rather
than storing an account key in the project.

Install the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
and sign in:

```bash
az login
```

The signed-in Azure user must have the **Storage Blob Data Contributor** role
for the storage account.

### Google Cloud Authentication

The BigQuery load uses local Google Application Default Credentials rather than
storing a service account key in the project.

Install the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install), then
sign in for local application credentials:

```bash
gcloud auth application-default login
```

The signed-in Google user must have permission to append rows to the raw
BigQuery table.

The script expects this raw BigQuery table to already exist in the London
region:

```text
tfl-analytics-mart.raw_tfl.line-status-snapshots
```

Current schema:

| Column           | Type      |
| ---------------- | --------- |
| `utc_fetched_at` | TIMESTAMP |
| `source_url`     | STRING    |
| `data`           | JSON      |

---

## Run

```bash
python fetch_tfl.py
```

By default, files are saved under `data/raw/tfl/`. You can choose a different
output folder with:

```bash
python fetch_tfl.py --output-dir data/raw/tfl
```

**Example output:**

```text
Bakerloo : Good Service
Central : Good Service
Northern : Minor Delays
Saved 11 lines to data/raw/tfl/tfl_lines_2026-06-20_14-30-00.json
Uploaded tfl_lines_2026-06-20_14-30-00.json to Azure Blob Storage
Loaded 1 row into BigQuery
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
API, upload files to Azure, or load data into BigQuery.

---

## Architecture

The ingestion and raw-loading layers are implemented. dbt setup has started,
but transformation models are still planned.

```text
TfL Unified API
      |
      v
Python ingestion script        <- built
      |
      +-- local raw JSON        <- built
      +-- Azure Blob Storage    <- built
      +-- BigQuery raw table    <- built
              |
              v
dbt staging and marts          <- setup started, models planned
      |
      v
GitHub Actions orchestration   <- planned
```

### Why Azure and BigQuery?

Azure Blob Storage is used as a raw file archive. It keeps timestamped copies
of the original API response so the project has a durable record of what was
fetched before any transformation happens.

BigQuery is used as the analytical warehouse. It stores the raw snapshots in a
queryable table so SQL and dbt can turn the nested JSON into cleaner
analysis-ready models.

In this project, Azure is the raw storage layer and BigQuery is the warehouse
layer. They serve different purposes.

---

## Stack

| Layer          | Tool                    | Status                            |
| -------------- | ----------------------- | --------------------------------- |
| Ingestion      | Python + `requests`     | Done                              |
| Testing        | pytest                  | Done for current local functions  |
| Raw storage    | Azure Blob Storage      | Done                              |
| Data warehouse | Google BigQuery         | Done for raw snapshot loading     |
| Transformation | dbt Core + dbt-bigquery | Setup started; TfL models planned |
| Orchestration  | GitHub Actions          | Planned                           |
