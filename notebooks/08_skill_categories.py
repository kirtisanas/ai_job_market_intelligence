import pandas as pd

# Load role skill analysis
df = pd.read_csv("data/role_skill_analysis.csv")


# Skill categories
skill_categories = {

    "Programming": [
        "python",
        "java",
        "javascript",
        "c++",
        "c#",
        "r"
    ],

    "Data & Analytics": [
        "sql",
        "excel",
        "power bi",
        "tableau",
        "pandas",
        "numpy",
        "statistics"
    ],

    "Machine Learning": [
        "machine learning",
        "deep learning",
        "scikit-learn",
        "tensorflow",
        "pytorch"
    ],

    "Cloud": [
        "aws",
        "azure",
        "gcp"
    ],

    "DevOps": [
        "git",
        "github",
        "docker",
        "kubernetes"
    ],

    "Databases": [
        "mysql",
        "postgresql"
    ],

    "Web Development": [
        "html",
        "css",
        "react",
        "fastapi",
        "flask",
        "django"
    ]
}


# Create reverse mapping:
# skill -> category

skill_to_category = {}

for category, skill_list in skill_categories.items():

    for skill in skill_list:
        skill_to_category[skill] = category


# Add category column
df["category"] = df["skill"].map(skill_to_category)


# Display results
print("\nSkill Category Analysis")
print("=" * 60)

print(df.to_string(index=False))


# Save categorized data
df.to_csv(
    "data/role_skill_categories.csv",
    index=False
)

print("\nSaved: data/role_skill_categories.csv")