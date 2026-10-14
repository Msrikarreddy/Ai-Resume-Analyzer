
from semantic_matcher import calculate_semantic_similarity

resume = """
Python developer with experience in data analysis,
Pandas, SQL, and machine learning projects.
"""

job_description = """
We need a candidate who can analyze datasets,
write SQL queries, and develop predictive models
using Python.
"""

score = calculate_semantic_similarity(
    resume,
    job_description
)

print(f"Semantic similarity: {score}%")