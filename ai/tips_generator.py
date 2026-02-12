from ai.llm_client import ask_llm, clean_json_response
import json

def generate_parenting_tips(child_data, selected_traits):
    """
    Generate parenting tips based on child's personality traits.
    Tips focus on helping parents manage and improve the child's behavior.
    """
    
    traits_text = "\n".join(
        f"- {t.get('title', 'Trait')}: {t.get('description', '')}"
        for t in selected_traits
    )

    prompt = f"""
You are the BEST parenting coach in the whole world! 🌟👨‍👩‍👧💖

TASK:
Give 4-6 super helpful parenting tips based on the child's personality traits.

RULES:
1. BABY WORDS ONLY: Use very very simple English! Like talking to a 5 year old! No big words! 👶✨
2. LOTS OF EMOJIS: Put emojis EVERYWHERE to make it fun and happy! 🎈🌈🍭🎉
3. WHAT & HOW: Tell parents WHAT to do and HOW to do it (step by step!)
4. DETAILED: Each tip should be 4-5 sentences long
5. PERSONALITY FOCUS: Give tips that help with the child's specific personality traits
6. MAKE IT FUN: Parents should LOVE reading this! Not boring! 🤗💕

FORMAT EXAMPLE:
[
  {{
    "title": "Help Your Angry Child Stay Calm 😤➡️😊",
    "description": "Your child gets angry sometimes. That's okay! 💕 What to do: Teach them to take deep breaths when upset. How to do it: When they get mad, sit with them and count to 10 together while breathing slowly. 🧘‍♀️ Then give them a big hug! 🤗 This helps them feel calm and safe. Do this every day and they will learn to stay peaceful! ✨"
  }}
]

CONTEXT:
Child's Personality Traits:
{traits_text}

Child Age: {child_data.get("age_years", 0)} years
Country: {child_data.get("country", "")}

Remember: SIMPLE WORDS + LOTS OF EMOJIS + FUN TO READ! 🎊
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