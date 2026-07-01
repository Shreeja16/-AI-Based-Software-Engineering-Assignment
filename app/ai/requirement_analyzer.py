def analyze_requirement(requirement: str, scenario_type: str) -> dict:
    lowered = requirement.lower()

    ambiguities = []
    if "scalable" in lowered:
        ambiguities.append("Scalability target is unspecified (RPS, latency, availability).")
    if "analytics" in lowered:
        ambiguities.append("Analytics granularity and retention policy are not specified.")
    if scenario_type == "ambiguous":
        ambiguities.append("Business domain scope is broad and needs clarification.")

    assumptions = [
        "REST APIs will be exposed via FastAPI.",
        "SQLite is used for prototype persistence; production can use Postgres.",
        "No authentication is required for MVP demo endpoints.",
    ]

    if scenario_type == "brownfield":
        assumptions.append("Backward compatibility for existing API contracts must be preserved.")

    return {
        "clarified_problem": f"Engineer a production-minded Python service for: {requirement}",
        "ambiguities": ambiguities,
        "assumptions": assumptions,
    }
