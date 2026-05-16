from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/mototracker.db"
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    scraper_user_agent: str = "MotoTracker/0.1 (price-history tracker; contact: mateusz.grucha@gmail.com)"
    throttle_min_seconds: float = 1.0
    throttle_jitter_seconds: float = 1.0
    scraper_max_pages: int = 20

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
