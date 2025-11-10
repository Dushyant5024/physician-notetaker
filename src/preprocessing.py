# src/preprocess.py

# Preprocessing script
# This module helps load and clean physician–patient transcripts.
# It mainly:
# 1 Reads text files
# 2️ Splits conversation into speaker-wise turns


from pathlib import Path
from typing import List, Tuple

# Function: load_transcript
# Purpose : Reads the transcript file from a given path
#           and returns the entire text as a single string.

def load_transcript(path: str) -> str:
    """Read transcript file and return text"""
    return Path(path).read_text(encoding='utf-8')

# Function: split_turns
# Purpose : Breaks down transcript into speaker–utterance pairs.
# Example : ("doctor", "How are you feeling today?")

def split_turns(text: str) -> List[Tuple[str, str]]:
    """
    Split transcript into list of (speaker, text) pairs.

    Assumes lines starting with 'Physician:', 'Doctor:' or 'Patient:'.
    Continuation lines (no speaker) are appended to the previous speaker.
    """

    # Clean lines → remove blanks and extra spaces
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    turns = []
    for l in lines:
        low = l.lower()

        # Doctor lines → tag as 'doctor'
        if low.startswith(('physician:', 'doctor:')):
            turns.append(('doctor', l.split(':', 1)[1].strip()))

        # Patient lines → tag as 'patient'
        elif low.startswith('patient:'):
            turns.append(('patient', l.split(':', 1)[1].strip()))

        # If no speaker label → continuation of previous line
        else:
            if turns:
                turns[-1] = (turns[-1][0], turns[-1][1] + ' ' + l)

    return turns
