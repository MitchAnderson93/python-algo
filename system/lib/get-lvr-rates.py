import os
import sys

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from system.common import raw_path, fitz, re, pd, csv, requests

def download_pdf(url, output_path):
    response = requests.get(url)
    with open(output_path, 'wb') as f:
        f.write(response.content)

def extract_text_from_all_pages(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Extract text from all pages
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text += page.get_text("text")
    
    return text

def parse_text_to_dataframe(text):
    # Define a regex pattern to match the rows
    pattern = re.compile(r'(\w+)\s+([A-Z\s]+)\s+(\d+%)\s+(\d+%)\s+(\d+%)')
    
    # Find all matches
    matches = pattern.findall(text)
    
    # Create a DataFrame from the matches
    df = pd.DataFrame(matches, columns=["code", "name", "portfolio_lvr", "standard_lvr", "single_lvr"])
    
    # Extract numeric values from the percentage strings
    df["portfolio_lvr"] = df["portfolio_lvr"].str.rstrip('%')
    df["standard_lvr"] = df["standard_lvr"].str.rstrip('%')
    df["single_lvr"] = df["single_lvr"].str.rstrip('%')
    
    return df

def main():
    url = "https://www.commsec.com.au/content/dam/EN/PDFs/Product/Margin-Lending/Accepted_Shares.pdf"
    pdf_path = os.path.join(raw_path, "Accepted_Shares.pdf")
    
    # Download the PDF file
    download_pdf(url, pdf_path)
    
    # Extract text from all pages of the PDF
    text = extract_text_from_all_pages(pdf_path)
    
    # Parse the text to a DataFrame
    df = parse_text_to_dataframe(text)
    
    # Save the DataFrame to a CSV file with all fields wrapped in double quotes
    df.to_csv(os.path.join(raw_path, "lvr.csv"), index=False, quoting=csv.QUOTE_ALL)
    
    print("Data extracted and saved to auto-lvr.csv")

if __name__ == "__main__":
    main()