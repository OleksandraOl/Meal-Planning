from google import genai
from google.genai import types
from django.conf import settings
from .ai_prompts import get_system_instructions


GEMINI_MODEL_NAME = "gemini-3-flash-preview"


client = genai.Client(
    api_key = settings.GEMINI_API_KEY,
    http_options = types.HttpOptions(
        retry_options = types.HttpRetryOptions(
            attempts=3,
            initial_delay=1.0,
            http_status_codes=[429, 500, 502, 503, 504]
        )
    )
)


def get_ai_model_config():
    return types.GenerateContentConfig(
        system_instruction=get_system_instructions(),
        response_mime_type="application/json",
        temperature=0.7
    )

