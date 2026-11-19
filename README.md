# UdyamGuide

**UdyamGuide** is an AI-powered assistant that helps micro and small enterprises discover government schemes, collateral-free loans, and protection against delayed payments using verified government documents and citations.

**Status:** Day 1 – Foundation (FastAPI skeleton, project structure, and quality gates). Live deployment planned from Day 5.

## Who It's For

An owner of a small engineering job-work unit in Ambattur Industrial Estate, Chennai, with Udyam registration and unpaid buyer invoices.

## The Problem

Micro and small enterprise owners often struggle to understand:

- Government schemes such as CGTMSE, PMEGP, and ZED.
- Eligibility conditions and documentation requirements.
- Collateral-free business loan opportunities.
- Their legal rights regarding delayed payments under the MSMED Act, 2006.

Different schemes have different eligibility criteria, making it difficult for business owners to identify the benefits available to them.

## Data Sources

UdyamGuide uses official government documents and guidelines as its knowledge sources.

- MSME Ministry scheme guidelines
- MSMED Act, 2006
- Udyam Registration FAQs
- CGTMSE guidelines
- MSME Samadhaan documents
- Tamil Nadu MSME scheme documents

**Official Sources:**

- [Ministry of MSME](https://msme.gov.in/)
- [Udyam Registration](https://udyamregistration.gov.in/)
- [CGTMSE](https://www.cgtmse.in/)

All scheme-related answers should cite the relevant source document and its publication or revision date.

##  Hardest Technical Challenge

**Enterprise classification and delayed-payment interest calculation.**

- Enterprise classification depends on investment and turnover thresholds, including the revised limits introduced in 2025.
- Delayed-payment interest under the MSMED Act requires implementing the statutory calculation correctly.
- The interest calculation involves monthly compounding at three times the RBI bank rate, as specified under the Act.

##  Signature Feature: Delayed Payment Calculator

Users can enter:

1. Invoice date
2. Invoice amount
3. Payment date

The calculator determines the delayed-payment interest due and provides the relevant statutory section as a reference.

## Target Metrics

- Interest calculation accuracy: 20 out of 20 test invoices.
- Scheme eligibility accuracy: 90% or higher across 30 test profiles.

##  Tech Stack

- **Language:** Python
- **Backend:** FastAPI
- **Package Management:** uv
- **Testing:** pytest
- **Code Quality:** Ruff
- **API Documentation:** Swagger UI

##  Run Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd prince28-fin09-udyamguide
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

```powershell
copy .env.example .env
```

### 4. Start the FastAPI server

```bash
uv run uvicorn udyamguide.api.main:create_app --factory --reload
```

### 5. Open API documentation

Visit:

http://localhost:8000/docs

##  Quality Checks

Run tests:

```bash
uv run pytest
```

Run lint checks:

```bash
uv run ruff check .
```

---
## Run locally in one command

You need Docker Desktop running. From a fresh clone:

```bash
docker compose up --build
```

This starts Postgres (with pgvector), Redis, runs the migrations and loads the sample data once, then starts the API.

- API docs: http://localhost:8000/docs
- Liveness: http://localhost:8000/health
- Readiness (checks the database): http://localhost:8000/ready

Stop with `Ctrl+C`, then `docker compose down`. Add `-v` to also delete the database volume.

## Develop and test

| Task | Mac / Linux | Windows |
|---|---|---|
| Run the API with reload | `make dev` | `uv run poe dev` |
| Unit tests (no network) | `make test` | `uv run poe test` |
| Integration tests (needs `docker compose up`) | `make test-integration` | `uv run poe test-integration` |
| Coverage report | `make cov` | `uv run poe cov` |
| Lint and format check | `make lint` | `uv run poe lint` |


**UdyamGuide – Making MSME government benefits and legal protections easier to understand and access.**
