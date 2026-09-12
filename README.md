# NFL Data Pipeline

A data engineering project that ingests NFL player statistics from a public data source and loads it into PostgreSQL, built as a hands-on portfolio project while transitioning into data engineering.

## What it does

- Pulls weekly NFL player statistics for the 2021-2025 seasons using [`nflreadpy`](https://github.com/nflverse/nflreadpy), a Python interface to the [nflverse](https://github.com/nflverse) public data project
- Loads the data into a PostgreSQL database (`raw` schema) using SQLAlchemy
- Keeps a local CSV backup of each pull as a safety net

## Architecture (current)

```
nflreadpy (source)
      │
      ▼
pipeline_nfl_playerstats.py   (fetch + orchestrate)
      │
      ├──► raw_backup.csv      (local backup, not tracked in git)
      │
      ▼
db_utils.py  (load_to_postgres)
      │
      ▼
PostgreSQL: raw.weekly_player_stats
```

## Tech stack

- **Python** — pandas, Polars (via `nflreadpy`), SQLAlchemy, psycopg2
- **PostgreSQL** — target data warehouse
- **python-dotenv** — environment-based credential management (no hardcoded secrets)

## Setup

1. Clone the repo
2. Create a virtual environment and install dependencies:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root (not tracked in git) with your database credentials:
   ```
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=nfl_pipeline
   ```
4. Create the target database and schema in PostgreSQL:
   ```sql
   CREATE DATABASE nfl_pipeline;
   CREATE SCHEMA raw;
   ```
5. Run the pipeline:
   ```
   python3 pipeline_nfl_playerstats.py
   ```

## Project status

This is an active work in progress, built incrementally as I learn. Current state:

- [x] Raw ingestion: pull player stats from `nflreadpy`, load into PostgreSQL
- [x] Environment-based credential management
- [ ] Incremental/idempotent loading (currently uses append; will move to delete-and-replace by season/week, then to upsert)
- [ ] Dagster orchestration (asset-based pipeline with scheduling)
- [ ] Staging layer (data cleaning, type standardization, team abbreviation normalization)
- [ ] Mart layer (analytical tables — team efficiency, QB performance splits)
- [ ] Data quality checks (Dagster asset checks)
- [ ] Additional source tables (schedules, rosters) joined against player stats
- [ ] Unit tests on transformation logic

## What I'd do differently at scale

This is a personal-scale project running against a local database. In a production context, I'd move to a proper orchestrator running on managed infrastructure, partition raw data by season rather than loading it as a single table, use dbt for the transformation layer instead of raw SQL/pandas, and add monitoring/alerting on pipeline failures rather than relying on manual runs.

## Why this project

I'm an application analyst with 8 years in healthcare IT (EHR systems, charge/billing data, SQL-based reporting) transitioning into data engineering. This project is where I'm building hands-on pipeline experience — ingestion, transformation, orchestration, and infrastructure — beyond what my day job covers.
