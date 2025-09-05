from fastapi import APIRouter, Request, HTTPException
from schemas import QueryRequest, QueryResponse
from services.llm_service import LLMService
from services.cache_service import CacheService
from logger import log_request, log_response, log_error, logger
from config import settings
import time
import uuid

from starlette.background import BackgroundTask
from fastapi import BackgroundTasks


router = APIRouter(prefix="/api", tags=["AI Agent"])


#  + Background tasks are included
@router.post("/ask", summary="Ask the AI Agent a question", response_model=QueryResponse)
async def ask_agent(request: Request, query_request: QueryRequest, background_tasks: BackgroundTasks):
    
    if hasattr(request.state, "is_cancelled"):
        raise HTTPException(status_code=499, detail="Client cancelled request")

    """Main endpoint for AI agent queries"""
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    # Store request_id in request state for logging
    request.state.request_id = request_id
    
    user_query = query_request.query
    
    log_request(request_id, "/api/ask", "POST", user_query)
    
    try:
        # Initialize services
        cache_service = CacheService()
        llm_service = LLMService()
        
        # Check the cache first
        cached_response = cache_service.get(user_query)
        if cached_response:
            duration = time.time() - start_time
            log_response(request_id, duration, 200, cached=True)
            return QueryResponse(
                answer=cached_response,
                meta={"cached": True, "model": "cached", "request_id": request_id}
            )
        
        # Step 1: Orchestration with Gemma
        logger.info(f"Request {request_id}: Starting orchestration with Gemma")
        orchestrator_response = await llm_service.call_gemma_orchestrator(request_id, user_query)
        
        # Step 2: Execution
        logger.info(f"Request {request_id}: Starting execution with Gemma")
        final_answer = await llm_service.call_openai_executor(request_id, orchestrator_response)
        # If the answer is the fallback error message, log as error
        if final_answer.startswith("Sorry, the AI agent could not generate a proper answer"):
            logger.error(f"Request {request_id}: Executor failed to generate a proper answer for query: {user_query}")
        
        # Store in cache
        cache_service.set(user_query, final_answer)
        
        # Close the LLM service
        await llm_service.close()
        
        duration = time.time() - start_time
        log_response(request_id, duration, 200, cached=False)
        
        return QueryResponse(
            answer=final_answer,
            meta={
                "cached": False,
                "model": f"{settings.GEMMA_ORCHESTRATOR_MODEL} + {settings.OPENAI_EXECUTOR_MODEL}",
                "request_id": request_id,
                "orchestrator_prompt": orchestrator_response
            }
        )
        
    except Exception as e:
        duration = time.time() - start_time
        log_error(request_id, e, "ask_agent")
        
        # Close LLM service on error
        try:
            await llm_service.close()
        except:
            pass
        
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )
