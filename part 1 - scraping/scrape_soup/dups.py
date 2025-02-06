import pandas as pd

# Read the CSV file
df = pd.read_csv('academic_ranking_world_universities.csv')

# Drop duplicate rows
df = df.drop_duplicates()

# Save the deduplicated data back to CSV
df.to_csv('academic_ranking_world_universities.csv', index=False)

print(f"Removed {len(df) - len(df.drop_duplicates())} duplicate rows")
