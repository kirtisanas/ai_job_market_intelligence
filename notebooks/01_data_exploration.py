import pandas as pd

# Load job postings dataset
df = pd.read_csv("data/postings.csv")

# Show basic information
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate job IDs:")
print(df["job_id"].duplicated().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())