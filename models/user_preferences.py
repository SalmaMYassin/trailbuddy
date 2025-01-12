from pydantic import BaseModel
from typing import List

class UserPreferences(BaseModel):
    destination: str
    duration: int
    interests: List[str]
    budget: float
