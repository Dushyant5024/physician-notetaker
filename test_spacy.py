# spacy_test.py — quick check to see if spaCy is installed and working

# This small file just loads the spaCy English model
# and runs it on a short sample text to check entity recognition.
# It's a simple test before using spaCy in the main project.

import spacy

print("spaCy test starting...")

# Load the small English model (download first if not available)
# Command to download if missing: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

# A short example sentence with some medical-like words
doc = nlp("I had 10 physiotherapy sessions and neck pain.")

# Print all detected entities (words/phrases recognized by spaCy)
print("Entities found:", [(ent.text, ent.label_) for ent in doc.ents])

print("spaCy is working correctly!")

# End of file — just a basic functionality test, nothing complex :)
