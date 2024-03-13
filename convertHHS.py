import pandas as pd

# Path to your CSV file
csv_file_path = '/home/kdefoe/Desktop/breach-report.csv'  # Update this path to your actual CSV file location

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Convert the DataFrame to a JSON file
# This uses the 'records' orientation to create a list of records in the JSON file
json_output_path = '/home/kdefoe/Desktop/breach-report.json'  # Specify your desired output JSON file name

df.to_json(json_output_path, orient='records', indent=4)

print(f"JSON file created at {json_output_path}")
