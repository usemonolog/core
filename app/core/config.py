from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os 

load_dotenv()

class Settings(BaseSettings):
    CLERK_JWKS_URL: str = os.getenv("CLERK_JWKS_URL")
    CLERK_ISSUER: str = os.getenv("CLERK_ISSUER")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    CEREBRAS_API_KEY: str = os.getenv("CEREBRAS_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    ASSEMBLYAI_API_KEY: str = os.getenv("ASSEMBLYAI_API_KEY")
    ENV: str = os.getenv("ENV", "development")
    
    # Cloudflare R2 Settings
    CLOUDFLARE_R2_TOKENVALUE: str = os.getenv("CLOUDFLARE_R2_TOKENVALUE")
    CLOUDFLARE_R2_ENDPOINT: str = os.getenv("CLOUDFLARE_R2_ENDPOINT")
    CLOUDFLARE_R2_ACCESS_KEY_ID: str = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID")
    CLOUDFLARE_R2_SECRET_ACCESS_KEY: str = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
    CLOUDFLARE_R2_BUCKET_NAME: str = os.getenv("CLOUDFLARE_R2_BUCKET_NAME")
    CLOUDFLARE_R2_PUBLIC_URL: str = os.getenv("CLOUDFLARE_R2_PUBLIC_URL")  #  R2 custom domain or public URL

    class Config: 
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()