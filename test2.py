import os
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR"

import pytesseract
from PIL import Image

img = Image.new("RGB", (200, 100), color="white")
text = pytesseract.image_to_string(img, lang="spa")
print(text)