from typing import Literal

from pydantic import BaseModel


class EngineeringRunRequest(BaseModel):
    requirement: str
    scenario_type: Literal["greenfield", "brownfield", "ambiguous"]


class EngineeringRunResponse(BaseModel):
    clarified_problem: str
    ambiguities: list[str]
    assumptions: list[str]
    tasks: list[str]
    artifacts: dict[str, str | list[str]]
    validation: dict[str, list[str]]
