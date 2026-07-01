def decompose_tasks(requirement: str, scenario_type: str) -> list[str]:
    common = [
        "Define API contracts and validation schemas.",
        "Implement persistence models and repository/service boundaries.",
        "Implement business logic for core requirement.",
        "Add unit and integration tests for happy paths and edge cases.",
        "Add engineering documentation, assumptions, and trade-offs.",
    ]

    if "url shortener" in requirement.lower():
        common.insert(2, "Implement URL creation, redirect, metadata, and stats endpoints.")
        common.insert(3, "Capture click analytics (timestamp, referrer, user-agent, anonymized IP).")

    if scenario_type == "brownfield":
        common.insert(0, "Assess existing modules and plan safe incremental changes.")
        common.append("Run regression checks to prevent behavior breaks.")

    if scenario_type == "ambiguous":
        common.insert(0, "Generate clarification questions and temporary assumptions before coding.")

    return common
