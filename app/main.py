from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.db.session import Base, engine
from app.models.click_event import ClickEvent
from app.models.link import Link

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-Assisted Software Engineering Prototype")

# Demo-friendly CORS policy. Restrict origins explicitly for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Prototype is running",
        "docs": "/docs",
    }
