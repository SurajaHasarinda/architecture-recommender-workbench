# Configuration Guide

## Overview

All application configuration is centralized in `app/config.py` using the `Settings` class. This class uses Pydantic settings management to load configuration from environment variables or use default values.

## Configuration File Location

**Primary configuration**: `app/config.py`  
**Environment variables**: `.env` file in the project root

## Available Settings

### API Configuration

| Setting       | Type | Default                             | Description                                 |
| ------------- | ---- | ----------------------------------- | ------------------------------------------- |
| `app_name`    | str  | "Architecture Recommendation Agent" | Application name displayed in API responses |
| `app_version` | str  | "1.0.0"                             | Application version                         |
| `api_prefix`  | str  | "/api"                              | API route prefix                            |

### Google Gemini Configuration

| Setting            | Type | Default                     | Description                  | Required |
| ------------------ | ---- | --------------------------- | ---------------------------- | -------- |
| `google_api_key`   | str  | -                           | Your Google Gemini API key   | ✅ Yes   |
| `embedding_model`  | str  | "models/text-embedding-004" | Gemini embedding model name  | No       |
| `generation_model` | str  | "gemini-2.5-pro"            | Gemini generation model name | No       |

### ChromaDB Configuration

| Setting                    | Type | Default             | Description                        |
| -------------------------- | ---- | ------------------- | ---------------------------------- |
| `chroma_persist_directory` | str  | "./chroma_db"       | Directory for ChromaDB persistence |
| `chroma_collection_name`   | str  | "architecture_docs" | Name of the ChromaDB collection    |

### Document Configuration

| Setting          | Type | Default               | Description                                  |
| ---------------- | ---- | --------------------- | -------------------------------------------- |
| `docs_directory` | str  | "./architecture_docs" | Directory containing architecture .txt files |

### RAG Configuration

| Setting                | Type | Default | Description                                     |
| ---------------------- | ---- | ------- | ----------------------------------------------- |
| `top_k_results`        | int  | 5       | Number of documents to retrieve for RAG context |
| `embedding_batch_size` | int  | 100     | Batch size for embedding generation             |

### Server Configuration

| Setting     | Type | Default   | Description                                 |
| ----------- | ---- | --------- | ------------------------------------------- |
| `host`      | str  | "0.0.0.0" | Server host address                         |
| `port`      | int  | 8000      | Server port                                 |
| `reload`    | bool | True      | Enable auto-reload on code changes          |
| `log_level` | str  | "INFO"    | Logging level (DEBUG, INFO, WARNING, ERROR) |

### CORS Configuration

| Setting            | Type | Default | Description               |
| ------------------ | ---- | ------- | ------------------------- |
| `cors_origins`     | list | ["*"]   | Allowed CORS origins      |
| `cors_credentials` | bool | True    | Allow credentials in CORS |
| `cors_methods`     | list | ["*"]   | Allowed HTTP methods      |
| `cors_headers`     | list | ["*"]   | Allowed HTTP headers      |

## How to Configure

### Method 1: Environment Variables (Recommended)

Create a `.env` file in the project root:

```env
# Required
GOOGLE_API_KEY=your_actual_api_key_here

# Optional - Override defaults
EMBEDDING_MODEL=models/text-embedding-004
GENERATION_MODEL=gemini-2.5-pro
CHROMA_PERSIST_DIRECTORY=./my_custom_db
TOP_K_RESULTS=10
PORT=9000
LOG_LEVEL=DEBUG
```

### Method 2: Direct Modification

Edit `app/config.py` and change the default values:

```python
class Settings(BaseSettings):
    # Change any default value here
    port: int = 9000  # Changed from 8000
    top_k_results: int = 10  # Changed from 5
```

## Configuration Usage in Code

The settings are automatically loaded and available throughout the application:

```python
from app.config import settings

# Access any setting
api_key = settings.google_api_key
model_name = settings.generation_model
port = settings.port
```

## Environment Variable Naming

Pydantic automatically converts setting names to environment variables:

- Case insensitive (as configured)
- `google_api_key` → `GOOGLE_API_KEY`
- `embedding_model` → `EMBEDDING_MODEL`
- `top_k_results` → `TOP_K_RESULTS`

## Configuration Validation

Settings are validated on application startup:

- **Required fields**: The app will fail to start if `google_api_key` is missing
- **Type validation**: Pydantic ensures correct types (int, str, bool, list)
- **Default values**: All optional settings have sensible defaults

## Production Configuration

For production deployment, consider:

1. **Security**:

   ```python
   cors_origins: list = ["https://yourdomain.com"]  # Don't use "*"
   ```

2. **Performance**:

   ```python
   reload: bool = False  # Disable auto-reload
   log_level: str = "WARNING"  # Reduce log verbosity
   ```

3. **Scaling**:
   ```python
   top_k_results: int = 10  # Increase for better context
   embedding_batch_size: int = 200  # Larger batches if API allows
   ```

## Troubleshooting

### Issue: "GOOGLE_API_KEY environment variable is not set"

**Solution**: Create a `.env` file with `GOOGLE_API_KEY=your_key`

### Issue: Settings not updating

**Solution**:

1. Check `.env` file syntax (no spaces around `=`)
2. Restart the application
3. Verify environment variable names match (case-insensitive)

### Issue: Wrong model being used

**Solution**: Override in `.env`:

```env
EMBEDDING_MODEL=models/text-embedding-004
GENERATION_MODEL=gemini-2.5-pro
```

## Configuration Files Modified

The following files now use the centralized settings:

- ✅ `main.py` - API key, server config, CORS, app metadata
- ✅ `app/services/gemini_service.py` - Model names
- ✅ `app/services/vector_store.py` - ChromaDB paths (via main.py)
- ✅ `app/services/rag_service.py` - Top-K results
- ✅ `app/utils/document_loader.py` - Docs directory (via main.py)

## Summary

**Before**: Configuration scattered across multiple files with hardcoded values  
**After**: Single source of truth in `app/config.py`, easily overridable via `.env`

**Key Benefit**: Change any configuration value in ONE place (`app/config.py` or `.env`) and it applies everywhere!
