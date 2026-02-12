from ai.llm_client import ask_llm

def generate_astro_analysis(child_data):
    """
    Step 1: Generate horoscope, Rashi, and moon alignment analysis.
    Step 2: Extract personality trait keywords from the astrological data.
    
    Returns: List of personality keywords (e.g., ["energetic", "leader", "impulsive"])
    """
    is_indian = child_data.get("country", "") == "India"
    
    if not is_indian:
        # For non-Indian children, return generic keywords based on age
        age = child_data.get("age_years", 0)
        if age <= 2:
            return ["curious", "playful", "dependent"]
        elif age <= 5:
            return ["energetic", "curious", "creative"]
        elif age <= 8:
            return ["active", "friendly", "imaginative"]
        else:
            return ["independent", "social", "analytical"]
    
    prompt = f"""
ACT AS A PROFESSIONAL INDIAN PANDIT (ASTROLOGER):
- You are an expert in Vedic Astrology (Jyotish), Rashi Shastra, and Nakshatras.
- Based on the child's Birth Date, Birth Time, and Birth City, you MUST determine their:
    1. Rashi (Moon Sign): Choose precisely one from the 12 Vedic Rashi signs
    2. Moon Alignment and Nakshatra
    3. Personality tendencies according to their Rashi

TASK:
Analyze the child's astrological profile and extract PERSONALITY TRAIT KEYWORDS.

STEP 1: Determine Rashi and Moon Alignment
- Calculate the correct Rashi based on DOB and Birth Time
- Identify the Nakshatra and Moon position

STEP 2: Extract Personality Keywords
Based on the Rashi and astrological analysis, extract 5-8 personality trait keywords.
Examples: energetic, calm, leader, shy, analytical, creative, impulsive, patient, etc.

OUTPUT FORMAT (STRICT JSON ONLY):
{{
  "rashi": "Name of Rashi (e.g., Mesh, Kark, Dhanu)",
  "nakshatra": "Name of Nakshatra",
  "moon_alignment": "Brief description of moon position",
  "personality_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}}

RULES:
- NO extra text outside JSON
- personality_keywords should be simple adjectives describing behavior/temperament
- Focus on behavioral traits, not spiritual predictions

CHILD PROFILE:
- Age: {child_data.get("age_years", 0)} years
- DOB: {child_data.get("dob")}
- Birth Time: {child_data.get("birth_time", "Not provided")}
- Location: {child_data.get("city")}, {child_data.get("country")}
"""
    
    response = ask_llm(prompt)
    
    # Try to parse the response
    try:
        import json
        from ai.llm_client import clean_json_response
        cleaned = clean_json_response(response)
        if cleaned:
            data = json.loads(cleaned)
            return data.get("personality_keywords", [])
    except:
        pass
    
    # Fallback: return generic keywords
    return ["curious", "energetic", "friendly"]


def generate_insights(child_data):
    """
    NEW FLOW:
    1. Generate astrological analysis and extract personality keywords
    2. Match keywords against traits database using AI
    3. Return matched traits as insights
    
    This function is called by insight_selector.py
    """
    from ai.trait_matcher import match_traits_with_ai
    
    # Step 1: Get personality keywords from astrology
    personality_keywords = generate_astro_analysis(child_data)
    
    # Step 2: Match against database
    matched_traits = match_traits_with_ai(personality_keywords, max_matches=6)
    
    # Step 3: Format as insights
    insights = []
    for trait in matched_traits:
        insights.append({
            "id": trait["id"],
            "category": trait["category"],
            "title": trait["title"],
            "description": trait["description"],
            "source": "personality_trait"
        })
    
    return insights
