import os
import pypdf
import pandas as pd

def read_document(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".txt":
        return read_txt(filepath)
    elif ext == ".pdf":
        return read_pdf(filepath)
    elif ext == ".csv":
        return read_csv(filepath)
    elif ext in [".xlsx", ".xls"]:
        return read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def read_txt(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def read_pdf(filepath: str) -> str:
    text = ""
    with open(filepath, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def read_csv(filepath: str) -> str:
    df = pd.read_csv(filepath)
    return df.to_string(index=False)

def read_excel(filepath: str) -> str:
    text = ""
    excel_file = pd.ExcelFile(filepath)
    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        text += f"\n--- Sheet: {sheet_name} ---\n"
        text += df.to_string(index=False)
    return text