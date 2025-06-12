import fitz  # PyMuPDF
import re
import os
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\\'
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import io

# Si usas Windows y Tesseract no está en PATH, descomenta y edita esta línea:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 🔍 OCR para extraer texto desde la imagen de la página PDF
def extraer_texto_ocr(page):
    pix = page.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return pytesseract.image_to_string(img, lang='spa')

# 🛑 Redacta RUTs menores a 35.000.000 (con o sin puntos)
def redactar_ruts(texto, page):
    rut_regex = r'(\d{1,2}\.?\d{3}\.?\d{3}-[\dkK])'
    ruts = re.findall(rut_regex, texto)
    for rut in ruts:
        numero = int(rut.replace(".", "").split("-")[0])
        if numero < 35000000:
            for area in page.search_for(rut):
                page.add_redact_annot(area, fill=(0, 0, 0))
                print(f"✓ RUT redactado: {rut}")

# 🛑 Redacta correos electrónicos
def redactar_correos(texto, page):
    correos = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", texto)
    for correo in correos:
        for area in page.search_for(correo):
            page.add_redact_annot(area, fill=(0, 0, 0))
            print(f"✓ Correo redactado: {correo}")

# 🛑 Redacta direcciones con patrón simple
def redactar_direcciones(texto, page):
    patrones = [
        r"\b(?:Calle|Pasaje|Av\.?|Avenida)\s+[^\n,;]+",  # Búsqueda básica
    ]
    for patron in patrones:
        matches = re.findall(patron, texto, re.IGNORECASE)
        for match in matches:
            for area in page.search_for(match.strip()):
                page.add_redact_annot(area, fill=(0, 0, 0))
                print(f"✓ Dirección redactada: {match.strip()}")

# 🧠 Función principal
def procesar_pdf_escaneado(ruta_entrada, ruta_salida):
    doc = fitz.open(ruta_entrada)
    for i, page in enumerate(doc):
        print(f"\n📄 Procesando página {i+1}")
        texto = extraer_texto_ocr(page)
        redactar_ruts(texto, page)
        redactar_correos(texto, page)
        redactar_direcciones(texto, page)
        page.apply_redactions()
    doc.save(ruta_salida)
    doc.close()
    print(f"\n✅ Listo: {ruta_salida}")

# 📁 Rutas reales proporcionadas por el usuario
carpeta_entrada = r"C:\Users\sofia\Desktop\RedactorPDF\entrada_pdfs"
carpeta_salida = r"C:\Users\sofia\Desktop\RedactorPDF\salida_pdfs"

# 🔄 Procesar todos los PDFs en la carpeta
def procesar_todos_los_pdfs():
    for archivo in os.listdir(carpeta_entrada):
        if archivo.lower().endswith(".pdf"):
            entrada = os.path.join(carpeta_entrada, archivo)
            salida = os.path.join(carpeta_salida, f"REDACTADO_{archivo}")
            procesar_pdf_escaneado(entrada, salida)

# 🚀 Ejecutar
if __name__ == "__main__":
    procesar_todos_los_pdfs()
