from mistralai import Mistral
from mistralai.models.sdkerror import SDKError
from fastapi import HTTPException
import time

def call_mistral_with_retry(client, prompt, max_retries=3):
    """Call Mistral API with retry and exponential backoff."""
    for attempt in range(max_retries):
        try:
            response = client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            return response
        except SDKError as e:
            if "429" in str(e) or "capacity exceeded" in str(e):
                if attempt == max_retries - 1:
                    raise HTTPException(
                        status_code=429,
                        detail="API rate limit exceeded. Please try again later."
                    )
                wait_time = (2 ** attempt)  # Exponential backoff
                time.sleep(wait_time)
            else:
                raise HTTPException(
                    status_code=503,
                    detail=f"API error: {str(e)}"
                )
    return None
