import pandas as pd

# Load categorized skill data
df = pd.read_csv("data/role_skill_categories.csv")

# --------------------------------------------------
# 1. Skill demand by role
# --------------------------------------------------

role_skill = df[
    [
        "role",
        "skill",
        "job_count",
        "percentage",
        "category"
    ]
].copy()

role_skill.to_csv(
    "data/powerbi_role_skill.csv",
    index=False
)


# --------------------------------------------------
# 2. Category demand by role
# --------------------------------------------------

category_summary = (
    df.groupby(
        ["role", "category"],
        as_index=False
    )["job_count"]
    .sum()
)

category_summary = category_summary.sort_values(
    ["role", "job_count"],
    ascending=[True, False]
)

category_summary.to_csv(
    "data/powerbi_category_demand.csv",
    index=False
)


# --------------------------------------------------
# 3. Overall skill demand
# --------------------------------------------------

overall_skill = (
    df.groupby(
        ["skill", "category"],
        as_index=False
    )["job_count"]
    .sum()
)

overall_skill = overall_skill.sort_values(
    "job_count",
    ascending=False
)

overall_skill.to_csv(
    "data/powerbi_overall_skills.csv",
    index=False
)


# --------------------------------------------------
# Print results
# --------------------------------------------------

print("\nDashboard Data Created")
print("=" * 60)

print("\nSkill demand by role:")
print(role_skill.head(15).to_string(index=False))

print("\nCategory demand by role:")
print(category_summary.to_string(index=False))

print("\nOverall skill demand:")
print(overall_skill.head(15).to_string(index=False))


print("\nFiles created:")
print("1. data/powerbi_role_skill.csv")
print("2. data/powerbi_category_demand.csv")
print("3. data/powerbi_overall_skills.csv")