#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Práctica 04: Clasificación Multi-Etiqueta de Documentos

Sistema para clasificar documentos (sinopsis de películas) por género 
usando clasificación multi-etiqueta, con integración de email.

Uso:
    python main.py train                     # Entrenar modelo
    python main.py classify --text "..."     # Clasificar texto
    python main.py classify --file doc.txt   # Clasificar archivo
    python main.py email-daemon              # Iniciar servidor de email
"""

import argparse
import os
import sys

# Añadir directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.model import MultiLabelClassifier
from src.document_handler import extract_text_from_file
from src.email_handler import EmailHandler


# Rutas por defecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "documents.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "multilabel_classifier.pkl")


def train_model(args):
    """Entrena el modelo de clasificación."""
    print("=" * 50)
    print("ENTRENAMIENTO DEL MODELO MULTI-ETIQUETA")
    print("=" * 50)
    
    data_path = args.data or DATA_PATH
    model_path = args.output or MODEL_PATH
    
    print(f"\n📂 Datos: {data_path}")
    print(f"💾 Modelo: {model_path}")
    
    # Crear clasificador y entrenar
    classifier = MultiLabelClassifier()
    metrics = classifier.train(data_path, test_size=args.test_size)
    
    print("\n📊 MÉTRICAS DE EVALUACIÓN:")
    print("-" * 40)
    print(f"  Hamming Loss: {metrics['hamming_loss']:.4f} (menor es mejor)")
    print(f"  F1 Micro:     {metrics['f1_micro']:.4f}")
    print(f"  F1 Macro:     {metrics['f1_macro']:.4f}")
    print("\n📋 Reporte de Clasificación:")
    print(metrics['classification_report'])
    
    # Guardar modelo
    classifier.save(model_path)
    
    print("\n✅ Entrenamiento completado exitosamente!")


def classify_text(args):
    """Clasifica un texto o archivo."""
    print("=" * 50)
    print("CLASIFICACIÓN DE DOCUMENTO")
    print("=" * 50)
    
    model_path = args.model or MODEL_PATH
    
    # Cargar modelo
    if not os.path.exists(model_path):
        print(f"\n❌ Error: No se encontró el modelo en {model_path}")
        print("   Ejecute primero: python main.py train")
        return
    
    classifier = MultiLabelClassifier(model_path)
    
    # Obtener texto
    if args.text:
        text = args.text
        source = "Texto directo"
    elif args.file:
        if not os.path.exists(args.file):
            print(f"\n❌ Error: Archivo no encontrado: {args.file}")
            return
        text = extract_text_from_file(args.file)
        source = args.file
    else:
        print("\n❌ Error: Debe proporcionar --text o --file")
        return
    
    print(f"\n📄 Fuente: {source}")
    print(f"📝 Texto ({len(text)} caracteres):")
    print("-" * 40)
    print(text[:500] + ("..." if len(text) > 500 else ""))
    print("-" * 40)
    
    # Clasificar
    result = classifier.predict(text)
    
    print("\n🏷️ ETIQUETAS PREDICHAS:")
    if result['labels']:
        for label in result['labels']:
            print(f"   ✓ {label}")
    else:
        print("   (ninguna etiqueta detectada)")
    
    print("\n📊 PROBABILIDADES:")
    for label, prob in sorted(result['probabilities'].items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(prob * 20) + "░" * (20 - int(prob * 20))
        print(f"   {label:15} {bar} {prob:.1%}")
    
    print("\n✅ Clasificación completada!")


def run_email_daemon(args):
    """Ejecuta el servidor de email para clasificación automática."""
    print("=" * 50)
    print("SERVIDOR DE EMAIL - CLASIFICACIÓN AUTOMÁTICA")
    print("=" * 50)
    
    model_path = args.model or MODEL_PATH
    
    # Verificar modelo
    if not os.path.exists(model_path):
        print(f"\n❌ Error: No se encontró el modelo en {model_path}")
        print("   Ejecute primero: python main.py train")
        return
    
    # Verificar credenciales
    if not args.email or not args.password:
        print("\n❌ Error: Debe proporcionar --email y --password")
        print("\n💡 Para Gmail, use una 'Contraseña de aplicación':")
        print("   1. Vaya a https://myaccount.google.com/apppasswords")
        print("   2. Genere una contraseña para 'Correo'")
        print("   3. Use esa contraseña con este script")
        return
    
    # Cargar modelo
    classifier = MultiLabelClassifier(model_path)
    
    # Configurar handler de email
    handler = EmailHandler(
        email_address=args.email,
        password=args.password,
        imap_server=args.imap_server,
        smtp_server=args.smtp_server
    )
    handler.set_classifier(classifier)
    
    print(f"\n📧 Email: {args.email}")
    print(f"🖥️ IMAP: {args.imap_server}")
    print(f"📤 SMTP: {args.smtp_server}")
    print(f"⏱️ Intervalo: {args.interval}s")
    
    print("\n📨 Envíe un email con un documento adjunto (.txt, .pdf, .docx)")
    print("   a esta dirección para recibir la clasificación automática.\n")
    
    # Ejecutar daemon
    handler.run_daemon(check_interval=args.interval)


def main():
    parser = argparse.ArgumentParser(
        description="Sistema de Clasificación Multi-Etiqueta de Documentos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main.py train
  python main.py classify --text "Un robot viaja en el tiempo..."
  python main.py classify --file documento.txt
  python main.py email-daemon --email tu@gmail.com --password contraseña
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando: train
    train_parser = subparsers.add_parser('train', help='Entrenar modelo')
    train_parser.add_argument('--data', help='Ruta al dataset CSV')
    train_parser.add_argument('--output', help='Ruta para guardar el modelo')
    train_parser.add_argument('--test-size', type=float, default=0.2, 
                              help='Proporción de datos para test (default: 0.2)')
    
    # Comando: classify
    classify_parser = subparsers.add_parser('classify', help='Clasificar documento')
    classify_parser.add_argument('--text', help='Texto a clasificar')
    classify_parser.add_argument('--file', help='Archivo a clasificar (.txt, .pdf, .docx)')
    classify_parser.add_argument('--model', help='Ruta al modelo entrenado')
    
    # Comando: email-daemon
    email_parser = subparsers.add_parser('email-daemon', help='Servidor de email')
    email_parser.add_argument('--email', required=True, help='Dirección de email')
    email_parser.add_argument('--password', required=True, help='Contraseña de email')
    email_parser.add_argument('--imap-server', default='imap.gmail.com', help='Servidor IMAP')
    email_parser.add_argument('--smtp-server', default='smtp.gmail.com', help='Servidor SMTP')
    email_parser.add_argument('--interval', type=int, default=60, help='Intervalo de revisión (seg)')
    email_parser.add_argument('--model', help='Ruta al modelo entrenado')
    
    args = parser.parse_args()
    
    if args.command == 'train':
        train_model(args)
    elif args.command == 'classify':
        classify_text(args)
    elif args.command == 'email-daemon':
        run_email_daemon(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
