from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    AGENT_URLS: str = (
        "http://agent1:8001,http://agent2:8002,http://agent3:8003,http://agent4:8004"
    )

    REDIS_HOST: str = "host.docker.internal"
    REDIS_PORT: int = 6379

    class Config:
        env_file = ".env"

    @property
    def agent_list(self) -> List[str]:
        return [url.strip() for url in self.AGENT_URLS.split(",") if url.strip()]


settings = Settings()
