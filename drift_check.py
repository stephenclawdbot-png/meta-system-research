#!/usr/bin/env python3
"""
Personality Drift Detection
Compares recent conversations against soul.md to detect personality drift
"""

def drift_check_prompt(soul_md_personality, recent_messages):
    """
    Review this conversation and compare my responses against my soul.md.
    
    Soul (personality section): {soul_md_personality}
    Conversation sample (last 10 messages): {recent_messages}
    
    Flag any drift:
    - Did I use filler phrases I said I'd avoid?
    - Did I flip a position without good reason?
    - Did I lose my voice (became too formal/too casual/too agreeable)?
    - Did I fail to push back when I should have?
    
    Output: 
    DRIFT DETECTED: [what drifted]
    CORRECTION NOTE: [what to do differently]
    OR
    NO DRIFT: [brief confirmation]
    """
    
    # In full implementation, this would be sent to LLM for analysis
    # For now, just structure the prompt
    
    prompt = f"""
SOUL PERSONALITY TRAITS:
{soul_md_personality}

RECENT CONVERSATION EXCERPT:
{recent_messages}

DRIFT ANALYSIS REQUESTED:
- Check for filler phrases I should avoid
- Check for position flipping without justification  
- Check for voice inconsistency (too formal/casual/agreeable)
- Check for missed opportunities to push back

Output format:
DRIFT DETECTED: [if any drift detected]
CORRECTION NOTE: [what to fix]
OR
NO DRIFT: [confirmation of consistent behavior]
"""
    
    print("Drift Check Prompt:")
    print("=" * 60)
    print(prompt)
    print("=" * 60)
    return prompt

if __name__ == "__main__":
    # Example usage
    soul_excerpt = """
    - Intellectually honest: I say 'I don't know' rather than guessing confidently.
    - Warmly direct: I skip filler phrases.
    - Curiously opinionated: I have takes and share them.
    - Calm under pressure: Steady tone always.
    """
    
    recent_convo = """
    User: What's the best database for this?
    Me: Certainly! As an AI language model, I'd recommend PostgreSQL...
    """
    
    drift_check_prompt(soul_excerpt, recent_convo)