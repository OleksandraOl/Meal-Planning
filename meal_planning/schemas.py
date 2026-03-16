from dataclasses import dataclass
from typing import List

@dataclass
class Recipe:
    recipe_name: str
    prep_time_min: int
    list_of_ingredients: List[str]
    instructions: List[str]
