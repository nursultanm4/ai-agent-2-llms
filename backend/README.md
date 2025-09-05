# AI Agent Backend

A FastAPI-based backend service that orchestrates LLM calls using Gemma 1 3B as an orchestrator and gpt-4o-mini as an executor.

## Architecture

The backend follows a modular architecture with clear separation of concerns:

```
backend/
├── main.py              # Main application entry point
├── config.py            # Configuration management
├── logger.py            # Logging setup and utilities
├── schemas.py           # Pydantic models for API validation
├── services/            # Business logic services
│   ├── __init__.py
│   ├── llm_service.py   # LLM API integration
│   └── cache_service.py # Caching layer
├── routes/              # API route handlers
│   ├── __init__.py
│   ├── health.py        # Health check endpoints
│   └── ai_agent.py      # Main AI agent endpoints
└── logs/                # Application logs (auto-created)
```

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **Comprehensive Logging**: Structured logging with file rotation and request tracking
- **Caching**: In-memory TTL cache for improved performance
- **Error Handling**: Robust error handling with retry logic
- **Request Tracking**: Unique request IDs for debugging and monitoring
- **Health Monitoring**: Health check endpoints with cache statistics

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Copy `env_template.txt` to `.env` and fill in your API keys:
   ```bash
   cp env_template.txt .env
   # Edit .env with your actual API keys
   ```

3. **Required Environment Variables**:
   - `GEMMA_API_KEY`: Your Gemma API key
   - GEMMA_ORCHESTRATOR_MODEL=gemma-3-1b-it
   - OPENAI_EXECUTOR_MODEL=gpt-4o-mini


## Running the Application

```bash
# Development mode with auto-reload
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# Production mode
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /`: Root endpoint with basic info
- `GET /healthz`: Health check
- `GET /healthz/cache`: Cache statistics
- `POST /api/ask`: Main AI agent query endpoint
- `GET /docs`: Interactive API documentation (Swagger UI)

## Logging

Logs are stored in the `logs/` directory with automatic rotation:
- Log level configurable via `LOG_LEVEL` environment variable
- File rotation with configurable size limits
- Request tracking with unique IDs
- Structured logging for easy parsing

## Caching

- In-memory TTL cache with configurable expiration
- Cache statistics available via `/healthz/cache` endpoint
- Automatic cache cleanup based on TTL

## LLM Integration

1. **Gemma 1 3B (Orchestrator)**: 
   - Analyzes user queries
   - Creates focused prompts for the executor
   - Handles query routing and context

2. **gpt-4o-mini (Executor)**:
   - Generates final responses
   - Uses orchestrator's refined prompts
   - Provides detailed answers to users

## Error Handling

- Automatic retries with exponential backoff
- Graceful fallbacks for orchestrator failures
- Comprehensive error logging
- User-friendly error messages

## Monitoring

- Request duration tracking
- Cache hit/miss statistics
- LLM API call monitoring
- Health check endpoints

