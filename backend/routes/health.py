from fastapi import APIRouter, Request
from datetime import datetime
from schemas import HealthResponse
from logger import log_request, log_response
from services.cache_service import CacheService
import time


router = APIRouter(prefix="/healthz", tags=["Monitoring"])


@router.get("/", summary="Health check", response_model=HealthResponse)
async def health_check(request: Request):
    """Health check endpoint"""
    start_time = time.time()
    request_id = str(request.state.request_id) if hasattr(request.state, 'request_id') else "unknown"
    
    log_request(request_id, "/healthz", "GET")
    
    # Get cache stats
    cache_service = CacheService()
    cache_stats = cache_service.get_stats()
    
    response = HealthResponse(
        status="ok",
        timestamp=datetime.utcnow().isoformat()
    )
    
    duration = time.time() - start_time
    log_response(request_id, duration, 200)
    
    return response


@router.get("/cache", summary="Cache statistics")
async def cache_stats(request: Request):
    """Get cache statistics"""
    request_id = str(request.state.request_id) if hasattr(request.state, 'request_id') else "unknown"
    
    log_request(request_id, "/healthz/cache", "GET")
    
    cache_service = CacheService()
    stats = cache_service.get_stats()
    
    duration = time.time()
    log_response(request_id, duration, 200)
    
    return stats