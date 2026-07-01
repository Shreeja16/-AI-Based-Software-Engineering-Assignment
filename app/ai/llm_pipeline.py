import json
import os
from typing import Any

import httpx


OLLAMA_API_URL = "http://localhost:11434/api/chat"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


SYSTEM_PROMPT = """
You are a senior software engineer assistant.
Given a requirement and scenario type, produce a strict JSON object with this exact shape:
{
  "clarified_problem": "string",
  "ambiguities": ["string"],
  "assumptions": ["string"],
  "tasks": ["string"],
  "artifacts": {
    "api_contract": "string",
    "task_summary": "string",
    "test_plan": ["string"],
    "documentation": "string",
    "requirement": "string"
  }
}
Rules:
- Return ONLY valid JSON.
- Make tasks and tests specific to the provided requirement domain.
- For ambiguous scenarios, include clarification-focused ambiguities and assumptions.
- For brownfield scenarios, include compatibility/regression tasks.
""".strip()


def _sanitize_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            result.append(item.strip())
    return result


def _is_valid_payload(data: dict[str, Any]) -> bool:
    required_top = {"clarified_problem", "ambiguities", "assumptions", "tasks", "artifacts"}
    if not required_top.issubset(set(data.keys())):
        return False
    if not isinstance(data.get("clarified_problem"), str):
        return False
    if not isinstance(data.get("artifacts"), dict):
        return False
    return True


def _try_ollama(requirement: str, scenario_type: str) -> dict[str, Any] | None:
    """Try to generate using local Ollama instance."""
    model = os.getenv("OLLAMA_MODEL", "mistral")
    user_prompt = (
        f"Requirement:\n{requirement}\n\n"
        f"Scenario Type: {scenario_type}\n\n"
        "Return JSON only."
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "format": "json",
    }

    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        
        # Ollama returns response in a slightly different format
        result = response.json()
        if "message" in result and "content" in result["message"]:
            content = result["message"]["content"]
        else:
            return None
            
        data = json.loads(content)

        if not isinstance(data, dict) or not _is_valid_payload(data):
            return None

        # Normalize list fields
        data["ambiguities"] = _sanitize_string_list(data.get("ambiguities"))
        data["assumptions"] = _sanitize_string_list(data.get("assumptions"))
        data["tasks"] = _sanitize_string_list(data.get("tasks"))

        artifacts = data.get("artifacts", {})
        if not isinstance(artifacts, dict):
            artifacts = {}

        test_plan = _sanitize_string_list(artifacts.get("test_plan"))
        artifacts["test_plan"] = test_plan
        artifacts.setdefault("requirement", requirement)
        artifacts.setdefault("documentation", "AI-generated draft. Review before acceptance.")
        artifacts.setdefault("task_summary", " | ".join(data["tasks"]))
        artifacts.setdefault("api_contract", "Domain-specific API contract to be finalized by engineer.")
        artifacts["provider"] = "ollama"

        data["artifacts"] = artifacts
        return data
    except Exception:
        return None


def _try_openai(requirement: str, scenario_type: str) -> dict[str, Any] | None:
    """Try to generate using OpenAI API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    user_prompt = (
        f"Requirement:\n{requirement}\n\n"
        f"Scenario Type: {scenario_type}\n\n"
        "Return JSON only."
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    }

    try:
        with httpx.Client(timeout=25.0) as client:
            response = client.post(OPENAI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        data = json.loads(content)

        if not isinstance(data, dict) or not _is_valid_payload(data):
            return None

        # Normalize list fields to keep response model-safe.
        data["ambiguities"] = _sanitize_string_list(data.get("ambiguities"))
        data["assumptions"] = _sanitize_string_list(data.get("assumptions"))
        data["tasks"] = _sanitize_string_list(data.get("tasks"))

        artifacts = data.get("artifacts", {})
        if not isinstance(artifacts, dict):
            artifacts = {}

        test_plan = _sanitize_string_list(artifacts.get("test_plan"))
        artifacts["test_plan"] = test_plan
        artifacts.setdefault("requirement", requirement)
        artifacts.setdefault("documentation", "AI-generated draft. Review before acceptance.")
        artifacts.setdefault("task_summary", " | ".join(data["tasks"]))
        artifacts.setdefault("api_contract", "Domain-specific API contract to be finalized by engineer.")
        artifacts["provider"] = "openai"

        data["artifacts"] = artifacts
        return data
    except Exception:
        return None


def generate_with_llm(requirement: str, scenario_type: str) -> dict[str, Any] | None:
    """
    Generate artifacts using LLM with fallback chain:
    1. Try local Ollama (free, fast, runs locally)
    2. Try OpenAI API (if OPENAI_API_KEY is set)
    3. Return None (triggers rule-based fallback)
    """
    # Try Ollama first (free local option)
    result = _try_ollama(requirement, scenario_type)
    if result is not None:
        return result
    
    # Fall back to OpenAI
    result = _try_openai(requirement, scenario_type)
    if result is not None:
        return result
    
    # If both fail, return None (triggers rule-based fallback in routes.py)
    return None
