def get_system_instructions():
    return """
        You are a recipe generator. 
        Your goal is to provide recipes
        Respond ONLY in valid JSON. No conversational filler.
    """

def build_recipe_prompt(ingredients):
    return f"""
        Based on these ingredients: {ingredients}, provide a recipe suggestions. 
        Return a list of objects where each object has keys:
            "recipe_name" (a string of 50 characters or less),
            "prep_time_min" (integer in minutes),
            "list_of_ingredients" (a list of strings),
            "instructions"(a list of steps).
    """