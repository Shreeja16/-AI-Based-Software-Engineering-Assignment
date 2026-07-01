def validate_output(artifacts: dict) -> dict[str, list[str]]:
    checks = []
    risks = []

    required_keys = ["api_contract", "test_plan", "documentation"]
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

    risks.extend(
        [
            "AI-generated tasks can miss hidden constraints unless manually reviewed.",
            "Performance and abuse protection controls are not production-complete in this prototype.",
        ]
    )

    return {"checks": checks, "risks": risks}
