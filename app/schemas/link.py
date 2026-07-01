from datetime import datetime

from pydantic import BaseModel, HttpUrl


class CreateLinkRequest(BaseModel):
    original_url: HttpUrl
    custom_alias: str | None = None
    expires_at: datetime | None = None


class CreateLinkResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    created_at: datetime
    expires_at: datetime | None


class LinkMetadataResponse(BaseModel):
    original_url: str
    short_code: str
    created_at: datetime
    expires_at: datetime | None
    click_count: int
    last_accessed_at: datetime | None


class LinkStatsResponse(BaseModel):
    short_code: str
    total_clicks: int
    last_accessed_at: datetime | None
