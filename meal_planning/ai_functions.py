import json
import logging
from google.api_core import exceptions
from .ai_config import client, GEMINI_MODEL_NAME, get_ai_model_config
from .schemas import Recipe

logger = logging.getLogger(__name__)

class AIServiceError(Exception):
    pass


def get_recipe_content(prompt_text):
    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=prompt_text,
        config=get_ai_model_config()
    )

    if not response or not response.text:
        return None

    return json.loads(response.text)


def get_recipe_content_with_retries(prompt_text, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            data = get_recipe_content(prompt_text)

            if data is None:
                continue

            clean_recipes = []

            for item in data:
                try:
                    recipe_obj = Recipe(
                        recipe_name=item.get("recipe_name"),
                        prep_time_min=item.get("prep_time_min", 0),
                        list_of_ingredients=item.get("list_of_ingredients", []),
                        instructions=item.get("instructions", [])
                    )

                    if recipe_obj.recipe_name and recipe_obj.instructions:
                        clean_recipes.append(recipe_obj)

                except TypeError as e:
                    logger.warning(f"Failed to map AI data to Recipe dataclass: {e}")
                    continue

            if not clean_recipes:
                logger.warning("AI returned valid JSON but no valid recipe object")
                continue

            return clean_recipes

        except json.JSONDecodeError:
            logger.error("AI returned invalid JSON formatting. Retrying...")
            continue

        except (exceptions.ResourceExhausted, exceptions.ServiceUnavailable) as e:
            raise AIServiceError("The AI is currently busy or offline. Please try again later.")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            if attempt == max_attempts - 1:
                raise AIServiceError("An unexpected error occurred.")

    return []

