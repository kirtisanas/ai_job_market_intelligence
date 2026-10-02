import pandas as pd

# Load skill demand results
df = pd.read_csv("data/data_analyst_skill_demand.csv")

# Total number of Data Analyst jobs
total_jobs = 408

# Calculate percentage of jobs mentioning each skill
df["percentage"] = (
    df["job_count"] / total_jobs * 100
).round(2)

# Sort by job count
df = df.sort_values(
    by="job_count",
    ascending=False
)

print("Skill Demand Analysis")
print("=" * 60)

print(df.to_string(index=False))

# Save enhanced results
df.to_csv(
    "data/data_analyst_skill_analysis.csv",
    index=False
)

print("\nSaved: data/data_analyst_skill_analysis.csv")