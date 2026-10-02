import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/cleaned_postings.csv")

# Skills we want to detect
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
    "java",
    "javascript",
    "c++",
    "c#",
    "html",
    "css",
    "react",
    "fastapi",
    "flask",
    "django",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "git",
    "github"
]

# Convert descriptions to lowercase
descriptions = df["description"].fillna("").str.lower()

skill_counts = {}

for skill in skills:
    count = descriptions.str.contains(skill, regex=False).sum()
    skill_counts[skill] = count

# Convert to DataFrame
skill_df = pd.DataFrame(
    list(skill_counts.items()),
    columns=["skill", "job_count"]
)

# Sort by demand
skill_df = skill_df.sort_values(
    by="job_count",
    ascending=False
)

print("\nMost requested skills:")
print(skill_df.to_string(index=False))