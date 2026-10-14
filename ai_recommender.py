
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def generate_ai_recommendations(resume_text, job_description):
    prompt = f"""
You are an expert resume improvement assistant.

Analyze the resume against the job description.

Provide:
1. The candidate's strengths supported by the resume.
2. Important job requirements without clear resume evidence.
3. Three specific resume improvement suggestions.
4. One improved resume bullet using only facts in the resume.

Rules:
- Never invent skills, qualifications, or achievements.
- Distinguish missing evidence from missing skills.
- Be concise and professional.

RESUME:
{resume_text[:2500]}

JOB DESCRIPTION:
{job_description[:2000]}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2}
            },
            timeout=600
        )

        response.raise_for_status()
        return response.json().get(
            "response",
            "No recommendations were generated."
        ).strip()

    except requests.exceptions.ConnectionError:
        return (
            "Ollama is not running. Start Ollama and try again."
        )

    except requests.exceptions.Timeout:
        return (
            "The AI model took too long to respond. "
            "Try again with shorter text."
        )

    except requests.exceptions.RequestException as error:
        return f"AI recommendation error: {error}"