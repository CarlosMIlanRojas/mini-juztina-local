import fitz  # PyMuPDF
import re
import shutil
import os
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def extraer_texto_pdf(ruta_pdf):
    doc = fitz.open(ruta_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text("text") + "\n"
    return texto

def chunking_spij(texto, nombre_fuente):
    # 1. Recortar índices y exposiciones de motivos al inicio para no meter ruido
    if "CONSTITUCION" in nombre_fuente.upper():
        inicio = texto.find("PREAMBULO\nEl Congreso")
        fin = texto.find("LINK DE ACCESO AL CUADRO DE MODIFICACIONES")
        if inicio != -1: texto = texto[inicio:]
        if fin != -1: texto = texto[:fin]
    else:
        inicio = texto.find("TITULO PRELIMINAR\nPRINCIPIOS GENERALES")
        if inicio != -1: texto = texto[inicio:]

    lineas = [l.strip() for l in texto.split('\n') if l.strip()]
    
    documentos = []
    titulo_actual = "Título Preliminar / Preámbulo"
    capitulo_actual = "General"
    
    art_num_actual = None
    lineas_art_actual = []
    sumilla_pendiente = ""
    
    # Detectores exactos para el formato SPIJ
    re_titulo = re.compile(r"^(T[ÍI]TULO\s+(?:PRELIMINAR|[IVXLC]+(?:\-[A-Z])?))(?:\s*[:\.-]\s*(.*))?$", re.IGNORECASE)
    re_capitulo = re.compile(r"^(CAP[ÍI]TULO\s+(?:[IVXLC]+(?:\-[A-Z])?|ÚNICO|UNICO))(?:\s*[:\.-]\s*(.*))?$", re.IGNORECASE)
    re_articulo = re.compile(r"^[\"\“]?(Art[íi]culo\s+(?:\d+(?:\s*-\s*[A-ZÑ])?|[IVX]+)\s*[\.\°-]*)\s*(.*)", re.IGNORECASE)

    i = 0
    while i < len(lineas):
        linea = lineas[i]
        
        # Filtrar enlaces de jurisprudencia del SPIJ que ensucian el texto
        if linea in ["PROCESOS CONSTITUCIONALES", "CONCORDANCIA NORMATIVA"] or linea.startswith("JURISPRUDENCIA DE LA CORTE") or linea.startswith("CONCORDANCIAS"):
            i += 1
            continue
            
        # ¿Es un nuevo TÍTULO?
        m_tit = re_titulo.match(linea)
        if m_tit:
            subtitulo = m_tit.group(2)
            if not subtitulo and (i + 1) < len(lineas) and lineas[i+1].isupper() and not re_capitulo.match(lineas[i+1]) and not re_articulo.match(lineas[i+1]):
                titulo_actual = f"{m_tit.group(1)}: {lineas[i+1]}"
                i += 2
            else:
                titulo_actual = linea
                i += 1
            sumilla_pendiente = ""
            continue

        # ¿Es un nuevo CAPÍTULO?
        m_cap = re_capitulo.match(linea)
        if m_cap:
            subcap = m_cap.group(2)
            if not subcap and (i + 1) < len(lineas) and lineas[i+1].isupper() and not re_articulo.match(lineas[i+1]):
                capitulo_actual = f"{m_cap.group(1)}: {lineas[i+1]}"
                i += 2
            else:
                capitulo_actual = linea
                i += 1
            sumilla_pendiente = ""
            continue

        # ¿Es el inicio de un ARTÍCULO?
        m_art = re_articulo.match(linea)
        if m_art:
            identificador_raw = m_art.group(1)
            num_limpio = re.sub(r"[\.\°-]+$", "", identificador_raw).strip()
            
            # Si es el MISMO artículo (porque el SPIJ muestra una modificatoria abajo), lo mantenemos unido
            if art_num_actual and num_limpio.upper() == art_num_actual.upper():
                lineas_art_actual.append(linea)
            else:
                # Guardar el artículo anterior antes de empezar el nuevo
                if art_num_actual and lineas_art_actual:
                    documentos.append(Document(
                        page_content="\n".join(lineas_art_actual),
                        metadata={
                            "fuente": nombre_fuente,
                            "titulo": titulo_actual,
                            "capitulo": capitulo_actual,
                            "articulo": art_num_actual
                        }
                    ))
                art_num_actual = num_limpio
                lineas_art_actual = []
                if sumilla_pendiente:
                    lineas_art_actual.append(f"[{sumilla_pendiente}]")
                    sumilla_pendiente = ""
                lineas_art_actual.append(linea)
            i += 1
            continue

        # Mirar si esta línea corta es la sumilla (título) del artículo que viene en la siguiente línea
        if (i + 1) < len(lineas) and re_articulo.match(lineas[i+1]):
            if len(linea) < 120 and not linea.startswith("(*)"):
                sumilla_pendiente = linea
                i += 1
                continue

        # Agregar línea al cuerpo del artículo actual
        if art_num_actual:
            lineas_art_actual.append(linea)
        i += 1

    # Guardar el último artículo del documento
    if art_num_actual and lineas_art_actual:
        documentos.append(Document(
            page_content="\n".join(lineas_art_actual),
            metadata={
                "fuente": nombre_fuente,
                "titulo": titulo_actual,
                "capitulo": capitulo_actual,
                "articulo": art_num_actual
            }
        ))

    return documentos

# Borrar la carpeta anterior automáticamente para no duplicar datos viejos
if os.path.exists("./chroma_db_legal"):
    shutil.rmtree("./chroma_db_legal")

print("1. Leyendo PDFs oficiales del SPIJ...")
texto_const = extraer_texto_pdf("data/constitucion.pdf")
texto_penal = extraer_texto_pdf("data/codigo_penal.pdf")

print("2. Aplicando chunking estructurado (Títulos, Capítulos, Sumillas y Artículos)...")
docs_const = chunking_spij(texto_const, "Constitución Política del Perú")
docs_penal = chunking_spij(texto_penal, "Código Penal Peruano")
todos_los_docs = docs_const + docs_penal
print(f"   -> Artículos de la Constitución extraídos: {len(docs_const)}")
print(f"   -> Artículos del Código Penal extraídos: {len(docs_penal)}")
print(f"   -> Total de fragmentos en la base: {len(todos_los_docs)}")

print("3. Cargando modelo de embeddings local (HuggingFace)...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

print("4. Guardando Base de Datos Vectorial limpia en './chroma_db_legal'...")
vectorstore = Chroma.from_documents(
    documents=todos_los_docs,
    embedding=embeddings,
    persist_directory="./chroma_db_legal",
    collection_name="leyes_peru"
)
print("¡LISTO! Base de datos regenerada y optimizada.")

def obtener_retriever():
    """Carga la base de datos vectorial existente para hacer búsquedas."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={'device': 'cpu'}
    )
    vectorstore = Chroma(
        persist_directory="./chroma_db_legal",
        embedding_function=embeddings,
        collection_name="leyes_peru"
    )
    # Retorna el buscador configurado para traer los 4 artículos más relevantes
    return vectorstore.as_retriever(search_kwargs={"k": 12})