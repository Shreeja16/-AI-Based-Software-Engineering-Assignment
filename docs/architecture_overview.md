# Architecture Overview

## Objective
This prototype demonstrates engineer-led, AI-assisted software engineering. It accepts a requirement, decomposes implementation tasks, generates engineering artifacts, and validates output quality.

## Components
- API Layer (FastAPI): request handling and response contracts
- URL Shortener Service: create links, redirects, metadata, analytics
- Persistence Layer (SQLAlchemy + SQLite): stores links and click events
- AI Assistance Layer:
  - Requirement Analyzer
  - Task Decomposer (structured tasks with dependencies)
  - Artifact Generator
  - Validation Checker

## Engineering Task Model
Each requirement is transformed into structured tasks with:
- Task id and objective
- Explicit dependency list (`depends_on`)
- Task-level AI assist prompt and expected AI output
- Engineer validation criteria before acceptance

This enforces engineer-led sequencing and avoids opaque autonomous generation.

## AI Integration Model
AI assists execution within bounded tasks. Engineering logic, quality checks, and final acceptance remain under engineer ownership.

## Trade-offs
- SQLite selected for demo speed; production should use Postgres.
- In-memory sync analytics writes are sufficient for prototype; production should use queued async ingestion.
- No auth/rate limiting in MVP; identified as known risks and future work.

## Validation Strategy
- Unit and API integration tests via pytest and FastAPI TestClient
- Output schema validation with Pydantic
- Structured validation checks for generated engineering artifacts and task dependency consistency
- Manual review requirement for AI-generated outputs

## Scenario Evidence
Submission includes example input and output artifacts for:
- Greenfield scenario
- Brownfield scenario
- Ambiguous scenario

Each output includes task breakdown, AI-assisted execution metadata, and validation results.