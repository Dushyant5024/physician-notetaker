# src/run_pipeline.py
"""
Main orchestrator for the Physician Notetaker demo.

Reads the sample transcript, runs preprocessing, NER, sentiment/intent,
summarization and SOAP generation, then writes JSON outputs to `outputs/`.

This file is intentionally simple and linear so it's easy to follow during review.
"""

from pathlib import Path
import json
import sys

# Import pipeline pieces. If something is missing, print helpful error and re-raise.
try:
    from src.preprocessing import load_transcript, split_turns
    from src.ner import extract_med_terms, extract_cardinals
    from src.sentiment_intent import detect_sentiment, detect_intent
    from src.summarizer import build_summary
    from src.soap_generator import generate_soap
except Exception as e:
    # Keep the message short and readable for someone scanning logs.
    print("ERROR: import failed:", e, file=sys.stderr)
    raise


def main():
    """
    Pipeline steps:
    1. Read sample transcript
    2. Split into speaker turns
    3. Extract medical terms and numeric counts
    4. Run sentiment and intent detection (overall + per utterance)
    5. Build structured summary and SOAP note
    6. Write JSON outputs to outputs/
    """

    # Project-root-aware paths so this works whether the script is run from repo root
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "sample_transcript.txt"
    out_dir = project_root / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("DEBUG: reading:", data_path)
    text = load_transcript(str(data_path))
    print("DEBUG: transcript length:", len(text))

    # Preprocessing: split into (speaker, text) pairs
    turns = split_turns(text)
    print("DEBUG: turns count:", len(turns))

    # Show a quick preview of the first few turns for manual sanity-checking
    for i, (s, t) in enumerate(turns[:6]):
        print(f"  TURN {i+1}: {s} -> {t[:80]}")

    # Combine all utterances for global extraction steps
    all_text = " ".join(t for _, t in turns)

    # NER-ish extraction (simple phrase based / regex helpers)
    med_terms = extract_med_terms(all_text)
    print("DEBUG: med_terms:", med_terms)

    # Extract numeric/cardinal mentions (e.g., number of sessions)
    cardinals = extract_cardinals(all_text)
    print("DEBUG: cardinals:", cardinals)

    # Overall sentiment & intent (for the whole conversation)
    sentiment = detect_sentiment(all_text)
    intent = detect_intent(all_text)
    print("DEBUG: overall sentiment:", sentiment, "intent:", intent)

    # Build a structured summary (returns a dict expected to be JSON-serializable)
    summary = build_summary(turns, med_terms, sentiment)
    if isinstance(summary, dict):
        print("DEBUG: summary keys:", list(summary.keys()))
    else:
        print("DEBUG: summary type:", type(summary))

    # Generate SOAP note (also expected to be a serializable dict)
    soap = generate_soap(turns, med_terms)

    # Build per-utterance sentiment/intent so the output shows fine-grained results
    sentiment_output = {
        "overall_sentiment": sentiment,
        "overall_intent": intent,
        "per_utterance": [
            {
                "speaker": s,
                "text": t,
                "sentiment": detect_sentiment(t),
                "intent": detect_intent(t)
            }
            for s, t in turns
        ]
    }

    # Write outputs (pretty-printed JSON) so reviewers can open them easily
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "soap.json").write_text(json.dumps(soap, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "sentiment.json").write_text(json.dumps(sentiment_output, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Saved outputs to", out_dir)
    for p in sorted(out_dir.iterdir()):
        print(" -", p.name, f"({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
