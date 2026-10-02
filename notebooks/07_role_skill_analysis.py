import pandas as pd
import re

# Load cleaned dataset
df = pd.read_csv("data/cleaned_postings.csv")

# Roles we want to analyze
roles = {
    "Data Analyst": "data analyst",
    "Data Scientist": "data scientist",
    "Software Engineer": "software engineer"
}

# Skills to analyze
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


# Skill extraction function
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


# Store results
all_results = []


# Analyze each role
for role_name, keyword in roles.items():

    role_jobs = df[
        df["title"].str.lower().str.contains(
            keyword,
            na=False
        )
    ].copy()

    print("\n" + "=" * 60)
    print(role_name)
    print("Number of jobs:", len(role_jobs))
    print("=" * 60)

    skill_counts = {}

    for skill in skills:
        skill_counts[skill] = 0

    # Analyze every job description
    for description in role_jobs["description"]:

        extracted_skills = extract_skills(description)

        for skill in extracted_skills:
            skill_counts[skill] += 1

    # Save results
    for skill, count in skill_counts.items():

        if count > 0:

            percentage = round(
                (count / len(role_jobs)) * 100,
                2
            )

            all_results.append({
                "role": role_name,
                "skill": skill,
                "job_count": count,
                "percentage": percentage
            })

            print(
                f"{skill:20} "
                f"{count:5} jobs "
                f"({percentage}%)"
            )


# Convert to DataFrame
results_df = pd.DataFrame(all_results)

# Save results
results_df.to_csv(
    "data/role_skill_analysis.csv",
    index=False
)

print("\nSaved: data/role_skill_analysis.csv")