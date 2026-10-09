import json
import os
import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from google.genai import types
from pydantic import BaseModel, ValidationError


load_dotenv()

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

_client = None

RETRYABLE_CODES = {429, 500, 503, 504}


def _generate_with_retry(model, contents, config, max_attempts=4):
    """Call Gemini and retry temporary errors with exponential backoff."""
    for attempt in range(1, max_attempts + 1):
        try:
            return get_client().models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )
        except errors.APIError as error:
            if error.code not in RETRYABLE_CODES or attempt == max_attempts:
                raise

            wait = 2 ** attempt
            print(
                f"[retry] Gemini error {error.code}. "
                f"Waiting {wait}s (attempt {attempt}/{max_attempts})..."
            )
            time.sleep(wait)


def get_client():
    global _client

    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY not found. Check your .env file."
            )

        _client = genai.Client(api_key=api_key)

    return _client


def ask(prompt, system=None, temperature=0.2, model=None):
    config = types.GenerateContentConfig(
        system_instruction=system,
        temperature=temperature,
    )

    response = _generate_with_retry(
    model=model or DEFAULT_MODEL,
    contents=prompt,
    config=config,
)

    if not response.text:
        raise ValueError("Model returned no text (blocked or cut off).")

    return response.text


def parse_json_response(text, model_class):
    cleaned = text.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        cleaned,
    )

    try:
        return model_class.model_validate_json(cleaned)

    except ValidationError as error:
        raise ValueError(
            f"LLM output did not match {model_class.__name__}: {error}"
        ) from error


def ask_json(
    prompt,
    model_class,
    system=None,
    temperature=0.0,
    model=None,
    retries=1,
):
    schema = json.dumps(
        model_class.model_json_schema(),
        indent=2,
    )

    full_prompt = (
        f"{prompt}\n\n"
        "Respond with ONLY valid JSON matching this JSON schema. "
        "No explanation and no markdown.\n"
        f"{schema}"
    )

    config = types.GenerateContentConfig(
        system_instruction=system,
        temperature=temperature,
        response_mime_type="application/json",
    )

    last_error = None

    for _ in range(retries + 1):
        response = _generate_with_retry(
            model=model or DEFAULT_MODEL,
            contents=full_prompt,
            config=config,
        )

        try:
            return parse_json_response(
                response.text or "",
                model_class,
            )

        except ValueError as error:
            last_error = error

    raise last_error