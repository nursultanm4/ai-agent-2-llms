import os
from openai import OpenAI
from config import settings
import asyncio

client = OpenAI(api_key=settings.OPENAI_API_KEY)


### had to run in a thread, so FastAPI endpoint stays async and responsive after finding out that OpenAI executor failed: Object ChatCompletion can't be used in 'await' expression.

def sync_gpt4o(request_id: str, prompt: str) -> str:
    response = client.chat.completions.create(
        model=settings.OPENAI_EXECUTOR_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    # Defensive: check if choices exist and have content
    if hasattr(response, "choices") and response.choices and hasattr(response.choices[0], "message") and response.choices[0].message and hasattr(response.choices[0].message, "content"):
        return response.choices[0].message.content.strip()
    else:
        # Returns a clear error message for logging and frontend
        return "Sorry, the AI model did not return a valid answer."

async def call_gpt4o(request_id: str, prompt: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_gpt4o, request_id, prompt)

# response.choices[0]. 
### -- модель может вернуть несколько вариантов ответа; берём первый .
######## -- Logs: OpenAI executor failed after 3.18s: object ChatCompletion can't be used in 'await' expression


# Agent is sometimes returning a "redefined prompt" and hardcoded config texts, instead of real answers to users' requests. This happens because the orchestrator (Gemma) is mistakenly sends those directly to the user.
# We gotta ensure only the executor model's answer is returned to the user, never the orchestrator's suggestions or prompt refinements.


#  + Frontend feature: let user stop agent while it's still thinking.

