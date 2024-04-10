import pandas as pd
import glob

# Get a list of all CSV files in the directory
csv_files = glob.glob('*.csv')

# Create an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Iterate over each CSV file and merge it with the existing data
for file in csv_files:
    data = pd.read_csv(file)
    merged_data = pd.concat([merged_data, data])

# Save the merged data to a new CSV file
merged_data.to_csv('merged.csv', index=False)