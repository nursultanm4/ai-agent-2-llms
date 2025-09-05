# AI Agent - LLM Orchestration System

A full-stack AI agent system that orchestrates multiple LLM models to provide intelligent responses through a web interface.

## Core Features

### 🧠 **Dual LLM Orchestration**
- **Orchestrator**: Gemma 3 1B model analyzes user queries and creates focused prompts
- **Executor**: gpt-4o-mini generates final responses using refined prompts
- **Fallback System**: Graceful handling of orchestrator failures

### ⚡ **Performance Optimizations**
- **In-Memory Caching**: TTL-based cache with configurable expiration
- **Request Tracking**: Unique IDs for debugging and monitoring
- **Retry Logic**: Exponential backoff for API failures
- **Connection Pooling**: Efficient API client management

### 🔍 **Monitoring & Observability**
- **Structured Logging**: File rotation with configurable levels
- **Health Endpoints**: Service status and cache statistics
- **Request Metrics**: Duration tracking and performance monitoring
- **Error Handling**: Comprehensive error logging and user feedback

### 🛡️ **Security & Configuration**
- **Environment-Based Config**: Secure API key management
- **CORS Protection**: Configurable origin restrictions
- **Input Validation**: Pydantic schema validation
- **Rate Limiting**: Built-in retry mechanisms

## How the LLM Orchestration Works

### 1. **Query Processing Pipeline**
```
User Query → Cache Check → Orchestrator → Executor → Response
```

### 2. **Orchestrator Role (Gemma 3 1B)**
- Analyzes user intent and context
- Creates focused, well-structured prompts
- Handles query routing and clarification
- Provides context for the executor

### 3. **Executor Role (Gemma 3n E2B)**
- Generates detailed, accurate responses
- Uses orchestrator's refined prompts
- Maintains conversation quality
- Handles complex reasoning tasks

### 4. **Caching Strategy**
- **TTL-Based**: Configurable expiration (default: 600s)
- **Key-Based**: Query-based cache keys
- **Statistics**: Hit/miss tracking via `/healthz/cache`

## Technology Stack

### Backend
- **Framework**: FastAPI with async/await
- **LLM Integration**: Google AI Studio & OpenAI
- **Caching**: cachetools with TTL
- **Logging**: Python logging with rotation
- **Validation**: Pydantic schemas

### Frontend
- **Framework and Build Tool**: React & TS & Vite for fast development
- **Styling**: CSS modules
- **HTTP Client**: Fetch API

### Development
- **Package Manager**: pip (Python), npm (Node.js)
- **Environment**: dotenv for configuration
- **Documentation**: Swagger UI (FastAPI auto-generated)

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google AI Studio API key

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp env_template.txt .env
# Edit .env with your GOOGLE_API_KEY
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
```bash
# Required
GOOGLE_API_KEY=your_gemma_api_key
OPENAI_API_KEY=your_openai_api_key

GEMMA_ORCHESTRATOR_MODEL=gemma-3-1b-it
OPENAI_EXECUTOR_MODEL=gpt-4o-mini
CACHE_TTL_SECONDS=600
LOG_LEVEL=INFO
```

## API Endpoints

- `GET /` - Root info
- `GET /healthz` - Health check
- `GET /healthz/cache` - Cache statistics
- `POST /api/ask` - Main AI query endpoint
- `GET /docs` - Interactive API documentation

## Development Workflow

1. **Local Development**: Both services run on localhost with hot reload
2. **Testing**: Manual testing via Swagger UI and frontend
3. **Logging**: Comprehensive logs in `backend/logs/`
4. **Monitoring**: Health endpoints for service status

## Production Considerations

- **Environment**: Set `DEBUG=False` for production
- **Logging**: Configure appropriate log levels
- **Caching**: Adjust TTL based on usage patterns
- **Security**: Review CORS settings for deployment
- **Scaling**: Consider Redis for distributed caching

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper logging
4. Test via health endpoints
5. Submit a pull request