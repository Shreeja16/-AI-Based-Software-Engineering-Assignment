from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.ai.artifact_generator import generate_artifacts
from app.ai.llm_pipeline import generate_with_llm
from app.ai.requirement_analyzer import analyze_requirement
from app.ai.task_decomposer import decompose_tasks
from app.ai.validator import validate_output
from app.db.session import get_db
from app.schemas.engineering import EngineeringRunRequest, EngineeringRunResponse
from app.schemas.link import (
    CreateLinkRequest,
    CreateLinkResponse,
    LinkMetadataResponse,
    LinkStatsResponse,
)
from app.services.url_shortener import create_link, get_link, get_metadata, get_stats, register_click

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/links", response_model=CreateLinkResponse)
def create_short_link(payload: CreateLinkRequest, request: Request, db: Session = Depends(get_db)):
    base_url = str(request.base_url).rstrip("/")
    return create_link(
        db=db,
        original_url=str(payload.original_url),
        base_url=base_url,
        custom_alias=payload.custom_alias,
        expires_at=payload.expires_at,
    )


@router.get("/{short_code}")
def redirect_short_link(
    short_code: str,
    request: Request,
    referrer: str | None = Header(default=None),
    user_agent: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    link = get_link(db, short_code)
    client_ip = request.client.host if request.client else None
    register_click(db, link, referrer=referrer, user_agent=user_agent, client_ip=client_ip)
    return RedirectResponse(url=link.original_url, status_code=307)


@router.get("/links/{short_code}", response_model=LinkMetadataResponse)
def get_link_metadata(short_code: str, db: Session = Depends(get_db)):
    return get_metadata(db, short_code)


@router.get("/links/{short_code}/stats", response_model=LinkStatsResponse)
def get_link_stats(short_code: str, db: Session = Depends(get_db)):
    return get_stats(db, short_code)


@router.post("/engineering/run", response_model=EngineeringRunResponse)
def run_engineering_pipeline(payload: EngineeringRunRequest):
    llm_result = generate_with_llm(payload.requirement, payload.scenario_type)

    if llm_result is not None:
        artifacts = llm_result["artifacts"]
        provider = artifacts.pop("provider", "llm")  # Extract provider and remove from artifacts
        artifacts["generation_mode"] = provider
        validation = validate_output(artifacts)
        return {
            "clarified_problem": llm_result["clarified_problem"],
            "ambiguities": llm_result["ambiguities"],
            "assumptions": llm_result["assumptions"],
            "tasks": llm_result["tasks"],
            "artifacts": artifacts,
            "validation": validation,
        }

    analyzed = analyze_requirement(payload.requirement, payload.scenario_type)
    tasks = decompose_tasks(payload.requirement, payload.scenario_type)
    artifacts = generate_artifacts(payload.requirement, payload.scenario_type, tasks)
    artifacts["generation_mode"] = "fallback"
    validation = validate_output(artifacts)

    return {
        "clarified_problem": analyzed["clarified_problem"],
        "ambiguities": analyzed["ambiguities"],
        "assumptions": analyzed["assumptions"],
        "tasks": tasks,
        "artifacts": artifacts,
        "validation": validation,
    }
