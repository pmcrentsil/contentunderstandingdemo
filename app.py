import requests
import time
import json

# Set up the endpoint and subscription key from Azure
endpoint = "https://contentservices.services.ai.azure.com/"  # Keep this as your Content Understanding endpoint
subscription_key = "DfO8IZa5iAgpOg2MBWILdeK73c2zRJLiObuneHIlaUu9gxoDUisdJQQJ99BCACYeBjFXJ3w3AAAAACOG8ozL"  # Replace with your actual subscription key

# The URL for the doc intell API call (document URL endpoint)
url = endpoint + "formrecognizer/documentModels/prebuilt-invoice/analyze?api-version=2023-02-28-preview"  # Correct API path for Form Recognizer

# Example document URL or file data (update with your file or URL)
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key
}

# Document URL (replace with the actual document URL or use a SAS URL if needed)
data = {
   "urlSource": "https://cooking.blob.core.windows.net/cooking/cooking.pdf"  # Replace with your document URL
}

# Make the POST request to the Form Recognizer API
response = requests.post(url, headers=headers, json=data)

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
            print(f"Waiting for results... Status code: {result_response.status_code}")
            time.sleep(5)  # Wait 5 seconds before polling again
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
