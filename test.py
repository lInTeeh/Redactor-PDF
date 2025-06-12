import os

pdfinfo_path = r"C:\poppler-24.08.0\Library\bin\pdfinfo.exe"

if os.path.exists(pdfinfo_path):
    print("✅ pdfinfo.exe existe")
else:
    print("❌ pdfinfo.exe NO se encontró")


"""import pytesseract
import os
from pdf2image import convert_from_path
from PIL import Image

pdf_path = r'C:\Users\sofia\Desktop\RedactorPDF\entrada_pdfs\ALARCON MARIA COMPAÑIA.pdf'
poppler_path = r'C:\poppler-24.08.0\Library\bin'


# 🖼 Convertimos cada página a imagen
pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)

# 🔧 Ruta a tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 🔧 Ruta base a tessdata (sin \tessdata al final)
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\\'

# 📄 Ruta del PDF a procesar
pdf_path = r'C:\Users\sofia\Desktop\RedactorPDF\entrada_pdfs\ALARCON MARIA COMPAÑIA.pdf'

# 🔍 Procesamos cada página
for i, page in enumerate(pages):
    text = pytesseract.image_to_string(page, lang='spa')
    print(f'\n--- Página {i + 1} ---\n')
    print(text)
"""
