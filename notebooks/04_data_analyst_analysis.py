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
    "statistics",
    "r",
    "mysql",
    "postgresql",
    "aws",
    "azure",
    "git"
]

# Convert descriptions to lowercase
descriptions = (
    data_analyst_jobs["description"]
    .fillna("")
    .str.lower()
)

# Count skill mentions
skill_counts = {}

for skill in skills:
    # Word boundary prevents false matches
    # Example: "r" will match R as a separate word,
    # but not the letter r inside other words.
    pattern = r"\b" + re.escape(skill) + r"\b"

    count = descriptions.str.contains(
        pattern,
        regex=True
    ).sum()

    skill_counts[skill] = count

# Convert results to DataFrame
skill_df = pd.DataFrame(
    list(skill_counts.items()),
    columns=["skill", "job_count"]
)

# Sort by demand
skill_df = skill_df.sort_values(
    by="job_count",
    ascending=False
)

print("\nMost requested skills for Data Analyst jobs:")
print(skill_df.to_string(index=False))