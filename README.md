# Physician Notetaker

This project is called **Physician Notetaker**. It is a simple NLP-based system that can read doctor-patient conversations, find useful medical details, and summarize them into easy-to-read notes.

---

## 📘 What this project does

* Reads medical transcripts
* Splits the text into doctor and patient parts
* Finds medical keywords (like symptoms, medicines, vitals)
* Creates short summaries of the discussion
* Detects the patient’s emotions (positive, neutral, negative)
* Converts the information into a **SOAP** format — Subjective, Objective, Assessment, and Plan

---

##  Setup Instructions

### Step 1: Clone the project

```bash
git clone <your-repo-url>
cd physician-notetaker
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

Activate it:

* Windows: `venv\Scripts\activate`
* macOS/Linux: `source venv/bin/activate`

### Step 3: Install all dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the project

```bash
python -m src.run_pipeline --input data/sample_transcript.txt --output outputs/result.json
```

### Step 5: Run tests (optional)

```bash
pytest
```

---

## Folder Structure

physician-notetaker/
│
├── data/ # Sample input transcript(s)
│ └── sample_transcript.txt
│
├── notebooks/ # Jupyter notebooks for demos or experiments
│ └── demo_notebook.ipynb
│
├── outputs/ # NLP pipeline results
│ ├── summary.json
│ ├── sentiment.json
│ └── soap.json
│
├── src/ # Source code modules
│ ├── init.py
│ ├── preprocessing.py # Cleans and splits dialogue text
│ ├── summarizer.py # Generates medical summaries
│ ├── sentiment.py # Detects patient sentiment & intent
│ ├── soap_mapper.py # Maps extracted data to SOAP structure
│ └── run_pipeline.py # Main entry point for running the pipeline
│
├── tests/ # Unit tests for code validation
│ └── test_pipeline.py
│
├── requirements.txt # All required Python packages
├── README.md # Project documentation
└── run_debug.py # Debug/testing entry point


##  Common Questions and Answers

### 1. How would you handle ambiguous or missing medical data in the transcript?

If some information is missing or confusing, I would:

* Mark uncertain parts as “not sure” or “not mentioned”
* Use context to guess meaning when possible
* Flag unclear data for a doctor to check
* Use multiple predictions and show confidence scores

This keeps the system honest and safe.

---

### 2. What pre-trained NLP models would you use for medical summarization?

I would use models that already understand medical text, like:

* **BioBERT** or **ClinicalBERT** for understanding medical words
* **T5** or **BART** for creating short summaries
* **Longformer** for long conversations

These models are good at reading and summarizing text clearly.

---

### 3. How would you fine-tune BERT for medical sentiment detection?

Steps:

1. Start with **ClinicalBERT** (trained on real hospital text)
2. Add a small classifier layer on top
3. Train it using data labeled with emotions (positive, neutral, negative)
4. Use small learning rates (like 2e-5)
5. Stop training when validation score stops improving

This helps detect patient emotions like fear, relief, or pain accurately.

---

### 4. What datasets would you use for training a healthcare-specific sentiment model?

I would use:

* **MIMIC-III / MIMIC-IV** (real hospital notes)
* **i2b2 datasets** (annotated medical text)
* **Health forums / Reddit** for patient opinions

If none are perfect, I’d make a small labeled dataset with doctors’ help.

---

### 5. How would you train an NLP model to map medical transcripts into SOAP format?

Two ways:

1. **Rule-based** – Tag each sentence as Subjective, Objective, Assessment, or Plan.
2. **AI-based** – Train a text-to-text model like T5 that learns from examples of transcripts and SOAP notes.

Best method: Combine both. Use rules for accuracy and AI for natural writing.

---

### 6. What rule-based or deep learning techniques would improve SOAP note accuracy?

**Rule-based:**

* Use speaker roles (doctor/patient)
* Detect negations like “no fever”
* Keep latest vitals only
* Normalize medical terms using UMLS or SNOMED

**Deep Learning:**

* Use **ClinicalBERT** for medical meaning
* Use **T5** or **BART** for generating final SOAP text
* Use **NER models** to find symptoms and medicines
* Use multi-task learning to connect emotion + summary + SOAP parts together

Together, they make more accurate and meaningful medical notes.
