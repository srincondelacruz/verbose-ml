"""
Módulo de modelo de clasificación multi-etiqueta.
Usa TF-IDF + OneVsRestClassifier para clasificación de géneros de películas.
"""

import os
import re
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, hamming_loss, f1_score
import nltk
from nltk.corpus import stopwords

# Descargar stopwords en español si no están disponibles
try:
    stopwords.words('spanish')
except LookupError:
    nltk.download('stopwords', quiet=True)


class MultiLabelClassifier:
    """Clasificador multi-etiqueta para documentos de texto."""
    
    # Etiquetas de géneros
    LABELS = ['action', 'comedy', 'drama', 'horror', 'scifi', 'romance', 'animation', 'thriller']
    LABEL_NAMES = {
        'action': 'Acción',
        'comedy': 'Comedia', 
        'drama': 'Drama',
        'horror': 'Terror',
        'scifi': 'Ciencia Ficción',
        'romance': 'Romance',
        'animation': 'Animación',
        'thriller': 'Thriller'
    }
    
    def __init__(self, model_path: str = None):
        """
        Inicializa el clasificador.
        
        Args:
            model_path: Ruta opcional para cargar un modelo existente
        """
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words=self._get_stopwords()
        )
        self.classifier = OneVsRestClassifier(
            LogisticRegression(max_iter=1000, random_state=42)
        )
        self.is_fitted = False
        
        if model_path and os.path.exists(model_path):
            self.load(model_path)
    
    def _get_stopwords(self) -> list:
        """Obtiene stopwords en español."""
        try:
            return stopwords.words('spanish')
        except:
            return []
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocesa el texto para clasificación.
        
        Args:
            text: Texto a preprocesar
            
        Returns:
            Texto limpio
        """
        # Convertir a minúsculas
        text = text.lower()
        # Eliminar caracteres especiales y números
        text = re.sub(r'[^a-záéíóúñü\s]', '', text)
        # Eliminar espacios múltiples
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def train(self, data_path: str, test_size: float = 0.2) -> dict:
        """
        Entrena el modelo con los datos proporcionados.
        
        Args:
            data_path: Ruta al archivo CSV con los datos
            test_size: Proporción de datos para test
            
        Returns:
            Diccionario con métricas de evaluación
        """
        # Cargar datos
        df = pd.read_csv(data_path)
        
        # Preprocesar texto
        texts = df['text'].apply(self._preprocess_text).tolist()
        
        # Obtener etiquetas
        y = df[self.LABELS].values
        
        # Dividir en train/test
        X_train, X_test, y_train, y_test = train_test_split(
            texts, y, test_size=test_size, random_state=42
        )
        
        # Vectorizar
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        
        # Entrenar
        self.classifier.fit(X_train_tfidf, y_train)
        self.is_fitted = True
        
        # Evaluar
        y_pred = self.classifier.predict(X_test_tfidf)
        
        metrics = {
            'hamming_loss': hamming_loss(y_test, y_pred),
            'f1_micro': f1_score(y_test, y_pred, average='micro'),
            'f1_macro': f1_score(y_test, y_pred, average='macro'),
            'classification_report': classification_report(
                y_test, y_pred, target_names=self.LABELS, zero_division=0
            )
        }
        
        return metrics
    
    # Palabras clave por género para boost
    KEYWORDS = {
        'horror': ['terror', 'asesino', 'matar', 'muerte', 'muerto', 'sangre', 'demonio', 
                   'fantasma', 'posesion', 'maldicion', 'horror', 'miedo', 'aterroriza',
                   'payaso', 'monstruo', 'pesadilla', 'sobrenatural', 'oscuro', 'maligno'],
        'action': ['lucha', 'pelea', 'explosion', 'armas', 'disparos', 'persecucion',
                   'heroe', 'villano', 'batalla', 'guerra', 'combate', 'venganza'],
        'comedy': ['risa', 'divertido', 'comico', 'humor', 'parodia', 'gracioso'],
        'drama': ['tragedia', 'familiar', 'conflicto', 'emocional', 'vida', 'muerte'],
        'scifi': ['robot', 'futuro', 'espacio', 'alien', 'nave', 'tecnologia', 'ciencia'],
        'romance': ['amor', 'enamorar', 'romance', 'pareja', 'beso', 'corazon'],
        'animation': ['animacion', 'animado', 'dibujos', 'pixar', 'disney'],
        'thriller': ['suspenso', 'tension', 'misterio', 'investigacion', 'crimen']
    }
    
    def predict(self, text: str) -> dict:
        """
        Predice las etiquetas para un texto.
        
        Args:
            text: Texto a clasificar
            
        Returns:
            Diccionario con etiquetas y probabilidades
        """
        if not self.is_fitted:
            raise ValueError("El modelo no ha sido entrenado. Ejecute train() primero.")
        
        # Preprocesar
        processed_text = self._preprocess_text(text)
        
        # Vectorizar
        X = self.vectorizer.transform([processed_text])
        
        # Predecir probabilidades del modelo ML
        probabilities = self.classifier.predict_proba(X)[0]
        
        # Aplicar boost por palabras clave
        boosted_probs = list(probabilities)
        for i, label in enumerate(self.LABELS):
            keyword_count = sum(1 for kw in self.KEYWORDS.get(label, []) if kw in processed_text)
            if keyword_count > 0:
                # Boost: +20% por cada palabra clave encontrada
                boost = min(keyword_count * 0.20, 0.5)  # Máximo 50% boost
                boosted_probs[i] = min(boosted_probs[i] + boost, 1.0)
        
        # Formatear resultado
        result = {
            'labels': [],
            'probabilities': {}
        }
        
        # Umbral dinámico
        THRESHOLD = 0.30
        
        for i, label in enumerate(self.LABELS):
            prob = float(boosted_probs[i])
            result['probabilities'][self.LABEL_NAMES[label]] = round(prob, 3)
            
            if prob >= THRESHOLD:
                result['labels'].append(self.LABEL_NAMES[label])
        
        return result
    
    def save(self, path: str):
        """
        Guarda el modelo entrenado.
        
        Args:
            path: Ruta donde guardar el modelo
        """
        if not self.is_fitted:
            raise ValueError("El modelo no ha sido entrenado.")
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        model_data = {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier
        }
        joblib.dump(model_data, path)
        print(f"Modelo guardado en: {path}")
    
    def load(self, path: str):
        """
        Carga un modelo entrenado.
        
        Args:
            path: Ruta del modelo a cargar
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el modelo en: {path}")
        
        model_data = joblib.load(path)
        self.vectorizer = model_data['vectorizer']
        self.classifier = model_data['classifier']
        self.is_fitted = True
        print(f"Modelo cargado desde: {path}")


if __name__ == "__main__":
    # Ejemplo de uso
    import os
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "documents.csv")
    model_path = os.path.join(base_dir, "models", "multilabel_classifier.pkl")
    
    # Crear y entrenar modelo
    classifier = MultiLabelClassifier()
    metrics = classifier.train(data_path)
    
    print("\n=== Métricas de Entrenamiento ===")
    print(f"Hamming Loss: {metrics['hamming_loss']:.4f}")
    print(f"F1 Micro: {metrics['f1_micro']:.4f}")
    print(f"F1 Macro: {metrics['f1_macro']:.4f}")
    print(f"\n{metrics['classification_report']}")
    
    # Guardar modelo
    classifier.save(model_path)
    
    # Probar predicción
    test_text = "Un robot del futuro viaja en el tiempo para salvar a la humanidad de las máquinas"
    result = classifier.predict(test_text)
    print(f"\nTexto: {test_text}")
    print(f"Etiquetas predichas: {result['labels']}")
    print(f"Probabilidades: {result['probabilities']}")
