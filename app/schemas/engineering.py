from typing import Literal

from pydantic import BaseModel

class AIAssist(BaseModel):
    prompt: str
    expected_ai_output: str


class EngineeringRunRequest(BaseModel):
    requirement: str
    scenario_type: Literal["greenfield", "brownfield", "ambiguous"]


class EngineeringTask(BaseModel):
    id: str
    title: str
    description: str
    depends_on: list[str]
    ai_assist: AIAssist
    engineer_validation: str


class EngineeringRunResponse(BaseModel):
    clarified_problem: str
    ambiguities: list[str]
    assumptions: list[str]
    tasks: list[EngineeringTask]
    artifacts: dict[str, str | list[str]]
    validation: dict[str, list[str]]