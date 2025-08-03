from typing import Dict, Optional
from pydantic import BaseModel, UUID4
from datetime import datetime

class ScenarioCreate(BaseModel):
    context: str
    additional_info: Optional[Dict[str, str]] = None


class Scenario(BaseModel):
    id: UUID4 
    user_id: str
    title: str
    knowledge_foundation: str
    guideline: Dict[str, str]
    created_at: datetime

    class Config:
        from_attributes = True
