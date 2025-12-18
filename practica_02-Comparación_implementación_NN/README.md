# Práctica 02: Comparación de Implementación de Redes Neuronales

## 🎯 Objetivo

Comparar el comportamiento entre redes neuronales **supervisadas** y **no supervisadas**, utilizando:
- Implementaciones propias (algoritmos desde cero)
- Librerías de redes neuronales (TensorFlow/Keras, scikit-learn)

## 📊 Datasets

1. **Datos Meteorológicos**: Mediciones de regiones de Sudamérica (NASA Power)
2. **MNIST**: Dígitos manuscritos (0-9)

## 📁 Estructura del Proyecto

```
practica_02-Comparación_implementación_NN/
├── data/
│   ├── raw/                    # Datos originales
│   │   ├── weather/            # Datos meteorológicos
│   │   └── mnist/              # Datos MNIST
│   └── processed/              # Datos preprocesados
├── src/
│   ├── custom/                 # Implementaciones propias
│   │   ├── mlp.py              # Red multicapa con backprop
│   │   ├── som.py              # Self-Organizing Map
│   │   └── autoencoder.py      # Autoencoder
│   ├── library_based/          # Implementaciones con librerías
│   │   ├── keras_models.py     # Modelos TensorFlow/Keras
│   │   └── sklearn_models.py   # Modelos scikit-learn
│   ├── utils/                  # Utilidades
│   │   ├── data_loader.py      # Carga de datos
│   │   ├── preprocessing.py    # Preprocesamiento
│   │   └── visualization.py    # Gráficos
│   └── cli.py                  # Aplicación de consola
├── notebooks/                  # Jupyter notebooks exploratorios
├── results/                    # Resultados y gráficos
├── requirements.txt            # Dependencias
└── README.md                   # Este archivo
```

## 🚀 Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 📖 Uso

```bash
# Ejecutar aplicación de consola
python src/cli.py
```

## 👤 Autor

Sergio Rincón de la Cruz
Álvaro López
Ángel Toledo
Iñigo Jiménez

