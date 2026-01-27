"""
Módulo para integración con email.
Permite recibir documentos por email y responder con su clasificación.
"""

import imaplib
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import decode_header
import os
from typing import List, Dict, Optional, Tuple

from .model import MultiLabelClassifier
from .document_handler import extract_from_bytes


class EmailHandler:
    """Manejador de emails para clasificación de documentos."""
    
    # Extensiones de archivo soportadas
    SUPPORTED_EXTENSIONS = ['.txt', '.pdf', '.docx']
    
    def __init__(
        self,
        email_address: str,
        password: str,
        imap_server: str = "imap.gmail.com",
        smtp_server: str = "smtp.gmail.com",
        imap_port: int = 993,
        smtp_port: int = 587
    ):
        """
        Inicializa el manejador de email.
        
        Args:
            email_address: Dirección de email
            password: Contraseña o contraseña de aplicación
            imap_server: Servidor IMAP
            smtp_server: Servidor SMTP
            imap_port: Puerto IMAP
            smtp_port: Puerto SMTP
        """
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.smtp_server = smtp_server
        self.imap_port = imap_port
        self.smtp_port = smtp_port
        
        self.imap_connection = None
        self.classifier = None
    
    def set_classifier(self, classifier: MultiLabelClassifier):
        """Establece el clasificador a usar."""
        self.classifier = classifier
    
    def connect_imap(self):
        """Conecta al servidor IMAP."""
        self.imap_connection = imaplib.IMAP4_SSL(
            self.imap_server, 
            self.imap_port
        )
        self.imap_connection.login(self.email_address, self.password)
        print(f"Conectado a IMAP: {self.imap_server}")
    
    def disconnect_imap(self):
        """Desconecta del servidor IMAP."""
        if self.imap_connection:
            self.imap_connection.logout()
            self.imap_connection = None
            print("Desconectado de IMAP")
    
    def _decode_header_value(self, value: str) -> str:
        """Decodifica un valor de cabecera de email."""
        if value is None:
            return ""
        
        decoded_parts = decode_header(value)
        result = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                result += part.decode(encoding or 'utf-8', errors='ignore')
            else:
                result += part
        
        return result
    
    def get_unread_emails_with_attachments(self) -> List[Dict]:
        """
        Obtiene emails no leídos con adjuntos soportados.
        
        Returns:
            Lista de diccionarios con información del email y adjuntos
        """
        if not self.imap_connection:
            self.connect_imap()
        
        self.imap_connection.select('INBOX')
        
        # Buscar emails no leídos
        status, messages = self.imap_connection.search(None, 'UNSEEN')
        
        if status != 'OK':
            return []
        
        email_ids = messages[0].split()
        emails_with_attachments = []
        
        for email_id in email_ids:
            status, msg_data = self.imap_connection.fetch(email_id, '(RFC822)')
            
            if status != 'OK':
                continue
            
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extraer información
            from_addr = self._decode_header_value(msg.get('From'))
            subject = self._decode_header_value(msg.get('Subject'))
            
            # Buscar adjuntos
            attachments = []
            
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                
                filename = part.get_filename()
                if filename:
                    filename = self._decode_header_value(filename)
                    ext = os.path.splitext(filename)[1].lower()
                    
                    if ext in self.SUPPORTED_EXTENSIONS:
                        attachments.append({
                            'filename': filename,
                            'content': part.get_payload(decode=True)
                        })
            
            if attachments:
                emails_with_attachments.append({
                    'id': email_id,
                    'from': from_addr,
                    'subject': subject,
                    'attachments': attachments
                })
        
        return emails_with_attachments
    
    def process_and_reply(self, email_data: Dict) -> bool:
        """
        Procesa un email, clasifica los documentos y responde.
        
        Args:
            email_data: Datos del email con adjuntos
            
        Returns:
            True si se procesó correctamente
        """
        if not self.classifier:
            raise ValueError("No se ha establecido un clasificador")
        
        results = []
        
        for attachment in email_data['attachments']:
            try:
                # Extraer texto
                text = extract_from_bytes(
                    attachment['content'],
                    attachment['filename']
                )
                
                # Clasificar
                prediction = self.classifier.predict(text)
                
                results.append({
                    'filename': attachment['filename'],
                    'labels': prediction['labels'],
                    'probabilities': prediction['probabilities'],
                    'text_preview': text[:200] + "..." if len(text) > 200 else text
                })
            except Exception as e:
                results.append({
                    'filename': attachment['filename'],
                    'error': str(e)
                })
        
        # Crear y enviar respuesta
        reply_body = self._format_reply(results)
        self._send_reply(email_data['from'], email_data['subject'], reply_body)
        
        return True
    
    def _format_reply(self, results: List[Dict]) -> str:
        """Formatea los resultados de clasificación para el email de respuesta."""
        body = "=== RESULTADOS DE CLASIFICACIÓN ===\n\n"
        
        for result in results:
            body += f"📄 Archivo: {result['filename']}\n"
            body += "-" * 40 + "\n"
            
            if 'error' in result:
                body += f"❌ Error: {result['error']}\n"
            else:
                if result['labels']:
                    body += f"🏷️ Etiquetas: {', '.join(result['labels'])}\n"
                else:
                    body += "🏷️ Etiquetas: (ninguna detectada)\n"
                
                body += "\n📊 Probabilidades:\n"
                for label, prob in sorted(
                    result['probabilities'].items(),
                    key=lambda x: x[1],
                    reverse=True
                ):
                    bar = "█" * int(prob * 10) + "░" * (10 - int(prob * 10))
                    body += f"   {label}: {bar} {prob:.1%}\n"
                
                body += f"\n📝 Vista previa:\n{result['text_preview']}\n"
            
            body += "\n" + "=" * 40 + "\n\n"
        
        body += "\n🤖 Clasificación automática usando modelo multi-etiqueta\n"
        body += "Práctica 04 - Machine Learning\n"
        
        return body
    
    def _send_reply(self, to_addr: str, original_subject: str, body: str):
        """Envía un email de respuesta."""
        # Extraer solo la dirección de email
        if '<' in to_addr:
            to_addr = to_addr.split('<')[1].split('>')[0]
        
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = to_addr
        msg['Subject'] = f"Re: {original_subject} - Clasificación de Documentos"
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email_address, self.password)
            server.send_message(msg)
        
        print(f"Respuesta enviada a: {to_addr}")
    
    def run_daemon(self, check_interval: int = 60):
        """
        Ejecuta el manejador como demonio, revisando emails periódicamente.
        
        Args:
            check_interval: Intervalo en segundos entre revisiones
        """
        import time
        
        print(f"Iniciando demonio de email (revisar cada {check_interval}s)")
        print("Presione Ctrl+C para detener\n")
        
        try:
            while True:
                print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Revisando emails...")
                
                try:
                    emails = self.get_unread_emails_with_attachments()
                    
                    if emails:
                        print(f"Encontrados {len(emails)} emails con adjuntos")
                        
                        for email_data in emails:
                            print(f"  Procesando: {email_data['subject']}")
                            self.process_and_reply(email_data)
                    else:
                        print("No hay emails nuevos con adjuntos")
                        
                except Exception as e:
                    print(f"Error: {e}")
                    # Reconectar si hay error de conexión
                    self.disconnect_imap()
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\nDeteniendo demonio...")
            self.disconnect_imap()


if __name__ == "__main__":
    print("Este módulo debe usarse a través de main.py")
    print("Ejemplo: python main.py email-daemon --email tu@gmail.com --password contraseña")
