from typing import Dict
from app.schemas.guideline import GeneratedGuideline
from app.services.llm_service import LLMService
import json

class GuidelineGenerator:
    @staticmethod
    async def generate(context: str) -> GeneratedGuideline: 
        try: 
            prompt = f"""You are an expert communication coach. Based on the provided scenario context, create a comprehensive communication guideline that will help users communicate effectively in this specific situation.

SCENARIO CONTEXT:
{context}

Please generate:
1. A clear, descriptive title for this communication scenario
2. Knowledge foundation explaining the key principles
3. Specific, actionable guidelines (5-7 key points)

Return your response in this exact JSON format:
{{
    "title": "A clear, descriptive title for this scenario",
    "knowledge_foundation": "A comprehensive explanation of the communication principles, psychology, and best practices relevant to this scenario. Include why these approaches work and what to avoid.",
    "guideline": {{
        "Opening Approach": "How to start the conversation appropriately",
        "Tone and Language": "What tone to use and language choices",
        "Key Points to Cover": "Essential information that must be communicated",
        "Active Listening": "How to demonstrate listening and engagement",
        "Handling Objections": "How to address concerns or pushback",
        "Closing Strategy": "How to end the conversation effectively",
    }}
}}

Make the guidelines specific to the scenario context provided. Each guideline point should be actionable and measurable."""

            response = await LLMService.get_completion(prompt)
            response_text = response.get("text", "").strip()
            
            # Try to parse JSON response
            try:
                parsed_response = json.loads(response_text)
                return GeneratedGuideline(
                    title=parsed_response["title"],
                    knowledge_foundation=parsed_response["knowledge_foundation"],
                    guideline=parsed_response["guideline"]
                )
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON response from LLM: {response_text}")
                
        except Exception as e:
            raise Exception(f"Guideline generation failed: {str(e)}")
            