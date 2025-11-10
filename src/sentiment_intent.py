# src/sentiment_intent.py

# Simple rule-based Sentiment and Intent detection module

# This script uses small keyword-based logic tuned to
# the assignment examples. It works fast and doesn’t
# depend on any external model.

def detect_sentiment(text: str) -> str:
    """
    Detects basic patient sentiment from a text segment.
    Returns one of: 'Anxious', 'Reassured', or 'Neutral'.
    """

    if not text:
        return "Neutral"

    t = text.lower()

    # If the sentence shows worry or fear
    if any(w in t for w in ['worried', 'worry', 'anxious', 'nervous']):
        return "Anxious"

    # If it contains signs of relief or positive progress
    if any(w in t for w in ['better', 'relieved', 'reassured', 'on track', 'full recovery']):
        return "Reassured"

    # Default / neutral tone
    return "Neutral"


def detect_intent(text: str) -> str:
    """
    Detects the likely patient intent based on simple phrase matching.
    Returns one of: 'Seeking reassurance', 'Reporting symptoms',
    'Scheduling/Follow-up', or 'Other'.
    """

    if not text:
        return "Other"

    t = text.lower()

    # If patient is asking or expressing worry → seeking reassurance
    if any(phrase in t for phrase in [
        "i'm a bit worried", "i am a bit worried", "i worry",
        "will i recover", "should i worry", "what will happen"
    ]):
        return "Seeking reassurance"

    # If patient describes pain or health issue → reporting symptoms
    if any(w in t for w in ['pain', 'hurt', 'injury', 'accident', 'symptom', 'backache', 'neck pain']):
        return "Reporting symptoms"

    # If message refers to future visit → scheduling or follow-up intent
    if any(w in t for w in ['follow up', 'follow-up', 'come back', 'return if', 'followup']):
        return "Scheduling/Follow-up"

    # Everything else (greetings, small talk, etc.)
    return "Other"
