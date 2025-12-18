"""
preprocessing.py - Preprocesamiento de datos

¿POR QUÉ PREPROCESAR?
Los datos "crudos" raramente están listos para redes neuronales:
1. Diferentes escalas: temperatura vs presión vs humedad
2. Valores faltantes
3. Outliers (valores extremos)

Sin preprocesamiento, la red puede:
- Dar más importancia a variables con valores grandes
- No converger durante el entrenamiento
- Producir resultados inconsistentes
"""

import numpy as np


class StandardScaler:
    """
    Estandarización: transforma datos para tener media=0 y std=1
    
    Fórmula: z = (x - μ) / σ
    
    ¿POR QUÉ ESTANDARIZAR?
    - Todas las variables quedan en la misma escala
    - Los gradientes fluyen mejor durante backpropagation
    - La red aprende más rápido
    
    Esta es una implementación propia para entender qué hace
    sklearn.preprocessing.StandardScaler
    """
    
    def __init__(self):
        self.mean_ = None
        self.std_ = None
        self.is_fitted = False
    
    def fit(self, X):
        """
        Calcula media y desviación estándar de X.
        
        ¿Por qué fit separado de transform?
        - fit: aprende los parámetros del conjunto de entrenamiento
        - transform: aplica esos parámetros
        
        IMPORTANTE: Solo hacemos fit con datos de entrenamiento,
        nunca con datos de test. ¿Por qué? Para simular que no
        conocemos el futuro (los datos de test representan datos nuevos).
        """
        X = np.array(X)
        self.mean_ = np.mean(X, axis=0)
        self.std_ = np.std(X, axis=0)
        
        # Evitar división por cero
        self.std_[self.std_ == 0] = 1.0
        
        self.is_fitted = True
        return self
    
    def transform(self, X):
        """Aplica la estandarización."""
        if not self.is_fitted:
            raise ValueError("Debes llamar a fit() primero")
        
        X = np.array(X)
        return (X - self.mean_) / self.std_
    
    def fit_transform(self, X):
        """Fit y transform en un solo paso (conveniencia)."""
        return self.fit(X).transform(X)
    
    def inverse_transform(self, X_scaled):
        """
        Deshace la estandarización.
        
        Útil para interpretar predicciones:
        - El modelo predice en escala estandarizada
        - Invertimos para obtener valores reales (ej: temperatura en °C)
        """
        if not self.is_fitted:
            raise ValueError("Debes llamar a fit() primero")
        
        X_scaled = np.array(X_scaled)
        return X_scaled * self.std_ + self.mean_


class MinMaxScaler:
    """
    Normalización Min-Max: transforma datos al rango [0, 1]
    
    Fórmula: x_norm = (x - min) / (max - min)
    
    ¿CUÁNDO USAR MinMax vs Standard?
    - MinMax: cuando necesitas valores en [0,1], ej: imágenes, redes con sigmoid
    - Standard: generalmente mejor para redes neuronales profundas
    """
    
    def __init__(self, feature_range=(0, 1)):
        self.feature_range = feature_range
        self.min_ = None
        self.max_ = None
        self.is_fitted = False
    
    def fit(self, X):
        """Calcula mínimo y máximo de X."""
        X = np.array(X)
        self.min_ = np.min(X, axis=0)
        self.max_ = np.max(X, axis=0)
        
        # Evitar división por cero
        range_ = self.max_ - self.min_
        range_[range_ == 0] = 1.0
        self.range_ = range_
        
        self.is_fitted = True
        return self
    
    def transform(self, X):
        """Aplica la normalización."""
        if not self.is_fitted:
            raise ValueError("Debes llamar a fit() primero")
        
        X = np.array(X)
        X_scaled = (X - self.min_) / self.range_
        
        # Ajustar al rango deseado
        min_r, max_r = self.feature_range
        return X_scaled * (max_r - min_r) + min_r
    
    def fit_transform(self, X):
        """Fit y transform en un solo paso."""
        return self.fit(X).transform(X)
    
    def inverse_transform(self, X_scaled):
        """Deshace la normalización."""
        if not self.is_fitted:
            raise ValueError("Debes llamar a fit() primero")
        
        X_scaled = np.array(X_scaled)
        min_r, max_r = self.feature_range
        X = (X_scaled - min_r) / (max_r - min_r)
        return X * self.range_ + self.min_


def handle_missing_values(X, strategy='mean'):
    """
    Maneja valores faltantes (NaN).
    
    Estrategias:
    - 'mean': reemplaza NaN con la media de la columna
    - 'median': reemplaza con la mediana (más robusto a outliers)
    - 'zero': reemplaza con 0
    
    ¿POR QUÉ NO SIMPLEMENTE ELIMINAR FILAS CON NaN?
    - Perderíamos demasiados datos
    - En producción, no podemos rechazar datos incompletos
    """
    X = np.array(X, dtype=float)
    
    for col in range(X.shape[1]):
        mask = np.isnan(X[:, col])
        if mask.any():
            if strategy == 'mean':
                fill_value = np.nanmean(X[:, col])
            elif strategy == 'median':
                fill_value = np.nanmedian(X[:, col])
            elif strategy == 'zero':
                fill_value = 0
            else:
                raise ValueError(f"Estrategia desconocida: {strategy}")
            
            X[mask, col] = fill_value
            print(f"  Columna {col}: {mask.sum()} NaN reemplazados con {strategy}")
    
    return X


def one_hot_encode(y, num_classes=None):
    """
    Convierte etiquetas a one-hot encoding.
    
    Ejemplo: para 3 clases
    - Etiqueta 0 → [1, 0, 0]
    - Etiqueta 1 → [0, 1, 0]
    - Etiqueta 2 → [0, 0, 1]
    
    ¿POR QUÉ ONE-HOT?
    Las etiquetas 0, 1, 2 implican un orden (2 > 1 > 0).
    Pero para clasificación, las clases no tienen orden.
    One-hot trata cada clase como igual de diferente de las demás.
    """
    y = np.array(y, dtype=int)
    
    if num_classes is None:
        num_classes = np.max(y) + 1
    
    one_hot = np.zeros((len(y), num_classes))
    one_hot[np.arange(len(y)), y] = 1
    
    return one_hot


def decode_one_hot(y_one_hot):
    """Convierte one-hot de vuelta a etiquetas."""
    return np.argmax(y_one_hot, axis=1)


# ============================================================
# PRUEBAS
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("PRUEBA DE PREPROCESAMIENTO")
    print("=" * 50)
    
    # Datos de ejemplo
    X = np.array([
        [1, 100, 0.1],
        [2, 200, 0.2],
        [3, 300, 0.3],
        [4, 400, 0.4],
        [5, 500, 0.5]
    ])
    
    print("\nDatos originales:")
    print(X)
    
    print("\n--- StandardScaler ---")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print("Después de estandarizar:")
    print(X_scaled)
    print(f"Media por columna: {X_scaled.mean(axis=0)}")
    print(f"Std por columna: {X_scaled.std(axis=0)}")
    
    print("\n--- One-Hot Encoding ---")
    y = np.array([0, 1, 2, 1, 0])
    y_one_hot = one_hot_encode(y, num_classes=3)
    print(f"Etiquetas originales: {y}")
    print(f"One-hot:\n{y_one_hot}")
    print(f"Decodificado: {decode_one_hot(y_one_hot)}")
