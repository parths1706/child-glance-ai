import json
import os

def select_insights(child_data):
    """
    NEW FLOW (for all countries):
    1. Call insights_generator which extracts personality from astrology (India) or age (others)
    2. Matches personality against traits database
    3. Returns matched personality traits as insights
    """
    from ai.insights_generator import generate_insights
    
    # The new generate_insights handles everything:
    # - For India: astrology → personality keywords → trait matching
    # - For others: age-based keywords → trait matching
    insights = generate_insights(child_data)
    
    if isinstance(insights, list) and len(insights) > 0:
        return insights
    
    # Fallback: return empty list if something fails
    return []

def get_available_pool(country, current_selection_ids):
    """
    Returns traits from the traits database that are NOT in the current selection.
    Used for the "Add Insight" dropdown.
    """
    TRAITS_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "traits_database.json")
    
    if not os.path.exists(TRAITS_DB_PATH):
        return []

    try:
        with open(TRAITS_DB_PATH, "r", encoding="utf-8") as f:
            traits_db = json.load(f)
    except:
        return []
    
    # Filter out what's already selected
    pool = [
        {
            "id": trait["id"],
            "category": trait["category"],
            "title": trait["title"],
            "description": trait["description"],
            "source": "personality_trait"
        }
        for trait in traits_db
        if trait["id"] not in current_selection_ids
    ]
    
    return pool
