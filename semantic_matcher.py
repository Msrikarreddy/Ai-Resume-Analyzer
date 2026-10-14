
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the model once and reuse it.
_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return _model


def calculate_semantic_similarity(
    resume_text,
    job_description
):
    """Compare the meaning of two documents."""

    model = get_model()

    embeddings = model.encode(
        [resume_text, job_description],
        normalize_embeddings=True
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(float(similarity) * 100, 2)