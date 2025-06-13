from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AIPROXY_TOKEN: str
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_MODEL: str = "gpt-4o-mini"
    API_BASE_URL: str = "https://aipipe.org/openai/v1"

settings = Settings()