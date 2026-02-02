import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ingestion.loaders import DataLoader
from ingestion.pdf_processor import PDFProcessor
from analysis.llm_client import LocalLLMClient

def main():
    print("=== Credit Admission Analysis System ===")
    
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    credit_app_path = os.path.join(data_dir, 'solicitud_credito.xlsx')
    macro_data_path = os.path.join(data_dir, 'datos_macro.xlsx')
    report_pdf_path = os.path.join(data_dir, 'reporte_empresa.pdf') # Fixed: was looking for .pdf
    
    # 1. Ingestion
    print("\n[1/3] Ingesting Data...")
    
    # Load Credit App
    if os.path.exists(credit_app_path):
        credit_data = DataLoader.load_credit_application(credit_app_path)
        print(f"Loaded Credit Application: {len(credit_data)} fields")
    else:
        print(f"Error: {credit_app_path} not found.")
        return

    # Load Macro Data
    if os.path.exists(macro_data_path):
        macro_text = DataLoader.load_macro_data(macro_data_path)
        print("Loaded Macro Data")
    else:
        print(f"Error: {macro_data_path} not found.")
        return

    # Load PDF Report
    if os.path.exists(report_pdf_path):
        company_report_text = PDFProcessor.extract_text_from_pdf(report_pdf_path)
        print(f"Loaded Company Report ({len(company_report_text)} chars)")
    else:
        print(f"Error: {report_pdf_path} not found.")
        return

    # Simulated Credit Bureau Score (Hardcoded as per plan or could be inputs)
    bureau_score = 680
    print(f"Bureau Score: {bureau_score}")

    # 2. Prompt Construction
    print("\n[2/3] Constructing Analysis Prompt...")
    
    prompt = f"""
    # Credit Admission Request Analysis

    ## 1. Applicant Profile
    {credit_data}

    ## 2. Bureau Score
    Score: {bureau_score} (Scale: 300-850, >650 is generally good)

    ## 3. Macroeconomic Context
    {macro_text}

    ## 4. Company Annual Report Summary
    {company_report_text[:2000]}... (truncated if too long)

    ## Task
    Analyze the above information to determine if the credit should be approved.
    
    Please provide:
    1. **Executive Summary**: Brief overview of the risk.
    2. **Key Strengths**: Simulation of positive factors.
    3. **Key Risks**: Negative factors.
    4. **Recommendation**: APPROVE, DENY, or CONDITIONALLY APPROVE.
    5. **Conditions (if applicable)**.

    Output format: Markdown.
    """

    # 3. LLM Analysis
    print("\n[3/3] Running LLM Analysis (Local)...")
    # Note: Ensure you have a local LLM running (e.g. Ollama)
    # Defaulting to model 'llama3', change in code if needed.
    llm = LocalLLMClient(model="llama3") 
    
    try:
        report = llm.analyze_credit(prompt)
        
        print("\n" + "="*40)
        print("ANALYSIS REPORT")
        print("="*40 + "\n")
        print(report)
        
        # Save report
        reporting_dir = os.path.join(os.path.dirname(__file__), 'src', 'reporting')
        if not os.path.exists(reporting_dir):
            os.makedirs(reporting_dir)
            
        report_path = os.path.join(reporting_dir, 'credit_report.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport saved to '{report_path}'")
        
    except Exception as e:
        print(f"Analysis failed: {e}")
        print("Ensure that your local LLM server is running (e.g., 'ollama serve' and 'ollama pull llama3')")

if __name__ == "__main__":
    main()
