"""
Paquete src para clasificación multi-etiqueta de documentos.
"""

from .model import MultiLabelClassifier
from .document_handler import extract_text_from_file, extract_from_bytes
from .email_handler import EmailHandler

__all__ = [
    'MultiLabelClassifier',
    'extract_text_from_file',
    'extract_from_bytes',
    'EmailHandler'
]
