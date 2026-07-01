from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "AI-Assisted Software Engineering Prototype"
    database_url: str = "sqlite:///./url_shortener.db"


settings = Settings()
