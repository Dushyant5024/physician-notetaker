# tests/test_preprocessing.py
# Simple unit test file for the preprocessing module

from src.preprocessing import split_turns

# Basic test for split_turns() function
def test_split_turns():
    # Sample short doctor-patient conversation
    text = """Doctor: Hello
Patient: Hi
Patient: I have pain"""

    # Run the function to split conversation into turns
    turns = split_turns(text)

    # We expect two turns: one from doctor, one from patient
    assert len(turns) == 2

    # Optional extra check for speaker labels
    assert turns[0][0] == 'doctor'
    assert turns[1][0] == 'patient'
