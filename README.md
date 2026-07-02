# AI-Assisted Software Engineering Assignment Prototype

This repository provides a runnable Python prototype for the assignment. It demonstrates:
- A working URL shortener (mandatory use case)
- Requirement-to-engineering-output pipeline
- Greenfield, brownfield, and ambiguous scenario handling
- Structured task decomposition with explicit sequence/dependencies
- Validation and testing discipline for AI-assisted outputs

## Tech Stack
- FastAPI
- SQLAlchemy
- SQLite
- Pytest

## Project Structure
- app/main.py: app bootstrap
- app/api/routes.py: API routes
- app/services/url_shortener.py: URL shortener business logic
- app/ai/: requirement analysis, decomposition, artifact generation, validation
- tests/test_app.py: integration tests
- examples/: scenario payloads and sample pipeline outputs
- docs/architecture_overview.md: architecture summary

## Setup
1. Create virtual environment:
   - Windows PowerShell: python -m venv .venv
2. Activate environment:
   - Windows PowerShell: .\\.venv\\Scripts\\Activate.ps1
3. Install dependencies:
   - pip install -r requirements.txt

## Run
- uvicorn app.main:app --reload

## Enable Real AI Mode (Optional)
By default, the pipeline works in fallback mode (rule-based) if no LLM is available.
To enable real LLM-backed generation for `/engineering/run`:

### Option 1: Local Ollama (Free, Recommended)
1. Download and install Ollama from [https://ollama.ai](https://ollama.ai)
2. Start Ollama (runs on http://localhost:11434 by default)
3. In PowerShell, pull a model:
   - `ollama run qwen2.5-coder:3b` (or other model)
4. Keep Ollama running, then in a new PowerShell tab:
   - `uvicorn app.main:app --reload`
5. Server will auto-detect Ollama and use it for generation.

Optional: Override model name:
   - PowerShell: `$env:OLLAMA_MODEL="qwen2.5-coder:3b"`

### Option 2: OpenAI API (Paid, ~$0.01-0.05 per call)
1. Get API key from [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. In PowerShell:
   - `$env:OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxx"`
3. Optional model override:
   - `$env:OPENAI_MODEL="gpt-4o-mini"`
4. Restart server.

### Fallback Behavior
Response will include `artifacts.generation_mode`:
- `ollama` when local Ollama is used
- `openai` when OpenAI API is used
- `fallback` when no LLM is available (rule-based generation)

Open docs at:
- http://127.0.0.1:8000/docs

Note on redirect endpoint:
- `GET /{short_code}` returns a `307` redirect. In Swagger UI, this may show `Failed to fetch` due to browser CORS behavior on redirected target domains.
- Validate redirect behavior with terminal curl:
   - `curl -i http://127.0.0.1:8000/<short_code>`

## Mandatory Use Case Flow
1. Create short URL:
   - POST /links
2. Redirect via code:
   - GET /{short_code}
3. Retrieve metadata:
   - GET /links/{short_code}
4. Retrieve analytics:
   - GET /links/{short_code}/stats

## Engineering Pipeline Flow
- POST /engineering/run with:
  - requirement
  - scenario_type (greenfield | brownfield | ambiguous)

The endpoint returns:
- clarified problem statement
- ambiguities
- assumptions
- decomposed tasks with dependencies and AI-assist prompts
- generated artifacts
- validation checks and risks

Sample output artifacts are included for quick reviewer access:
- examples/greenfield_output.json
- examples/greenfield_output_ollama.json
- examples/brownfield_output.json
- examples/brownfield_output_ollama.json
- examples/ambiguous_output.json
- examples/ambiguous_output_ollama.json

## Run Tests
- pytest -q

## Demo Script
- See `docs/demo_script.md` for a 5-minute walkthrough.

## Submission Checklist
- See `docs/submission_checklist.md` for final handoff steps.

## Publish To Public GitHub
1. Create a new public repository on GitHub (without initializing README).
2. Run the following commands from project root:
   - `git init`
   - `git add .`
   - `git commit -m "Initial submission: AI-assisted software engineering prototype"`
   - `git branch -M main`
   - `git remote add origin <YOUR_PUBLIC_GITHUB_REPO_URL>`
   - `git push -u origin main`
3. Copy and share the public repository URL with the hiring team.

## Assignment Coverage Mapping
1. Requirement Understanding: app/ai/requirement_analyzer.py
2. Task Decomposition: app/ai/task_decomposer.py
3. AI-Assisted Development: app/ai/llm_pipeline.py + per-task AI assist metadata in task_decomposer.py
4. Engineering Output Generation: /engineering/run response artifacts + URL shortener implementation + examples/*_output.json
5. Validation and QA: app/ai/validator.py + tests/test_app.py + scenario output evidence
6. Risk Awareness: validation risk output + architecture trade-offs
7. Final Engineering Output: README + docs/architecture_overview.md + examples

## Known Limitations
- No authentication/authorization
- No rate limiting
- No distributed caching
- SQLite not suitable for high-scale production traffic

These are intentionally documented to demonstrate engineering trade-off awareness.
