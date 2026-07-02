def validate_output(artifacts: dict, tasks: list[dict] | None = None) -> dict[str, list[str]]:
    checks = []
    risks = []

    required_keys = ["api_contract", "test_plan", "documentation", "task_summary"]
    missing = [key for key in required_keys if key not in artifacts]
    if missing:
        checks.append(f"Missing required artifacts: {', '.join(missing)}")
    else:
        checks.append("All core artifact sections are present.")

    test_plan = artifacts.get("test_plan", [])
    if len(test_plan) < 4:
        risks.append("Test plan may be insufficient for broad behavioral coverage.")
    else:
        checks.append("Test plan includes multiple functional and edge-path validations.")

    ai_notes = artifacts.get("ai_execution_notes", [])
    if isinstance(ai_notes, list) and len(ai_notes) >= 2:
        checks.append("AI-assisted execution notes are present for engineer review traceability.")
    else:
        risks.append("AI-assisted execution traceability is weak; add notes on prompt and review decisions.")

    if tasks:
        invalid_dependency = False
        seen_ids = {task.get("id") for task in tasks}
        for task in tasks:
            for dependency in task.get("depends_on", []):
                if dependency not in seen_ids:
                    invalid_dependency = True
        if invalid_dependency:
            risks.append("At least one task dependency is invalid.")
        else:
            checks.append("Task dependency graph is internally consistent.")

    risks.extend(
        [
            "AI-generated tasks can miss hidden constraints unless manually reviewed.",
            "Performance and abuse protection controls are not production-complete in this prototype.",
        ]
    )

    return {"checks": checks, "risks": risks}