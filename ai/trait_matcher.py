from ai.llm_client import ask_llm, clean_json_response
import json
import os

TRAITS_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "traits_database.json")

def load_traits_database():
    """Load the traits database from JSON file."""
    try:
        with open(TRAITS_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def match_traits_with_ai(astro_traits, max_matches=6):
    """
    Uses AI to match astrological personality traits against the database.
    
    Args:
        astro_traits: List of personality keywords extracted from horoscope
        max_matches: Maximum number of traits to return
    
    Returns:
        List of matched trait objects from database
    """
    traits_db = load_traits_database()
    
    if not traits_db or not astro_traits:
        return []
    
    # Create a simplified version for the AI prompt
    traits_summary = "\n".join([
        f"- {t['id']}: {t['title']} ({', '.join(t['keywords'][:3])})"
        for t in traits_db
    ])
    
    astro_keywords = ", ".join(astro_traits) if isinstance(astro_traits, list) else astro_traits
    
    prompt = f"""
You are a child psychology expert matching personality traits.

TASK:
Based on the astrological personality keywords provided, select the {max_matches} BEST MATCHING traits from the database below.

ASTROLOGICAL PERSONALITY KEYWORDS:
{astro_keywords}

TRAITS DATABASE:
{traits_summary}

RULES:
1. Return ONLY the trait IDs that best match the astrological personality
2. Choose traits that semantically align with the keywords
3. Return exactly {max_matches} trait IDs (or fewer if not enough good matches)
4. Output as a simple JSON array of trait IDs

OUTPUT FORMAT:
["trait_id_1", "trait_id_2", "trait_id_3", ...]

NO extra text, ONLY the JSON array.
"""
    
    for _ in range(3):
        response = ask_llm(prompt)
        cleaned = clean_json_response(response)
        if cleaned:
            try:
                matched_ids = json.loads(cleaned)
                if isinstance(matched_ids, list):
                    # Get full trait objects for matched IDs
                    matched_traits = [
                        trait for trait in traits_db 
                        if trait["id"] in matched_ids
                    ]
                    return matched_traits[:max_matches]
            except:
                continue
    
    return []
