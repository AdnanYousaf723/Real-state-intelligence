# RELI — Real Estate Lead Intelligence

An automated real-estate data pipeline that transforms messy property records into explainable, ranked leads.

CSV/API → Validation → Normalization → Deduplication → Enrichment → Signals → Scoring → PostgreSQL → FastAPI → Dashboard

## Architecture
The system follows a strict pipeline pattern to ensure data quality and integrity before scoring leads.

### Core Modules
1. **Ingestion (`src/reli/ingestion`)**: Adapters for ATTOM API and local CSV parsing.
2. **Pipeline (`src/reli/pipeline`)**: Core runner coordinating validation, normalisation, and deduplication.
3. **Signals & Scoring (`src/reli/scoring`)**: Rules engine translating facts into confidence-weighted signals.
4. **Database (`src/reli/database`)**: SQLAlchemy + PostgreSQL schema for durable canonical records.
5. **API (`src/reli/api`)**: FastAPI backend serving structured insights.
6. **Dashboard (`src/pages`)**: Next.js/React internal tooling for lead visualization.

## Getting Started

### Local Development (Python)
1. Install requirements:
   ```bash
   pip install -e .
   ```
2. Initialize DB:
   ```bash
   reli init-db
   ```
3. Run the pipeline:
   ```bash
   reli pipeline-run --source sample_csv
   ```
4. Run the API:
   ```bash
   uvicorn reli.api.main:app --reload
   ```

### UI Development (React)
1. Install node modules:
   ```bash
   npm install
   ```
2. Start dev server:
   ```bash
   npm run dev
   ```

## CI/CD
GitHub Actions are configured in `.github/workflows` to run Pytest suites on every pull request and to run the data pipeline on a nightly cron schedule.
