#!/usr/bin/env python3
"""
META-SYSTEM: Project Idea Generator
Generates breakthrough concepts that should exist but don't
"""

import random
import json
from datetime import datetime

IDEA_SEEDS = [
    {
        "domain": "Computing Interfaces",
        "prompts": [
            "What if computers could sense intention before action?",
            "What if displays didn't need light to be visible?",
            "What if keyboards were obsolete?",
            "What if screens could be anywhere in your field of view?",
            "What if computers could read stress levels and adapt?"
        ],
        "tech_angles": ["EMG", "EEG", "ultrasound haptics", "airborne ultrasound", "thermal imaging"]
    },
    {
        "domain": "Energy Systems",
        "prompts": [
            "What if batteries weren't needed for small devices?",
            "What if energy could be harvested from body heat reliably?",
            "What if wireless power worked across a room efficiently?",
            "What if piezoelectric could power wearables practically?"
        ],
        "tech_angles": ["RF harvesting", "thermoelectric", "piezo", " triboelectric", "micro-turbines"]
    },
    {
        "domain": "Communication",
        "prompts": [
            "What if translation happened in real-time without cloud?",
            "What if you could whisper to someone across a noisy room?",
            "What if braille displays were refreshable and cheap?",
            "What if lip reading was automated privately?"
        ],
        "tech_angles": ["ultrasound beams", "haptic braille", "edge ML", "bone conduction arrays"]
    },
    {
        "domain": "Sensing",
        "prompts": [
            "What if you could see around corners without mirrors?",
            "What if air quality was continuously monitored personally?",
            "What if posture was corrected automatically?",
            "What if object recognition worked without cameras?"
        ],
        "tech_angles": ["time-of-flight", "coherent detection", "radar", "capacitive sensing"]
    },
    {
        "domain": "Manufacturing",
        "prompts": [
            "What if desktop fabrication made PCBs obsolete?",
            "What if 3D printing was 100× faster?",
            "What if circuits were grown not etched?",
            "What if self-assembly was reliable?"
        ],
        "tech_angles": ["photopolymer", "electrohydrodynamic", "microfluidic", "DNA origami"]
    }
]

def generate_concept():
    """Generate a breakthrough concept"""
    domain = random.choice(IDEA_SEEDS)
    prompt = random.choice(domain['prompts'])
    tech = random.sample(domain['tech_angles'], 2)
    
    # Generate concept name
    words = ['flux', 'echo', 'resonance', 'field', 'wave', 'pulse', 'node', 'vertex', 'anchor', 'beacon']
    concept_name = f"{random.choice(words).upper()}{random.randint(100, 999)}"
    
    concept = {
        "id": concept_name,
        "domain": domain['domain'],
        "seed_question": prompt,
        "tech_angles": tech,
        "hypothesis": f"Combine {tech[0]} and {tech[1]} to solve: {prompt}",
        "feasibility_estimate": random.choice([0.3, 0.5, 0.6, 0.7, 0.8]),
        "generated_at": datetime.now().isoformat()
    }
    
    return concept

def main():
    """Generate and print a concept"""
    concept = generate_concept()
    
    print(f"\n🎯 NEW CONCEPT GENERATED: {concept['id']}")
    print(f"Domain: {concept['domain']}")
    print(f"Question: {concept['seed_question']}")
    print(f"Approach: {concept['hypothesis']}")
    print(f"Feasibility: {concept['feasibility_estimate']*100:.0f}%")
    print(f"Time: {concept['generated_at']}")
    
    # Save to file
    with open('/Users/clawdbot/.openclaw/workspace/META_SYSTEM/IDEA_QUEUE.json', 'a') as f:
        f.write(json.dumps(concept) + '\n')
    
    return concept

if __name__ == "__main__":
    main()
