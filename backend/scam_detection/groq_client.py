"""
Scam Detection API Client Integration (Person C Scope)
"""

import json
import logging
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

from config import Config
from scam_detection.prompt import SYSTEM_INSTRUCTION, get_scam_detection_prompt
from scam_detection.feedback_loop import get_recent_correction_hints

logger = logging.getLogger(__name__)

# Pydantic schema for Gemini structured output
class ScamAnalysisSchema(BaseModel):
    scam_score: int = Field(description="Scam risk score from 0 to 100")
    scam_flags: list[str] = Field(description="Plain-English red flags identified in the listing")
    tip: str = Field(description="Advice for the buyer")

def analyze_scam_patterns(title: str, description: str, seller_info: str | None) -> dict:
    """
    Analyzes listing title, description, and seller_info for scam patterns.
    Uses Google GenAI SDK with gemini-3.6-flash.
    
    Returns:
    {
      "scam_score": int,        # 0-100, higher = more suspicious
      "scam_flags": list[str],  # plain-English red flags, [] if none found
      "tip": str,               # plain-English buyer advice
      "raw_llm_response": str   # optional, debug only, never surfaced to frontend
    }
    """
    # 1. Fetch recent correction hints from the feedback loop
    correction_hints = get_recent_correction_hints()
    
    # 2. Build prompt content
    prompt_content = get_scam_detection_prompt(title, description, seller_info, correction_hints)
    
    # 3. Retrieve API key
    api_key = getattr(Config, "GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured in Config.")
        
    # 4. Initialize client
    client = genai.Client(api_key=api_key)
    
    # Configure generation config
    gen_config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        response_mime_type="application/json",
        response_schema=ScamAnalysisSchema,
        temperature=0.1,
    )
    
    # 5. Execute with retry logic (up to 2 attempts)
    max_attempts = 2
    last_error = None
    
    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt_content,
                config=gen_config,
            )
            
            raw_text = response.text
            if not raw_text:
                raise ValueError("Empty response text from Gemini API")
                
            # 6. Safety Net: Manual json.loads + key/type validation pass
            parsed = json.loads(raw_text)
            
            # Retrieve fields
            scam_score_val = parsed.get("scam_score")
            scam_flags_val = parsed.get("scam_flags")
            tip_val = parsed.get("tip")
            
            # Validate scam_score
            if scam_score_val is None:
                raise ValueError("Response missing required key 'scam_score'")
            try:
                # Coerce to float first to handle string representations of numbers, round, then cast to int
                score_numeric = float(scam_score_val)
                score_int = int(round(score_numeric))
            except (ValueError, TypeError) as e:
                raise ValueError(f"scam_score is not a valid number: {scam_score_val}") from e
                
            # Clamp to 0-100 range
            score_int = max(0, min(100, score_int))
            
            # Validate scam_flags
            if scam_flags_val is None:
                scam_flags_list = []
            elif isinstance(scam_flags_val, list):
                # Ensure every item in list is coerced to string
                scam_flags_list = [str(flag) for flag in scam_flags_val]
            else:
                # scam_flags must always be a list[str], never a bare string or other types
                raise ValueError("scam_flags must be a list of strings")
                
            # Validate tip
            if tip_val is None:
                raise ValueError("Response missing required key 'tip'")
            tip_str = str(tip_val)
            
            # Success - return matching exact contract
            return {
                "scam_score": score_int,
                "scam_flags": scam_flags_list,
                "tip": tip_str,
                "raw_llm_response": raw_text
            }
            
        except Exception as e:
            logger.warning(f"Scam detection API attempt {attempt + 1} failed: {e}")
            last_error = e
            
    # Unrecoverable error after retries
    raise RuntimeError(f"Unrecoverable error during scam detection analysis: {last_error}") from last_error