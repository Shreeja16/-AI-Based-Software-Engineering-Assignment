from typing import Any


def _build_task_summary(tasks: list[dict[str, Any]]) -> str:
    return " | ".join(f"{task['id']}: {task['title']}" for task in tasks)


def generate_artifacts(requirement: str, scenario_type: str, tasks: list[dict[str, Any]]) -> dict:
    requirement_lower = requirement.lower()
    is_url_shortener = "url shortener" in requirement_lower

    if is_url_shortener:
        api_contract = (
            "POST /links, GET /{short_code}, GET /links/{short_code}, "
            "GET /links/{short_code}/stats, POST /engineering/run"
        )
        test_plan = [
            "Validate link creation with valid/invalid URLs.",
            "Validate redirect flow and click counter increments.",
            "Validate stats endpoint reflects click totals.",
            "Validate expired link handling returns HTTP 410.",
            "Validate engineering pipeline response structure.",
        ]
    else:
        api_contract = "Define domain-specific APIs for the provided requirement plus POST /engineering/run"
        test_plan = [
            "Validate primary business workflow happy paths.",
            "Validate key failure and edge cases.",
            "Validate API contract correctness and schema errors.",
            "Validate regression safety for existing behavior.",
            "Validate engineering pipeline response structure.",
        ]

    if scenario_type == "brownfield":
        test_plan.append("Add regression tests for unchanged legacy behavior.")
    if scenario_type == "ambiguous":
        test_plan.append("Validate ambiguity extraction and clarification questions.")

    documentation = (
        "This prototype demonstrates AI-assisted requirement interpretation, task decomposition, "
        "artifact generation, and validation while preserving engineer ownership of outputs."
    )

    generated_outputs = [
        "Code implementation updates in API, service, and persistence layers",
        "API contract definitions using FastAPI/Pydantic schemas",
        "Pytest integration tests for health, redirect behavior, expiry handling, and engineering pipeline",
        "Architecture, demo, and submission documentation",
    ]

    ai_execution_notes = [
        "Each task defines a bounded AI prompt and expected output.",
        "Engineer validates correctness before accepting generated outputs.",
        "Validation stage records quality checks and risks before final acceptance.",
    ]

    return {
        "api_contract": api_contract,
        "task_summary": _build_task_summary(tasks),
        "test_plan": test_plan,
        "documentation": documentation,
        "generated_outputs": generated_outputs,
        "ai_execution_notes": ai_execution_notes,
        "requirement": requirement,
    }
