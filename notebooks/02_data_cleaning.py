import pandas as pd

# Load original dataset
df = pd.read_csv("data/postings.csv")

print("Original rows:", len(df))

# Keep the columns useful for our project
columns_to_keep = [
    "job_id",
    "company_name",
    "title",
    "description",
    "location",
    "formatted_experience_level",
    "skills_desc",
    "formatted_work_type",
    "work_type",
    "remote_allowed",
    "min_salary",
    "max_salary",
    "currency",
    "listed_time"
]

df = df[columns_to_keep]

# Remove rows where important information is missing
df = df.dropna(subset=["title", "description", "location"])

# Remove duplicate job IDs
df = df.drop_duplicates(subset=["job_id"])

# Fill missing text fields
df["company_name"] = df["company_name"].fillna("Unknown")
df["formatted_experience_level"] = df["formatted_experience_level"].fillna("Not Specified")
df["skills_desc"] = df["skills_desc"].fillna("")

# Save cleaned dataset
df.to_csv("data/cleaned_postings.csv", index=False)

print("Cleaned rows:", len(df))
print("Cleaned columns:", len(df.columns))
print("Saved: data/cleaned_postings.csv")
print("\nTop 20 job titles:")
print(df["title"].value_counts().head(20))

# Find technology-related jobs
tech_keywords = [
    "data analyst",
    "data scientist",
    "machine learning",
    "software engineer",
    "software developer",
    "python developer",
    "sql",
    "ai engineer",
    "artificial intelligence"
]

tech_jobs = df[
    df["title"].str.lower().str.contains(
        "|".join(tech_keywords),
        na=False
    )
]

print("\nTechnology-related jobs:", len(tech_jobs))

print("\nTop technology job titles:")
print(tech_jobs["title"].value_counts().head(20))