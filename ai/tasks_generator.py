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
You are a disciplined Child Development Coach.

TASK:
Create 4–8 character-building tasks for the CHILD to complete.

IMPORTANT:
This is NOT a pampering app.
Tasks must build discipline, responsibility, respect, and obedience.

Child Age: {age_desc}

CORE RULES:

1. TASKS MUST BE DONE BY THE CHILD.
   Parent guides, but child must perform the task.

2. AGE APPROPRIATE:
   - Age 0-2: Very simple habits (clap, hold spoon, put toy back)
   - Age 3-5: Basic responsibility (put toys away, greet elders, tell parents about day)
   - Age 6-8: Responsibility (make bed, pack school bag, complete homework on time)
   - Age 9-12: Discipline (prepare school items, help in house chores, respect all elders including workers)
   - Age 13+: Accountability (manage study time, assist family work, control screen time)

3. CHARACTER FOCUS:
   Tasks must build:
   - Discipline
   - Respect for elders (regardless of status)
   - Listening to parents
   - Clean habits
   - Responsibility
   - Self-control

4. LANGUAGE STYLE:
   - Simple clear instructions.
   - Not baby tone.
   - Not cartoon.
   - No excessive emojis.
   - Firm but positive tone.

5. CONNECT TO TRAITS:
   If child shows:
   - Anger → self-control tasks
   - Laziness → routine tasks
   - Shyness → communication tasks
   - Messy behavior → cleanliness tasks
   - Disrespect → greeting and respect tasks

FORMAT:
Return ONLY JSON list:

[
  {{
    "title": "Clear Task Title",
    "description": "2–3 clear sentences explaining what the child must do and why it improves character."
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
- Tasks must improve the child.
- Tasks must be realistic.
- Tasks must match age {age_desc}.
- Tasks must be doable daily.
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
