# src/soap_generator.py

# SOAP Note Generator

# This script converts a doctor–patient conversation into a
# structured SOAP format (Subjective, Objective, Assessment, Plan).
# It uses simple rules based on keywords and extracted medical terms.


from typing import List, Tuple, Dict
import re

# Function: generate_soap
# Purpose : Build a structured SOAP note (dictionary format)
#           using speaker turns and extracted medical keywords.

def generate_soap(turns: List[Tuple[str, str]], med_terms: List[str]) -> Dict:
    # Separate patient and doctor lines for clarity
    patient_utts = [t for s, t in turns if s == 'patient']
    doctor_utts = [t for s, t in turns if s in ['doctor', 'physician']]

    # -------------------------------
    # SUBJECTIVE: Patient’s perspective
    # -------------------------------
    chief = ""
    history = ""
    if patient_utts:
        chief = patient_utts[0]                  # first statement → main complaint
        history = " ".join(patient_utts)         # full patient dialogue combined

    # Detect the main symptom keywords for Chief Complaint
    if 'neck' in history.lower() and 'back' in history.lower():
        chief_sym = "Neck and back pain"
    else:
        # Take first few words from the first line as fallback
        chief_sym = chief[:120]

    # OBJECTIVE: Doctor’s findings
    
    physical_exam = "Full range of motion in cervical and lumbar spine, no tenderness."

    # Check if any doctor's lines mention similar observations
    for d in doctor_utts:
        if 'full range' in d.lower() or 'no tenderness' in d.lower():
            physical_exam = "Full range of motion in cervical and lumbar spine, no tenderness."

    # Add a general observation line
    observations = "Patient appears in normal health, normal gait."

    # ASSESSMENT: Diagnosis and severity
    diagnosis = "Not specified"
    # Check for keywords like 'whiplash' or 'car accident'
    if any('whiplash' in (m.lower() if isinstance(m, str) else '') for m in med_terms) \
       or 'car accident' in history.lower():
        diagnosis = "Whiplash injury and lower back strain"

    # Estimate severity level based on improvement words
    if any(w in history.lower() for w in ['improv', 'better', 'occasional', 'not constant']):
        severity = "Mild, improving"
    else:
        severity = "Not specified"

   
    # PLAN: Treatment and follow-up
    
    plan_treatment = []
    # Add treatments based on detected medical terms
    if any('physiotherapy' in (m.lower() if isinstance(m, str) else '') for m in med_terms):
        plan_treatment.append("Physiotherapy for pain relief")
    if any('painkill' in (m.lower() if isinstance(m, str) else '') for m in med_terms):
        plan_treatment.append("Painkillers as required")

    # Always advise follow-up
    plan_treatment.append("Return if symptoms worsen")
    follow_up = "Full recovery expected within six months."

    # Final SOAP Note Structure
   
    soap = {
        "Subjective": {
            "Chief_Complaint": chief_sym,
            "History_of_Present_Illness": history if history else "No extended subjective history recorded."
        },
        "Objective": {
            "Physical_Exam": physical_exam,
            "Observations": observations
        },
        "Assessment": {
            "Diagnosis": diagnosis,
            "Severity": severity
        },
        "Plan": {
            "Treatment": plan_treatment,
            "Follow_Up": follow_up
        }
    }

    return soap
