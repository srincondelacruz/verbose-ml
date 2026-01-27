"""
Módulo para manejo de documentos.
Extrae texto de archivos .txt, .pdf, .docx
"""

import os
from typing import Optional


def extract_text_from_file(file_path: str) -> str:
    """
    Extrae texto de un archivo según su extensión.
    
    Args:
        file_path: Ruta al archivo
        
    Returns:
        Texto extraído del archivo
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.txt':
        return extract_from_txt(file_path)
    elif ext == '.pdf':
        return extract_from_pdf(file_path)
    elif ext == '.docx':
        return extract_from_docx(file_path)
    else:
        raise ValueError(f"Extensión no soportada: {ext}. Use .txt, .pdf o .docx")


def extract_from_txt(file_path: str) -> str:
    """Extrae texto de un archivo .txt"""
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    raise ValueError(f"No se pudo decodificar el archivo: {file_path}")


def extract_from_pdf(file_path: str) -> str:
    """Extrae texto de un archivo .pdf"""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError("Instale PyPDF2: pip install PyPDF2")
    
    reader = PdfReader(file_path)
    text = ""
    
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    
    return text.strip()


def extract_from_docx(file_path: str) -> str:
    """Extrae texto de un archivo .docx"""
    try:
        from docx import Document
    except ImportError:
        raise ImportError("Instale python-docx: pip install python-docx")
    
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def extract_from_bytes(content: bytes, filename: str) -> str:
    """
    Extrae texto de contenido en bytes (para adjuntos de email).
    
    Args:
        content: Contenido del archivo en bytes
        filename: Nombre del archivo para determinar el tipo
        
    Returns:
        Texto extraído
    """
    import tempfile
    
    ext = os.path.splitext(filename)[1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        text = extract_text_from_file(tmp_path)
    finally:
        os.unlink(tmp_path)
    
    return text
