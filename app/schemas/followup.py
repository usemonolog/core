from pydantic import BaseModel, Json
from typing import Dict, List

class GeneratedFollowUp(BaseModel):
    status: str  # "follow-up-needed" or "sufficient"
    follow_up_questions: List[str]  # List of follow-up questions in JSON format
