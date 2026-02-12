from ai.llm_client import ask_llm, clean_json_response
import json

def generate_daily_tasks(child_data, traits, tips):
    """
    Generate child-focused tasks that help improve the child's behavior.
    Tasks are based on the child's personality traits and parenting tips.
    """
    
    traits_text = "\n".join(
        f"- {t.get('title', '')}: {t.get('description', '')}"
        for t in traits
    )
    
    # Extract tip titles/themes
    tips_summary = "\n".join(
        f"- {t.get('title', '')}"
        for t in tips if isinstance(t, dict)
    )
    
    age_yrs = child_data.get("age_years", 0)
    age_mos = child_data.get("age_months", 0)
    age_desc = f"{age_yrs} years and {age_mos} months" if age_yrs or age_mos else "unknown age"

    prompt = f"""
You are a super fun Task Master! 🎮🌟

TASK:
Create 4-6 VERY SIMPLE tasks for the CHILD to do. The child is {age_desc} old!

CRITICAL RULES - READ CAREFULLY:
1. BABY WORDS ONLY: Use the SIMPLEST words possible! Like: run, jump, play, draw, sing, hug, clean, put, take, give, help, count, color, dance, clap! 👶
2. NO BIG WORDS: Do NOT use words like: comfortably, charades, emotions, puzzle, showcase, treasure! These are too hard! ❌
3. AGE MATCH: A {age_desc} child must be able to DO this task easily! 
   - Age 0-2: Very very simple! Like clap hands, hug teddy, put toy in box
   - Age 3-5: Simple! Like draw a sun, count to 5, put shoes away
   - Age 6-8: Easy tasks! Like make bed, water plant, read a book
   - Age 9+: Can do more! Like cook simple food, clean room, help cook
4. CHILD TASKS: Tasks are for the CHILD to do (parent helps but child does it!)
5. IMPROVEMENT: Task should help fix the child's personality problem
6. FUN EMOJIS: Use lots of emojis! 🎈🌈✨
7. SHORT: Each task is 2-3 sentences only!

FORMAT EXAMPLE (for age 4):
[
  {{
    "title": "Put Your Toys Away! 🧸",
    "description": "Put all your toys back in the toy box! Mom or dad will help you. This makes you learn to be clean and neat! 🌟"
  }},
  {{
    "title": "Draw a Happy Face! 😊",
    "description": "Take a paper and draw a big happy face! Use colors you like! This helps you feel calm and happy! 🎨"
  }}
]

CONTEXT:
Child's Personality (what needs to improve):
{traits_text}

What Parents Are Learning:
{tips_summary}

Child Age: {age_desc}

REMEMBER: 
- VERY SIMPLE WORDS (like talking to a baby!)
- Age {age_desc} must be able to DO it!
- If child is ANGRY → calm tasks (draw, breathe, hug teddy)
- If child is SHY → brave tasks (say hi to family, show a toy)
- If child is LAZY → move tasks (run, jump, dance, play)
- If child is MESSY → clean tasks (put toys away, make bed)

Make it SUPER SIMPLE! 👶✨
"""
    
    for _ in range(3):
        res = ask_llm(prompt)
        cleaned = clean_json_response(res)
        if cleaned:
            try:
                json.loads(cleaned)
                return res
            except:
                continue
    return ""
