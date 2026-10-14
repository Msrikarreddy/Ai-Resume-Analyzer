# AI Resume Analyzer

An AI-powered web application that analyzes a resume against a job description. It identifies recognized matching skills, highlights potential skill gaps, estimates semantic similarity between the two documents, generates personalized improvement suggestions, and creates a downloadable PDF report.

## Features

- **Resume upload:** Accepts PDF and DOCX resumes.
- **Text extraction:** Extracts text from PDF files using PyMuPDF and from DOCX files using `python-docx`.
- **Skill matching:** Detects skills from a predefined skill dictionary and compares resume skills with job-description skills.
- **Semantic similarity:** Uses the `sentence-transformers/all-MiniLM-L6-v2` model and cosine similarity to compare the meaning of the resume and job description.
- **Combined match score:** Calculates an experimental overall score using 60% skill coverage and 40% semantic similarity.
- **Skill-gap analysis:** Displays matched skills, potentially missing skills, and all recognized skills detected in each document.
- **Rule-based suggestions:** Generates recommendations from skill-matching results.
- **Local AI recommendations:** Uses a locally running Ollama model (`qwen2.5:3b`) to suggest improvements.
- **PDF report:** Creates a downloadable report containing scores, matched skills, skill gaps, and rule-based recommendations.
- **Streamlit interface:** Provides a browser-based interface for uploading a resume and entering a job description.

> **Important:** Match scores are experimental text-matching metrics. They are not a probability of receiving a job offer or a validated measure of candidate suitability. AI-generated advice may contain errors; verify all suggestions and never add skills or achievements you do not have.

## Technology Stack

- **Language:** Python
- **UI:** Streamlit
- **Resume parsing:** PyMuPDF, `python-docx`
- **Skill matching:** Python regular expressions
- **Semantic similarity:** Sentence Transformers, scikit-learn
- **Local language model:** Ollama with `qwen2.5:3b`
- **PDF generation:** ReportLab
- **HTTP requests:** Requests

## How It Works

1. Upload a resume in PDF or DOCX format.
2. Paste the target job description.
3. The application extracts readable text from the resume.
4. The skill matcher detects skills from its predefined dictionary and identifies matching and missing recognized skills.
5. The semantic matcher encodes the resume and job description with `all-MiniLM-L6-v2` and calculates cosine similarity.
6. The application calculates the experimental overall score:

   `Overall Match Score = (0.60 × Skill Coverage) + (0.40 × Semantic Similarity)`

7. Rule-based suggestions and Ollama-generated recommendations are displayed.
8. Download the analysis as a PDF report.

The skill matcher only recognizes skills included in its dictionary. A skill not detected by the program is not necessarily a skill the candidate lacks.

## Project Structure

The following is the expected structure based on the modules used by the application. Keep the filenames consistent with the imports in `app.py`.

```text
AI-Resume-Analyzer/
├── app.py
├── resume_parser.py
├── matcher.py
├── semantic_matcher.py
├── recommendations.py
├── ai_recommender.py
├── report_generator.py
├── test_semantic.py
├── requirements.txt
└── README.md
```

If your current resume extraction file is named `resumeparse.py`, either rename it to `resume_parser.py` or update the import in `app.py` to match. The same rule applies to `test semantic.py`: use the Python filename `test_semantic.py` if you want to run it as a script.

## Prerequisites

- Python installed on your computer
- Git (optional, for version control and GitHub)
- Ollama installed and running for local AI recommendations
- Internet access for the initial download of the Sentence Transformers model and its dependencies

Use a virtual environment so project packages do not interfere with other Python projects.

## Installation and Setup

### 1. Open the project folder

Open a terminal in the folder containing `app.py`.

### 2. Create and activate a virtual environment

**Windows — Command Prompt:**

```bat
python -m venv .venv
.venv\Scripts\activate
```

**Windows — PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt or follow your organization's PowerShell policy.

### 3. Install dependencies

Make sure the dependency file is named `requirements.txt` (not `requirement.txt`).

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install and start Ollama

Install Ollama from [https://ollama.com/](https://ollama.com/).

Then open a terminal and download the model:

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running. On Windows, the Ollama desktop application normally runs the local service. You can check that the model is available with:

```bash
ollama list
```

The application sends requests to `http://localhost:11434/api/generate`. The AI recommendation module uses the model name `qwen2.5:3b`. If Ollama is not running, the application will show a connection message for the AI recommendations.

### 5. Run the Streamlit app

From the project folder, with the virtual environment activated:

```bash
python -m streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open that URL in your browser.

## How to Use

1. Upload your resume as a PDF or DOCX file.
2. Paste the complete target job description.
3. Click **Analyze Resume**.
4. Review the overall match score, skill coverage, and semantic similarity.
5. Check matched skills and potential skill gaps.
6. Read the rule-based and AI-generated recommendations.
7. Click the PDF report download button to save the analysis.

For best text extraction, use a text-based PDF. Scanned PDFs may require OCR, which is not implemented in the supplied resume extraction module.

## Run the Semantic Similarity Test

After confirming the test script is named `test_semantic.py` and the project dependencies are installed, run:

```bash
python test_semantic.py
```

The first run may download the `all-MiniLM-L6-v2` model and can take longer than subsequent runs.

## Troubleshooting

### `ModuleNotFoundError: No module named 'resume_parser'`

The filename and import do not match. Rename `resumeparse.py` to `resume_parser.py`, or change the import in `app.py` to the actual module name.

### `ModuleNotFoundError: No module named 'recommendations'` or `semantic_matcher`

Ensure `recommendations.py` and `semantic_matcher.py` exist in the same project folder as `app.py`. These modules are imported by the application.

### Ollama is not running

Open the Ollama application, then check:

```bash
ollama list
```

If necessary, start the Ollama service according to your operating system's installation. Confirm that `qwen2.5:3b` appears in the model list.

### Resume text cannot be extracted

Try a text-based PDF or a DOCX file. Scanned/image-only PDFs may not contain extractable text; OCR support is not included in the supplied parser.

### Dependency installation fails

Check your Python version and the package versions in `requirements.txt`. Some pinned versions may not be available for every Python version or operating system. Install dependencies in a fresh virtual environment and review the exact pip error before changing version pins.

### The semantic model downloads slowly

The Sentence Transformers model is downloaded the first time it is used. Keep an internet connection active until the download finishes.

## Privacy

The AI recommendation module sends resume text and job-description text to the Ollama service running at `localhost` on your computer. The semantic model may be downloaded from an external model repository on first use. Do not assume that every part of the application is offline during initial setup.

## Future Improvements

- Expand the skill dictionary and support configurable skill categories.
- Add OCR for scanned resumes.
- Improve extraction of tables, columns, and complex resume layouts.
- Add tests for parsing, skill matching, scoring, and report generation.
- Add clearer handling for model-download and Ollama errors.
- Allow users to configure the scoring weights and explain how each score is calculated.
- Improve privacy controls and document-processing safeguards.

## Disclaimer

This project is intended as a resume-review aid. Its scores and recommendations should be treated as guidance, not as a hiring decision or a guarantee of interview selection.
