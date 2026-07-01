import hashlib
import secrets
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.click_event import ClickEvent
from app.models.link import Link


def utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def generate_short_code(length: int = 7) -> str:
    token = secrets.token_urlsafe(10)
    return token[:length]


def create_link(db: Session, original_url: str, base_url: str, custom_alias: str | None = None, expires_at: datetime | None = None):
    short_code = custom_alias or generate_short_code()

    existing = db.query(Link).filter(Link.short_code == short_code).first()
    if existing:
        raise HTTPException(status_code=409, detail="Short code already exists")

    link = Link(
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at,
    )
    db.add(link)
    db.commit()
    db.refresh(link)

    return {
        "short_code": link.short_code,
        "short_url": f"{base_url}/{link.short_code}",
        "original_url": link.original_url,
        "created_at": link.created_at,
        "expires_at": link.expires_at,
    }


def get_link(db: Session, short_code: str) -> Link:
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    if link.expires_at and link.expires_at < utc_now_naive():
        raise HTTPException(status_code=410, detail="Link has expired")
    return link


def register_click(db: Session, link: Link, referrer: str | None, user_agent: str | None, client_ip: str | None):
    link.click_count += 1
    link.last_accessed_at = utc_now_naive()

    ip_hash = None
    if client_ip:
        ip_hash = hashlib.sha256(client_ip.encode("utf-8")).hexdigest()

    event = ClickEvent(
        link_id=link.id,
        referrer=referrer,
        user_agent=user_agent,
        ip_hash=ip_hash,
    )
    db.add(event)
    db.add(link)
    db.commit()


def get_metadata(db: Session, short_code: str):
    link = get_link(db, short_code)
    return {
        "original_url": link.original_url,
        "short_code": link.short_code,
        "created_at": link.created_at,
        "expires_at": link.expires_at,
        "click_count": link.click_count,
        "last_accessed_at": link.last_accessed_at,
    }


def get_stats(db: Session, short_code: str):
    link = get_link(db, short_code)
    return {
        "short_code": link.short_code,
        "total_clicks": link.click_count,
        "last_accessed_at": link.last_accessed_at,
    }
