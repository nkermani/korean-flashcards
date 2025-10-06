# app/mistral_client.py
# This module handles interactions with the Mistral API, including retry logic for rate limiting.

from mistralai import Mistral
from mistralai.models.sdkerror import SDKError
from fastapi import HTTPException
import asyncio
import time


def _sync_call_with_retry(client, prompt, max_retries=3):
    """Synchronous call + retry for callers that pass an explicit client.

    Keeps existing synchronous usage unchanged: call_mistral_with_retry(client, prompt)
    """
    for attempt in range(max_retries):
        try:
            response = client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": prompt}],
            )
            return response
        except SDKError as e:
            if "429" in str(e).lower() or "capacity exceeded" in str(e).lower():
                if attempt == max_retries - 1:
                    raise HTTPException(
                        status_code=429,
                        detail="API rate limit exceeded. Please try again later.",
                    )
                wait_time = 2**attempt
                time.sleep(wait_time)
            else:
                raise HTTPException(status_code=503, detail=f"API error: {str(e)}")


async def _async_call_with_retry(prompt, max_retries=3):
    """Async call used when caller supplies only the prompt and awaits the result.

    This function lazy-imports the module-level `client` from
    `app.services.flashcard_service` so tests can patch that client.
    """
    # Create a default Mistral client here using configured API key so this
    # module is self-contained. Importing a `client` from other modules is
    # fragile and caused runtime import errors in the past.
    try:
        from app.config import api_key
        if not api_key:
            raise RuntimeError("MISTRAL_API_KEY not configured")
        default_client = Mistral(api_key=api_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No Mistral client available: {e}")

    for attempt in range(max_retries):
        try:
            resp = default_client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": prompt}],
            )

            if asyncio.iscoroutine(resp):
                resp = await resp

            return resp
        except SDKError as e:
            err = str(e).lower()
            if "429" in err or "capacity exceeded" in err:
                if attempt == max_retries - 1:
                    raise HTTPException(
                        status_code=429,
                        detail="API rate limit exceeded. Please try again later.",
                    )
                wait_time = 2**attempt
                await asyncio.sleep(wait_time)
            else:
                raise HTTPException(status_code=503, detail=f"API error: {str(e)}")


def call_mistral_with_retry(*args, max_retries: int = 3):
    """Entrypoint supporting both calling conventions:

    - Synchronous: call_mistral_with_retry(client, prompt) -> response
    - Asynchronous: await call_mistral_with_retry(prompt) -> response
    """
    if len(args) == 0:
        raise TypeError("call_mistral_with_retry() missing required arguments")

    if len(args) >= 2:
        client = args[0]
        prompt = args[1]
        return _sync_call_with_retry(client, prompt, max_retries=max_retries)

    # single-arg form -> return coroutine to be awaited by caller
    prompt = args[0]
    return _async_call_with_retry(prompt, max_retries=max_retries)
