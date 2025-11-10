# src/ner.py

from typing import List, Tuple
import re

# Common medical terms and phrases that might appear in transcripts
_MED_PHRASES = [
    'whiplash', 'physiotherapy', 'painkillers', 'x-ray',
    'neck pain', 'back pain', 'head impact', 'stiffness',
    'tenderness', 'range of motion', 'backaches', 'headache',
    'backache', 'lower back strain', 'head impact'
]
# Function: extract_med_terms
# Purpose : Extracts and normalizes medical-related terms
#           (e.g., symptoms, treatments) from text.

def extract_med_terms(text: str) -> List[str]:
    # Convert to lowercase for easy matching
    t = text.lower()
    found = []

    # 1️ Look for patterns like "ten physiotherapy sessions" etc.
    for match in re.finditer(r'(\b\d+\b|\bten\b|\beleven\b|\btwo\b)\s+(physiotherapy)\s+sessions?', text, flags=re.I):
        num = match.group(1)
        if num.lower() == 'ten':
            num = '10'
        found.append(f"{num} physiotherapy sessions")

    # 2 Check if any phrase from _MED_PHRASES exists in text
    for p in _MED_PHRASES:
        if p in t:
            # Capitalize properly for clean output
            if p in ['neck pain', 'back pain', 'head impact', 'backache', 'headache', 'range of motion']:
                pretty = p.title()
            else:
                pretty = p.capitalize()

            if pretty not in found:
                found.append(pretty)

    # 3️ Normalize a few common variations (for consistent output)
    normalized = []
    for f in found:
        ff = f.lower()
        if 'painkill' in ff:
            normalized.append('Painkillers')
        elif 'physiotherapy' in ff and 'session' not in ff:
            normalized.append('Physiotherapy')
        else:
            normalized.append(f)

    # 4️ Remove duplicates (while preserving order)
    out = []
    for x in normalized:
        if x not in out:
            out.append(x)

    return out

# Function: extract_cardinals
# Purpose : Extracts numeric values (e.g., number of sessions)
#           and converts words like "ten" into digits.

def extract_cardinals(text: str) -> List[str]:
    # Find all numbers or number words
    nums = re.findall(r'\b(\d+|ten|eleven|two|three|four|five|six|seven|eight|nine)\b', text, flags=re.I)
    normalized = []

    for n in nums:
        # Convert words like 'ten' → '10'
        if n.lower() == 'ten':
            normalized.append('10')
        else:
            try:
                normalized.append(str(int(n)))
            except:
                normalized.append(n)

    return normalized
