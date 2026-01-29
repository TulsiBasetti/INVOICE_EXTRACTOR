from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pypdf import PdfReader
import sys
import os
import json
from dotenv import load_dotenv


load_dotenv()


llm=ChatGroq(
    model='llama-3.3-70b-versatile',
    temperature=0
)

def text_extraction_from_pdf(pdf_path):
    reader=PdfReader(pdf_path)
    return reader.pages[0].extract_text()

system_prompt="""
You are a financial Invoice EXTRACTION ENGINE.

Rules:
-Extract factual data only.
-Donot explain anything.
-Do not add Comentary.
-output only in valid json format.
-use null if a field is missing.
"""

user_prompt_template="""
Extract structured data from the invoice text below.

Return JSON with the schema :

{{
    "invoice_number":string | null,
    "invoice_date": string | null,
    "vendor_name": string | null,
    "customer_name": string | null,
    "currency": string | null,
    "line_items": [
        {{  "product_name": string | null,
            "sub-category": string | null,
            "category": string | null,
            "product_id" : string | null,
            "quantity_or_duration": string | null,
            "rate": number | null,
            "amount": number | null
        }}
    ],

    "subtotal": number | null
    "discount": number | null
    "shipping": number | null
    "total": number | null
}}

Invoice Text:
{invoice_text}

"""
def extract_invoice(invoice_text):
    
    parser=JsonOutputParser()

    prompt=[
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt_template.format(invoice_text=invoice_text))
    ]
    
    chain=llm | parser

    return chain.invoke(prompt)

invoice_folder = r"C:\GenAI\LangChain\ASSIGNMENTS\INVOICE\invoice_dataset"  
output_folder = r"C:\GenAI\LangChain\ASSIGNMENTS\INVOICE\Invoices_JSON"  
os.makedirs(output_folder, exist_ok=True)

pdf_files = [f for f in os.listdir(invoice_folder) if f.lower().endswith(".pdf")]

for pdf_file in pdf_files:
    pdf_path = os.path.join(invoice_folder, pdf_file)
    invoice_text = text_extraction_from_pdf(pdf_path)
    invoice_data = extract_invoice(invoice_text)
    
    json_file = os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(invoice_data, f, indent=2)
    
    print(f"Processed {pdf_file} -> {json_file}")
    