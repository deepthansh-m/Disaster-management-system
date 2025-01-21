import pandas as pd

# Path to your existing CSV file
input_csv = r'C:\Users\Asus\Desktop\disaster-management-system\backend\ml\data\raw\disaster_historical_data.csv'
output_csv = r'C:\Users\Asus\Desktop\disaster-management-system\backend\ml\data\raw\disaster_historical_data_updated.csv'

# Load the CSV
df = pd.read_csv(input_csv)

# Add 'rainfall' and 'temperature' with default values (e.g., 0.0)
df['rainfall'] = 0.0
df['temperature'] = 0.0

# Add 'disaster_occurred' column. Since all entries are disasters, set to 1
df['disaster_occurred'] = 1

# Optional: Rename 'Latitude' and 'Longitude' to lowercase if needed
df.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'}, inplace=True)

# Save the updated CSV
df.to_csv(output_csv, index=False)

print(f"Updated CSV saved as {output_csv}")