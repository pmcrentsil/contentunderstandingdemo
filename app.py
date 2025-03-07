import requests
import time
import json
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    credential, "https://cognitiveservices.azure.com/.default")

# Set up the endpoint and subscription key from Azure
# Keep this as your Content Understanding endpoint
endpoint = "https://aihubdemowestu3982015250.services.ai.azure.com/"

analyzer_id = "recipe_analyzer"  # The ID of the analyzer to create

# The URL for the doc intell API call (document URL endpoint)
# Correct API path for Content Understanding
create_analyzer_url = endpoint + \
    f"contentunderstanding/analyzers/{analyzer_id}?api-version=2024-12-01-preview"

# Example document URL or file data (update with your file or URL)
headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {token_provider()}"
}

# Load the request body from a JSON file
with open('analyzer_template.json', 'r') as file:
    data = json.load(file)

# Delete the analyzer if it already exists
# response = requests.delete(create_analyzer_url, headers=headers)

# Make the PUT request to the Content Understanding API
response = requests.put(create_analyzer_url, headers=headers, json=data)

if response.status_code == 201:
    print("Created Content Understanding analyzer successfully.")
    print("Operation-Location: ", response.headers["Operation-Location"])
else:
    print(
        f"Failed to create Content Understanding analyzer. Status code: {response.status_code}")
    print(response.text)

run_analyzer_url = endpoint + \
    f"contentunderstanding/analyzers/{analyzer_id}:analyze?api-version=2024-12-01-preview"

# Document URL (replace with the actual document URL or use a SAS URL if needed)
recipe_file = {
    # Replace with your document URL
    "url": "https://cooking.blob.core.windows.net/cooking/cooking.pdf"
}

# Make the POST request to the Form Recognizer API
response = requests.post(
    run_analyzer_url, headers=headers, json=recipe_file, timeout=30)

# Check if the request was successful
if response.status_code == 202:
    print("Request successful, processing started.")

    # Get the operation-location URL for polling
    result_url = response.headers["Operation-Location"]

    # Polling for the result
    while True:
        result_response = requests.get(result_url, headers=headers)
        if result_response.status_code == 200:
            analysis_result = result_response.json()
            print("Analysis Result: ")
            print(json.dumps(analysis_result, indent=2))
            break  # Once results are received, exit the loop
        else:
            print(
                f"Waiting for results... Status code: {result_response.status_code}")
            time.sleep(5)  # Wait 5 seconds before polling again
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)


#
# TODO: Poll and wait for the analysis to be completed before retrieving the results
#
result_id = json.loads(response.text)["id"]
results_url = endpoint + \
    f"contentunderstanding/analyzers/{analyzer_id}/results/{result_id}?api-version=2024-12-01-preview"

# Make the GET request to the Content Understanding API
response = requests.get(results_url, headers=headers, timeout=30)
print(response.text)
