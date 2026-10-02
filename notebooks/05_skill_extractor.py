import pandas as pd
import re

# Load cleaned dataset
df = pd.read_csv("data/cleaned_postings.csv")

# Select Data Analyst jobs
data_analyst_jobs = df[
    df["title"].str.lower().str.contains(
        "data analyst",
        na=False
    )
].copy()

print("Data Analyst jobs:", len(data_analyst_jobs))


# Skills to detect
skills = [
    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "machine learning",
    "deep learning",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "statistics",
    "r",
    "mysql",
    "postgresql",
    "aws",
    "azure",
    "gcp",
    "git",
    "github",
    "docker",
    "kubernetes",
    "fastapi",
    "flask",
    "django",
    "java",
    "javascript",
    "c++",
    "c#",
    "html",
    "css",
    "react"
]


# Extract skills from a job description
def extract_skills(description):

    description = str(description).lower()

    found_skills = []

    for skill in skills:

        if skill in ["c++", "c#"]:
            pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        else:
            pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, description):
            found_skills.append(skill)

    return found_skills


# Count how many jobs mention each skill
skill_counts = {}

for skill in skills:
    skill_counts[skill] = 0


for description in data_analyst_jobs["description"]:

    extracted_skills = extract_skills(description)

    for skill in extracted_skills:
        skill_counts[skill] += 1


# Convert results to DataFrame
skill_df = pd.DataFrame(
    list(skill_counts.items()),
    columns=["skill", "job_count"]
)


# Sort from most requested to least requested
skill_df = skill_df.sort_values(
    by="job_count",
    ascending=False
)


# Remove skills that were not found
skill_df = skill_df[
    skill_df["job_count"] > 0
]


print("\nMost requested skills for Data Analyst jobs:\n")
print(skill_df.to_string(index=False))


# Save results
skill_df.to_csv(
    "data/data_analyst_skill_demand.csv",
    index=False
)

print("\nSaved: data/data_analyst_skill_demand.csv")