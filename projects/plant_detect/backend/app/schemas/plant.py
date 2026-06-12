from pydantic import BaseModel, Field
from typing import List, Optional

class PlantMatch(BaseModel):
    common_name: str
    scientific_name: str
    confidence_percentage: int = Field(ge=0, le=100)
    description: str
    care_tips: List[str]
    toxicity: str
    origin: str
    fun_fact: str

class IdentificationResult(BaseModel):
    is_plant: bool
    message: Optional[str] = None
    results: Optional[List[PlantMatch]] = None