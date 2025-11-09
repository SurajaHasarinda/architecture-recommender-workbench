from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Configuration
    app_name: str = "Architecture Recommendation Agent"
    app_version: str = "1.0.0"
    api_prefix: str = "/api"
    
    # Google Gemini Configuration
    google_api_key: str
    embedding_model: str = "models/text-embedding-004"
    generation_model: str = "gemini-2.5-pro"
    
    # ChromaDB Configuration
    chroma_persist_directory: str = "./chroma_db"
    chroma_collection_name: str = "architecture_docs"
    
    # Document Configuration
    docs_directory: str = "./architecture_docs"
    
    # RAG Configuration
    top_k_results: int = 5
    embedding_batch_size: int = 100
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    log_level: str = "INFO"
    
    # CORS Configuration
    cors_origins: list = ["*"]
    cors_credentials: bool = True
    cors_methods: list = ["*"]
    cors_headers: list = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
