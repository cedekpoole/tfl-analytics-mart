import json
import os
import requests
from datetime import datetime

# The TfL API endpoint for London Underground tube line statuses (Good Service, Minor Delays, etc.)
url = "https://api.tfl.gov.uk/Line/Mode/tube/Status"

# Make a GET request to the API and wait up to 30 seconds for a response
response = requests.get(url, timeout=30)

# If the API returned an error (e.g. 404, 500), this will raise an exception and stop the script
response.raise_for_status()

# Convert the raw API response
data = response.json()

# Build a filename using the current date and time so each file is unique
# e.g. "tfl_lines_2026-06-20_14-30-00.json"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"tfl_lines_{timestamp}.json"

# Set the folder path where the file will be saved
output_dir = "data/raw/tfl"

# Create the folder if it doesn't already exist (safe to run even if it does exist)
os.makedirs(output_dir, exist_ok=True)

# Join the folder path and filename into a full file path
# e.g. "data/raw/tfl/tfl_lines_2026-06-20_14-30-00.json"
output_path = os.path.join(output_dir, filename)

# Open the file for writing and save the data as formatted JSON
with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

# Print a confirmation message so you know it worked
print(f"Saved {len(data)} lines to {output_path}")
