import requests
import json
import pandas as pd

# API Endpoint
url = "https://apithunder.makecontact.space/SearchRecord"

# API Key
CS_API_KEY = "1abnshqn1rmv243kbuq6i5bq6xyfdexpx58un5kc6qllp"  # Replace with your actual API key

# Headers
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "x-api-key": CS_API_KEY
}

# API Parameters
payload = {
    "datasetid": "26170",  # Replace with actual dataset ID
    "initiativeid": "1764",  # Include if required
    "jsondata": '{}',  # No filter
    "activeonly": "true"
}

# Send API Request
response = requests.post(url, headers=headers, data=payload)

# Print raw response for debugging
print("Raw API Response:", response.text)

if response.status_code == 200:
    try:
        data = response.json()
        print("Parsed JSON Response:", json.dumps(data, indent=4))  # Pretty-print JSON

        if "info" in data:
            records = data["info"]

            if isinstance(records, list) and len(records) > 0:
                df = pd.DataFrame(records)
                output_file = r"C:\Users\Omniuser\Downloads\output.xlsx"
                df.to_excel(output_file, index=False)
                print(f"File downloaded successfully and saved as: {output_file}")
            else:
                print("Warning: 'info' exists but is empty or not a list.")
        else:
            print("Error: 'info' key is missing in API response.")

    except json.JSONDecodeError:
        print("Error: API did not return valid JSON.")
else:
    print(f"HTTP Error {response.status_code}: {response.text}")
