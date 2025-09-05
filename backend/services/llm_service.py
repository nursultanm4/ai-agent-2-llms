import time
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type
from config import settings
from logger import logger, log_llm_call
from google import genai
import time
from openai_api import call_gpt4o


class LLMService:
    """Service for handling LLM API calls - Google AI Studio with two Gemma models"""
    
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set")
        
        # Initialize Google AI client
        self.google_client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    
    
    # ISSUE  ---- >  FIXED
    # The orchestrator only generates a prompt, never a final answer.
    # The executor is always called with the orchestrator’s output (or the user’s query if the orchestrator fails).
    # Only the executor’s answer is returned to the user.

    async def call_gemma_orchestrator(self, request_id: str, user_query: str) -> str:
        """Call Gemma 3 1B as orchestrator to generate a prompt for the executor"""
        start_time = time.time()
        try:
            orchestrator_prompt = f"""You are an AI query optimizer. Your task is to take the user's question and optimize it for the AI executor to provide a direct, informative and accurate answer.

User Query: {user_query}

Change, optimize complex questions that require web search only.
Your task for those questions: Rephrase this as a clear, simple question. Do not provide suggestions or refinements - just optimize the question itself in a short, accurate way.
If it is not a question but conversational words like "hey" or direct messages towards the agent, just don't touch it and let it be.

Response format:
[Just the optimized question, nothing else]"""
            logger.info(f"Request {request_id}: Calling Gemma orchestrator")
            response = self.google_client.models.generate_content(
                model=settings.GEMMA_ORCHESTRATOR_MODEL,
                contents=orchestrator_prompt
            )
            orchestrator_response = response.text
            duration = time.time() - start_time
            log_llm_call(request_id, "Gemma Orchestrator", orchestrator_prompt, orchestrator_response, duration)
            # Always return the orchestrator's output as a prompt for the executor, never as a final answer
            return orchestrator_response.strip()
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Request {request_id}: Gemma orchestrator failed after {duration:.2f}s: {str(e)}")
            # Fallback: use the original user query as prompt for the executor
            return user_query

    async def call_openai_executor(self, request_id: str, prompt: str) -> str:
        """Call OpenAI gpt-4o-mini as executor to generate the final answer"""
        start_time = time.time()
        try:
            logger.info(f"Request {request_id}: Calling OpenAI executor")
            
            # Enhance the prompt to force a direct answer
            enhanced_prompt = f"""Answer this question directly and informatively: {prompt}

Instructions for AI:
1. Provide a direct, factual answer, be relatively short
2. Use clear, concise language
3. Include specific details where relevant
4. DO NOT suggest refinements or ask for clarification
5. DO NOT start with phrases like "Your prompt is" or "To answer this"
6. Just provide the informative answer. Use symbols like " or * or any other special symbols only when necessary, use correct grammar.

Answer:"""
            
            response = await call_gpt4o(request_id, enhanced_prompt)
            duration = time.time() - start_time
            
            # Check for orchestrator-like output or empty responses
            if any(phrase in response.strip().lower() for phrase in [
                "your prompt is",
                "suggestions for refinement",
                "to answer this question",
                "i need more context",
                "could you please clarify"
            ]):
                logger.error(f"Request {request_id}: Executor returned a prompt-like response")
                return "I apologize, but I couldn't generate a proper answer. Please try asking your question differently."
            
            log_llm_call(request_id, "OpenAI gpt-4o-mini", enhanced_prompt, response, duration)
            return response
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Request {request_id}: OpenAI executor failed after {duration:.2f}s: {str(e)}")
            return "Sorry, there was an error generating your answer."

    async def close(self):
        """Close client"""
        pass