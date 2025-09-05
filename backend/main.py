import uuid      # to give IDs to requests
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from config import settings
from logger import logger, setup_logger
from routes import health, ai_agent


class RequestIDMiddleware(BaseHTTPMiddleware):
    #   МИДДЛВЕР СОЗДАЕМ ВНУТРИ main.py потому что этот класс мы больше нигде не используем. И эффективнее быстро создать его здесь рядом, чтобы не обращаться к другим модулям. 
    """Middleware to add request ID to each request"""
    
    async def dispatch(self, request: Request, call_next):
        request.state.request_id = str(uuid.uuid4())
        request.state.start_time = time.time()
        
        response = await call_next(request)
        
        # log request completion
        duration = time.time() - request.state.start_time
        logger.info(f"Request {request.state.request_id}: Completed in {duration:.2f}s")
        
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    
    # Start it up
    logger.info("Starting AI Agent Backend...")
    logger.info(f"Environment: {settings.LOG_LEVEL}")
    logger.info(f"Cache TTL: {settings.CACHE_TTL_SECONDS}s")
    logger.info(f"Max Retries: {settings.MAX_RETRIES}")
    logger.info(f"HTTP Timeout: {settings.HTTP_REQUEST_TIMEOUT_S}s")
    
    yield
     
    logger.info("Shutting down AI Agent Backend...")


app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan   ##   Когда запускаешь uvicorn, FastAPI автоматически вызовет эту функцию при старте/остановке. (учитывая yield).
)


# Add Middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(health.router)
app.include_router(ai_agent.router)


# Root endpoint
@app.get("/", summary="Root endpoint")
async def root():
    """Root endpoint with basic info"""
    return {
        "message": "AI Agent Backend",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/healthz"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )