from docx2pdf import convert

def docx2pdf(docx_path: str, pdf_path: str):
    convert(docx_path, pdf_path)