# Práctica 04: Clasificación Multi-Etiqueta de Documentos

Sistema para clasificar documentos (sinopsis de películas) por género usando clasificación multi-etiqueta con TF-IDF + LogisticRegression, e integración con email para clasificación automática.

## Estructura del Proyecto

```
practica_04-Etiquetar-documentos/
├── data/
│   └── documents.csv          # Dataset de 50 sinopsis de películas
├── models/
│   └── multilabel_classifier.pkl  # Modelo entrenado (se genera)
├── src/
│   ├── __init__.py
│   ├── model.py               # Clasificador multi-etiqueta
│   ├── document_handler.py    # Extracción de texto de archivos
│   └── email_handler.py       # Integración con email
├── main.py                    # CLI principal
├── requirements.txt           # Dependencias
└── README.md
```

## Instalación

```bash
cd practica_04-Etiquetar-documentos
pip install -r requirements.txt
```

## Uso

### 1. Entrenar el modelo

```bash
python main.py train
```

### 2. Clasificar un texto

```bash
python main.py classify --text "Un robot del futuro viaja en el tiempo para salvar a la humanidad"
```

### 3. Clasificar un archivo

```bash
python main.py classify --file documento.txt
```

### 4. Servidor de email (clasificación automática)

```bash
python main.py email-daemon --email tu@gmail.com --password TU_CONTRASEÑA_DE_APP
```

> **Nota**: Para Gmail, necesitas una [contraseña de aplicación](https://myaccount.google.com/apppasswords)

## Etiquetas

El modelo clasifica documentos en 8 géneros:

| Etiqueta | Descripción |
|----------|-------------|
| Acción | Películas con escenas de acción, peleas, persecuciones |
| Comedia | Películas humorísticas |
| Drama | Películas con conflictos emocionales profundos |
| Terror | Películas de miedo, suspenso sobrenatural |
| Ciencia Ficción | Películas con tecnología futurista, viajes espaciales |
| Romance | Películas con historias de amor |
| Animación | Películas animadas |
| Thriller | Películas de suspenso, tensión psicológica |

## Flujo de Email

1. Envía un email con un documento adjunto (.txt, .pdf, .docx) a la dirección configurada
2. El sistema extrae el texto del documento
3. Clasifica el documento usando el modelo
4. Responde automáticamente con las etiquetas predichas y probabilidades

## Métricas del Modelo

- **Hamming Loss**: Mide la fracción de etiquetas incorrectas
- **F1 Micro**: Promedio ponderado por instancia
- **F1 Macro**: Promedio no ponderado por clase
