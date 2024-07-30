import io
from PIL import Image
from apis.utils.convert_file import docx2pdf

def get_image_file(object_content: bytes, file_name: str):
    image_content = Image.open(io.BytesIO(object_content))
    file_path = f'tmp/{file_name}'
    image_content.save(file_path)
    return file_path

def get_pdf_file(object_content:bytes, file_name: str):
    file_path = f'tmp/{file_name}'
    with open(file_path, 'wb') as f:
        f.write(object_content)
    return file_path

def get_docx_file(object_content:bytes, file_name: str):
    docx_file_path = f'tmp/{file_name}'
    with open(docx_file_path, 'wb') as f:
        f.write(object_content)

    pdf_file_path = f'tmp/{file_name.rsplit(".", 1)[0]}.pdf'
    docx2pdf(docx_file_path, pdf_file_path)
    file_path = pdf_file_path
    return file_path, docx_file_path
