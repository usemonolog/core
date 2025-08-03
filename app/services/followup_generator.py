from typing import Dict
from app.schemas.followup import GeneratedFollowUp
from app.schemas.guideline import GeneratedGuideline
from app.services.llm_service import LLMService
import json

class FollowUpGenerator:
    @staticmethod
    async def generate(context: str) -> GeneratedGuideline: 
        try: 
            prompt_dict = {
    "task": "Validate if user's scenario has enough context. If not, request clarification.",
    "rules": [
        "Respond in the user's input language.",
        "If scenario is vague (e.g., 'I need help with a presentation'), ask 3 follow-up questions like:",
        "What is the goal of your communication? (e.g., inform, persuade, negotiate)",
        "Who is your audience? (role, cultural background, pain points)",
        "What are your key challenges? (e.g., nervousness, unclear message)",
        "formulate questions relevant to the given scenario and context"
    ],
    "output_format": {
        "status": "follow-up-needed | sufficient",
        "follow_up_questions": ["..."]
    },
    "context": f"SCENARIO CONTEXT: {context}"
}
            prompt = json.dumps(prompt_dict, ensure_ascii=False)

            response = await LLMService.get_completion(prompt)
            response_text = response.get("text", "").strip()
            print(f"Parsed response: {response_text}")  
            
            # Try to parse JSON response
            try:
                parsed_response = json.loads(response_text)
                return GeneratedFollowUp(
                    status=parsed_response.get("status", "follow-up-needed"),
                    follow_up_questions=parsed_response.get("follow_up_questions", [])
                )
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON response from LLM: {response_text}")
                
        except Exception as e:
            raise Exception(f"Guideline generation failed: {str(e)}")
            