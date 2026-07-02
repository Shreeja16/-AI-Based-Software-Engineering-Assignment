from typing import Any


def _build_task(task_id: str, title: str, description: str, depends_on: list[str], prompt: str, validation: str) -> dict[str, Any]:
    return {
        "id": task_id,
        "title": title,
        "description": description,
        "depends_on": depends_on,
        "ai_assist": {
            "prompt": prompt,
            "expected_ai_output": "Draft implementation artifacts that require engineer review before acceptance.",
        },
        "engineer_validation": validation,
    }


def _base_tasks(requirement: str) -> list[dict[str, Any]]:
    is_url_shortener = "url shortener" in requirement.lower()

    tasks: list[dict[str, Any]] = [
        _build_task(
            "T1",
            "Define API Contracts",
            "Define request/response schemas and endpoint behavior including error contracts.",
            [],
            "Generate OpenAPI-aligned endpoint contracts and error responses for this requirement.",
            "Review schema correctness, naming clarity, and backward compatibility constraints.",
        ),
        _build_task(
            "T2",
            "Design Persistence",
            "Model entities and storage access patterns for required system data.",
            ["T1"],
            "Draft SQLAlchemy models and data access boundaries for required entities.",
            "Verify indexes, uniqueness, nullability, and migration impact.",
        ),
    ]

    if is_url_shortener:
        tasks.append(
            _build_task(
                "T3",
                "Implement URL Core Flows",
                "Implement URL creation, redirect, metadata retrieval, and stats endpoints.",
                ["T1", "T2"],
                "Generate handler/service code for URL creation, redirect, metadata, and stats.",
                "Manually verify behavior for successful, missing, and expired link flows.",
            )
        )
        tasks.append(
            _build_task(
                "T4",
                "Implement Analytics Capture",
                "Capture click analytics fields including timestamp, referrer, user-agent, and anonymized IP hash.",
                ["T2", "T3"],
                "Generate analytics event capture logic and privacy-aware data handling.",
                "Verify click count integrity and ensure no raw client IP is stored.",
            )
        )
        task_dependency_for_tests = ["T3", "T4"]
    else:
        tasks.append(
            _build_task(
                "T3",
                "Implement Core Requirement",
                "Implement business logic required by the requirement scope.",
                ["T1", "T2"],
                "Generate service-layer implementation for the core requirement.",
                "Validate domain behavior against requirement acceptance criteria.",
            )
        )
        task_dependency_for_tests = ["T3"]

    tasks.append(
        _build_task(
            "T5",
            "Add Tests",
            "Add unit and integration tests covering happy paths, edge cases, and regressions.",
            task_dependency_for_tests,
            "Generate pytest cases for success paths, error handling, and regressions.",
            "Run tests and confirm behavior-level assertions, not just status-code assertions.",
        )
    )
    tasks.append(
        _build_task(
            "T6",
            "Document Design and Risks",
            "Document assumptions, design trade-offs, and operational limitations.",
            ["T5"],
            "Draft architecture notes including scaling, security, and maintainability trade-offs.",
            "Confirm documentation aligns with implemented behavior and known limitations.",
        )
    )

    return tasks


def _inject_scenario_tasks(tasks: list[dict[str, Any]], scenario_type: str) -> list[dict[str, Any]]:
    if scenario_type == "brownfield":
        tasks.insert(
            0,
            _build_task(
                "T0",
                "Assess Existing System",
                "Assess existing modules and define an incremental change strategy that preserves behavior.",
                [],
                "Summarize existing architecture and identify safe extension points.",
                "Review impact radius and confirm compatibility constraints are explicit.",
            ),
        )
        for task in tasks[1:]:
            if task["id"] == "T1":
                task["depends_on"] = ["T0"]

    if scenario_type == "ambiguous":
        tasks.insert(
            0,
            _build_task(
                "TQ",
                "Clarify Ambiguities",
                "Produce clarification questions and temporary assumptions before implementation.",
                [],
                "Generate top ambiguity questions and ranked assumptions for engineering execution.",
                "Approve assumptions explicitly and track unresolved ambiguity risks.",
            ),
        )
        for task in tasks[1:]:
            if task["id"] == "T1":
                task["depends_on"] = ["TQ"]

    return tasks


def build_structured_tasks_from_text(raw_tasks: list[str], scenario_type: str) -> list[dict[str, Any]]:
    structured: list[dict[str, Any]] = []
    previous_task_id: str | None = None

    for index, raw in enumerate(raw_tasks, start=1):
        task_id = f"L{index}"
        structured.append(
            _build_task(
                task_id,
                f"LLM Task {index}",
                raw,
                [previous_task_id] if previous_task_id else [],
                f"Refine this task into implementation steps: {raw}",
                "Confirm the task output is technically correct, scoped, and testable.",
            )
        )
        previous_task_id = task_id

    if not structured:
        structured = _inject_scenario_tasks(_base_tasks(""), scenario_type)

    return structured


def decompose_tasks(requirement: str, scenario_type: str) -> list[dict[str, Any]]:
    tasks = _base_tasks(requirement)
    return _inject_scenario_tasks(tasks, scenario_type)