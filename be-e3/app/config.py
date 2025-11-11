from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")
    
    supabase_url: str
    supabase_key: str
    api_key: str
    retell_api_key: str
    openai_api_key: str
    openai_model: str = "gpt-4o"
    retell_default_voice_id: str = "11labs-Adrian"
    webhook_base_url: str = "http://localhost:8000"

settings = Settings()

