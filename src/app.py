import os
from pathlib import Path
import sys
import logging
import requests
import time
import json
import uuid
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from content_understanding.content_understanding_client import AzureContentUnderstandingClient

logging.basicConfig(level=logging.INFO)
# The URL and Version for the Content Understanding API
AZURE_AI_ENDPOINT = "https://aihubdemowestu3982015250.services.ai.azure.com/"
AZURE_AI_API_VERSION = "2024-12-01-preview"


def create_analyzer(cu_client, analyzer_id, analyzer_template_path):
    # Creates a new Content Understanding analyzer
    return cu_client.begin_create_analyzer(
        analyzer_id=analyzer_id,
        analyzer_template_path=analyzer_template_path)


def run_analyzer(cu_client, analyzer_id, file_location):
    # Analyzes the document using the specified analyzer
    # exits the program if the call to analyze operation fails
    try:
        analyze_file = cu_client.begin_analyze(
            analyzer_id=analyzer_id,
            file_location=file_location)
    except Exception as e:
        logging.error("Failed to analyze the document. Error message:\n %s", e)
        cu_client.delete_analyzer(analyzer_id=analyzer_id)
        sys.exit(1)
    return analyze_file


def main():
    # The ID of the analyzer to create
    ANALYZER_ID = "recipe_analyzer-" + str(uuid.uuid4().hex[:8])

    # Path of the analyzer template file in absolute path
    ANALYZER_TEMPLATE_PATH = Path(
        "src/analyzer_templates/recipes.json").resolve()

    # Document URL (replace with the actual document URL or use a SAS URL if needed)
    RECIPE_FILE = "https://cooking.blob.core.windows.net/cooking/cooking.pdf"

    # Get Azure bearer token for Azure AI services
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

    logging.info("Analyzer template path: %s", ANALYZER_TEMPLATE_PATH)

    cu_client = AzureContentUnderstandingClient(
        endpoint=AZURE_AI_ENDPOINT,
        api_version=AZURE_AI_API_VERSION,
        token_provider=token_provider,)

    analyzer = create_analyzer(
        cu_client, ANALYZER_ID, ANALYZER_TEMPLATE_PATH)

    result = cu_client.poll_result(analyzer)

    if result is not None and "status" in result and result["status"] == "Succeeded":
        logging.info(
            "Analyzer '%s' created successfully with the properties:", result['result']['analyzerId'])
        logging.info(json.dumps(result, indent=2))
    else:
        logging.info(
            "Failed to create the analyzer. Please check the error message below:")
        logging.error(json.dumps(result, indent=2))

    analyze_file = run_analyzer(cu_client, ANALYZER_ID, RECIPE_FILE)
    result = cu_client.poll_result(analyze_file)

    logging.info("Status of the analyze operation: %s", result["status"])
    logging.info("Analyze operation completed with the result:")
    logging.info(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
