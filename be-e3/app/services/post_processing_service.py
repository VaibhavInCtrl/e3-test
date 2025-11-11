import json
import logging
from openai import AsyncOpenAI
from typing import Dict
from app.config import settings

logger = logging.getLogger(__name__)

class PostProcessingService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def extract_structured_data(
        self,
        transcript: str,
        scenario_description: str
    ) -> Dict:
        system_prompt = """You are an AI agent analyzing logistics dispatch call transcripts. Your task is to extract structured data from driver check-in conversations.

ANALYSIS INSTRUCTIONS:
1. Read the entire call transcript carefully
2. Identify what type of call this is based on the conversation content
3. Extract ALL relevant information discussed in the call
4. Return a JSON object containing only the data points that are relevant and mentioned
5. Use descriptive, clear keys for each data point
6. If a relevant data point was discussed but no clear answer was given, use null for that field
7. Do not include fields for information that was never discussed or referenced

GUIDELINES FOR EXTRACTION:

Call Classification:
- Determine if this is a routine status update, arrival confirmation, emergency situation, or other type
- Use a "call_outcome" field to categorize the call type

Driver Status & Location:
- Extract driver's current status (driving, arrived, unloading, delayed, etc.)
- Capture current location if mentioned
- Record estimated arrival time if discussed
- Note any delays and their reasons

Delivery Operations:
- Capture unloading status, door numbers, detention situations
- Note if proof of delivery reminders were acknowledged
- Record any operational issues or updates

Emergency Situations:
- If an emergency is mentioned, capture the emergency type (accident, breakdown, medical, etc.)
- Record safety status and whether anyone is injured
- Note the specific emergency location
- Indicate if the load is secure
- Document escalation actions (connecting to dispatcher, etc.)

DATA QUALITY RULES:
- Use clear, descriptive keys (snake_case preferred)
- Values should be concise but complete
- Use boolean true/false for yes/no questions that were clearly answered
- Use null only when a topic was discussed but the answer is unclear/not provided
- Use strings for descriptive information
- Keep location and status descriptions as provided by the driver
- Preserve specific details like door numbers, mile markers, times, etc.

OUTPUT FORMAT:
- Return ONLY valid JSON
- No explanations, preamble, or text outside the JSON
- Include only fields that are relevant to what was actually discussed
- Ensure proper JSON syntax (quoted keys, proper commas, etc.)


Extract the relevant structured data as JSON:
        """
        prompt = f"""Scenario requirements:
{scenario_description}

Call transcript:
{transcript}
"""
        logger.info("Calling OpenAI for structured data extraction")
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            logger.info("Successfully received response from OpenAI")
        except Exception as e:
            logger.error(f"Failed to call OpenAI: {e}")
            return {"error": "Failed to extract structured data", "details": str(e)}
        
        try:
            result = json.loads(response.choices[0].message.content)
            logger.info("Successfully parsed structured data")
            return result
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return {"error": "Failed to parse structured data", "raw_response": response.choices[0].message.content}