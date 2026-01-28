# Invoice Extraction using LLM

## Description
This project extracts structured data from invoice PDF files using a Large Language Model (LLM).

The script reads invoice PDFs, extracts text using PyPDF, converts the text into structured JSON using ChatGroq, and saves the output as JSON files.


## Extracted Fields
- Invoice Number  
- Invoice Date  
- Vendor Name  
- Customer Name  
- Currency  
- Line Items (description, quantity, rate, amount)  
- Subtotal  
- Discount  
- Shipping  
- Total

Missing values are stored as `null`.

### Output

Each invoice PDF generates one JSON file.

## How It Works
- PyPDF extracts raw text from the invoice
- ChatGroq (LLM) converts unstructured text into structured JSON
