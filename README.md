# Content Understanding with Azure Document Intelligence (Form Recognizer)

## Project Overview

This project leverages **Azure's Content Understanding** services to analyze documents and extract valuable insights using **Document Intelligence** (formerly known as **Form Recognizer**). The solution integrates multiple services such as **Text Analytics**, **Document Intelligence**, and **Bing Search** for processing a wide range of content types, with a focus on document analysis, invoices, and other related tasks.

The use case is aligned with Rashed’s approach of creating a **"tour guide"** for documents, processing them through a **Bing search**, and using **personal notes** for a tailored user experience. In this scenario, the system analyzes documents (such as PDFs or images) and extracts structured data that can be used for various business applications.

## Objective

The goal is to create a system that:
- Analyzes documents using **Document Intelligence** (formerly Form Recognizer).
- Extracts structured data (fields like names, dates, and amounts).
- Integrates **Bing Search** to retrieve relevant data or context for documents.
- Provides personalized notes or narrative generation based on the document content.

This can be used in various domains, such as invoice processing, automated data extraction from documents, and even generating insights or reports based on the content.

## Technologies Used

- **Azure Cognitive Services** (Content Understanding, Document Intelligence)
- **Bing Search API**
- **Flask** for exposing the API
- **Python Requests** for making API calls
- **JSON** for response handling

## Solution Architecture

1. **Document Intelligence**:
   - The **Document Intelligence** (formerly **Form Recognizer**) API is used to analyze documents (such as invoices, receipts, and forms) and extract structured data like fields, tables, and text.
   - A **prebuilt model** like **`prebuilt-invoice`** is used for invoice documents, while **custom models** can be used for specialized document types.
   
2. **Bing Search API**:
   - The **Bing Search API** helps provide additional context by searching for related content on the web based on document keywords.
   
3. **Personal Notes and Narrative Generation**:
   - A **personalized note generation system** provides an interface for the user to interact with the data, add notes, and generate tailored narratives.
   
4. **Azure Blob Storage**:
   - Documents are hosted on **Azure Blob Storage**, and the system pulls the document from the provided URL to analyze it using Document Intelligence.

## Endpoints and API Integration

1. **Document Intelligence API Endpoint**:
   - **Endpoint URL**: `https://<your-resource-name>.cognitiveservices.azure.com/`
   - **API Path**: `/formrecognizer/documentModels/prebuilt-invoice/analyze?api-version=2023-02-28-preview`
   - This API processes the document URL provided in the request body and returns the analysis results.

2. **Bing Search API**:
   - **Endpoint URL**: `https://api.bing.microsoft.com/v7.0/search`
   - **Usage**: Used to retrieve web search results for terms identified in the document content, providing context for the user.

3. **Personal Notes API**:
   - This allows users to add custom notes or generate a narrative based on the document analysis.

---

This change ensures that the document reflects **Document Intelligence** instead of **Form Recognizer**.

Let me know if you'd like further revisions!
