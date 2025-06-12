import fitz  # PyMuPDF
import re
import os

# === LISTAS NORMALIZADAS ===
afps = [
    "AFP Modelo", "Modelo", "AFP MODELO",
    "AFP Habitat", "Habitat", "AFP HABITAT",
    "AFP Capital", "Capital", "AFP CAPITAL",
    "AFP Cuprum", "Cuprum", "AFP CUPRUM",
    "AFP Provida", "Provida", "AFP PROVIDA",
    "AFP PlanVital", "PlanVital", "Plan Vital", "AFP PLAN VITAL",
    "AFP Uno", "AFP UNO", "Uno", "AFPUNO", "AFP UNO S.A.",
    "AFP", "HABITAT", "MODELO", "CAPITAL", "CUPRUM", "PROVIDA", "PLAN VITAL", "AFP PLAN VITAL"
]

saludes = [
    "ISAPRE Banmédica", "ISAPRE Banmedica","BANMEDICA",
    "ISAPRE Colmena","COLMENA", 
    "ISAPRE Consalud","CONSALUD", 
    "ISAPRE Cruz Blanca", "ISAPRE CruzBlanca", "ISAPRE Cruz-Blanca","CRUZ BLANCA",
    "ISAPRE Nueva Mas Vida", "ISAPRE nueva mas vida","NUEVA MAS VIDA",
    "ISAPRE Vida Tres", "ISAPRE Vidatres","VIDA TRES",
    "FONASA", "Fonasa", "FONASA.",
    "ISAPRE"
]

def normalizar_texto(texto):
    texto = texto.lower()
    texto = texto.replace('\n', ' ').replace('\r', ' ')
    texto = re.sub(r'[áàäâ]', 'a', texto)
    texto = re.sub(r'[éèëê]', 'e', texto)
    texto = re.sub(r'[íìïî]', 'i', texto)
    texto = re.sub(r'[óòöô]', 'o', texto)
    texto = re.sub(r'[úùüû]', 'u', texto)
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()


def redactar_dato_despues_de(page, frase_clave, lista_valores):
    texto = page.get_text()
    texto_normalizado = normalizar_texto(texto)
    frase_clave_norm = normalizar_texto(frase_clave)

    # Buscar posición de la frase clave en texto normalizado
    matches = list(re.finditer(frase_clave_norm, texto_normalizado, re.IGNORECASE))

    for match in matches:
        # Tomar todo el texto después de la frase clave
        texto_post_norm = texto_normalizado[match.end():]

        for valor in lista_valores:
            valor_norm = normalizar_texto(valor)
            if valor_norm in texto_post_norm:
                # Buscar en el texto original el valor (sin normalizar)
                cuadros = page.search_for(valor)
                if cuadros:
                    print(f"🔒 Redactando valor: {valor}")
                    for cuadro in cuadros:
                        page.add_redact_annot(cuadro, fill=(0, 0, 0))
                    break

"""def redactar_valores_directos(page, lista_valores):
    texto = page.get_text()
    for valor in lista_valores:
        patron = re.compile(re.escape(valor), re.IGNORECASE)
        for match in patron.finditer(texto):
            encontrado = match.group(0)
            # Buscar exactamente cómo está escrito en el PDF
            rects = page.search_for(encontrado)
            for rect in rects:
                page.add_redact_annot(rect, fill=(0, 0, 0))"""

# Redactar RUT solo si viene después de "cédula de identidad N°"
def redactar_rut(page, doc, page_index):
    texto = page.get_text("text")

    # Buscar RUTs con y sin puntos
    ruts = re.findall(r"\b\d{1,2}\.?\d{3}\.?\d{3}-[0-9kK]\b|\b\d{7,8}-[0-9kK]\b", texto)

    redactados = set()

    for rut in ruts:
        # Eliminar puntos del rut para evaluar
        rut_sin_puntos = rut.replace(".", "")
        numero_str = rut_sin_puntos.split('-')[0]

        try:
            numero = int(numero_str)
        except ValueError:
            continue

        if numero <= 35000000:
            if rut not in redactados:
                print(f"Redactando RUT: {rut}")
                cuadros = page.search_for(rut)
                for rect in cuadros:
                    page.add_redact_annot(rect, fill=(0, 0, 0))
                redactados.add(rut)
    page.apply_redactions()
""" def redactar_rut(page, doc, page_index):
    texto = page.get_text("text")
    ruts = re.findall(r"\b\d{7,8}-[0-9kK]\b", texto)
    for rut in ruts:
        numero_str = rut.split('-')[0]
        try:
            numero = int(numero_str)
        except ValueError:
            continue
        if numero <= 35000000:
            print(f"Redactando RUT en página {page_index + 1}: {rut}")
            cuadros = page.search_for(rut)
            for rect in cuadros:
                page.add_redact_annot(rect, fill=(0,0,0))
    page.apply_redactions()

    # Si no es última página, aplica búsqueda usual después de frase clave
    lineas = texto.splitlines()
    for i, linea in enumerate(lineas):
        if "cédula de identidad n°" in linea.lower():
            for linea_sgte in lineas[i:]:
                ruts_en_linea = re.findall(r"\b\d{7,8}-[0-9kK]\b", linea_sgte)
                for rut in ruts_en_linea:
                    numero_str = rut.split('-')[0]
                    try:
                        numero = int(numero_str)
                    except ValueError:
                        continue
                    if numero <= 35000000:
                        print(f"Redactando RUT: {rut}")
                        cuadros = page.search_for(rut)
                        for rect in cuadros:
                            page.add_redact_annot(rect, fill=(0, 0, 0))
            break
    page.apply_redactions() """



# Redactar correos electrónicos
def redactar_correos(page):
    texto = page.get_text("text")
    correos = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", texto)
    for correo in correos:
        print(f"Redactando correo: {correo}")
        cuadros = page.search_for(correo)
        for rect in cuadros:
            page.add_redact_annot(rect, fill=(0,0,0))
    page.apply_redactions()

def redactar_bloque(page, bbox):
    page.add_redact_annot(bbox, fill=(0, 0, 0))
    page.apply_redactions()


def redactar_domicilios(page):
    # Obtener todo el texto de la página (un solo string)
    texto_pagina = page.get_text()

    # Buscar desde "domiciliad" hasta "correo electrónico" (inclusivo)
    patron = re.compile(r'domiciliad[ao]?/?[ao]?.*?correo\s+electr[oó]nico', re.IGNORECASE | re.DOTALL)
    coincidencia = patron.search(texto_pagina)

    if not coincidencia:
        print("⚠️ No se encontró domicilio para redactar en esta página.")
        return

    texto_domicilio = coincidencia.group(0).strip()
    print(f"\n✅ Texto domicilio detectado para redactar:\n{texto_domicilio}\n")

    # Buscar posiciones exactas del texto domicilio en la página
    rects = page.search_for(texto_domicilio)

    if not rects:
        print("⚠️ No se encontró el texto domicilio en las posiciones del PDF.")
        return

    # Añadir anotaciones de redacción SOLO sobre los rectángulos exactos
    for rect in rects:
        page.add_redact_annot(rect, fill=(0, 0, 0))  # negro

    # Aplicar redacciones en la página
    page.apply_redactions()


# Procesar cada PDF
def redactar_pdf(ruta_entrada, ruta_salida):
    doc = fitz.open(ruta_entrada)
    for i, page in enumerate(doc):
        redactar_rut(page, doc, i)
        redactar_correos(page)
        redactar_domicilios(page)  
        redactar_dato_despues_de(page, "afiliado a", afps)
        redactar_dato_despues_de(page, "SALUD a", saludes)
        page.apply_redactions()
    doc.save(ruta_salida)
    

# Procesar todos los PDFs en la carpeta
def procesar_pdfs(directorio_entrada, directorio_salida):
    for archivo in os.listdir(directorio_entrada):
        if archivo.lower().endswith(".pdf"):
            ruta_entrada = os.path.join(directorio_entrada, archivo)
            ruta_salida = os.path.join(directorio_salida, archivo)
            redactar_pdf(ruta_entrada, ruta_salida)

# Ejecutar
if __name__ == "__main__":
    entrada = "entrada_pdfs"
    salida = "salida_pdfs"
    procesar_pdfs(entrada, salida)
