"""
visualization.py - Visualización de datos y resultados

¿POR QUÉ VISUALIZAR?
1. Entender los datos antes de entrenar
2. Detectar problemas (outliers, clases desbalanceadas)
3. Evaluar el rendimiento del modelo
4. Comunicar resultados
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_mnist_samples(X, y, n_samples=10, figsize=(15, 3)):
    """
    Muestra ejemplos de dígitos MNIST.
    
    Args:
        X: Imágenes (puede ser plano 784 o 28x28)
        y: Etiquetas
        n_samples: Número de ejemplos a mostrar
    """
    fig, axes = plt.subplots(1, n_samples, figsize=figsize)
    
    for i, ax in enumerate(axes):
        img = X[i]
        
        # Si está aplanado, reshape a 28x28
        if img.ndim == 1:
            img = img.reshape(28, 28)
        
        ax.imshow(img, cmap='gray')
        ax.set_title(f'Dígito: {y[i]}')
        ax.axis('off')
    
    plt.suptitle('Ejemplos de MNIST', fontsize=14)
    plt.tight_layout()
    return fig


def plot_training_history(history, metrics=['loss', 'accuracy'], figsize=(12, 4)):
    """
    Grafica el historial de entrenamiento.
    
    ¿QUÉ BUSCAMOS EN ESTAS CURVAS?
    
    1. Loss descendente: el modelo está aprendiendo
    2. Accuracy ascendente: mejora la precisión
    3. Train ≈ Validation: buen generalización
    4. Train < Validation: overfitting (aprende demasiado los datos de entrenamiento)
    
    Args:
        history: diccionario con métricas por época
                 {'loss': [0.5, 0.3, ...], 'accuracy': [...]}
    """
    n_metrics = len(metrics)
    fig, axes = plt.subplots(1, n_metrics, figsize=figsize)
    
    if n_metrics == 1:
        axes = [axes]
    
    for ax, metric in zip(axes, metrics):
        if metric in history:
            ax.plot(history[metric], label=f'Train {metric}')
        
        val_metric = f'val_{metric}'
        if val_metric in history:
            ax.plot(history[val_metric], label=f'Validation {metric}')
        
        ax.set_xlabel('Época')
        ax.set_ylabel(metric.capitalize())
        ax.set_title(f'{metric.capitalize()} durante entrenamiento')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_confusion_matrix(y_true, y_pred, class_names=None, figsize=(8, 6)):
    """
    Grafica matriz de confusión.
    
    ¿QUÉ ES UNA MATRIZ DE CONFUSIÓN?
    Muestra cuántas veces el modelo confunde una clase con otra.
    
    - Diagonal: predicciones correctas
    - Fuera de diagonal: errores
    
    Ejemplo para MNIST:
    Si muchos 4 se predicen como 9, hay algo parecido entre ellos.
    """
    from collections import Counter
    
    # Calcular matriz
    classes = np.unique(np.concatenate([y_true, y_pred]))
    n_classes = len(classes)
    
    matrix = np.zeros((n_classes, n_classes), dtype=int)
    
    for true, pred in zip(y_true, y_pred):
        true_idx = np.where(classes == true)[0][0]
        pred_idx = np.where(classes == pred)[0][0]
        matrix[true_idx, pred_idx] += 1
    
    # Graficar
    fig, ax = plt.subplots(figsize=figsize)
    
    im = ax.imshow(matrix, cmap='Blues')
    plt.colorbar(im)
    
    # Etiquetas
    if class_names is None:
        class_names = [str(c) for c in classes]
    
    ax.set_xticks(range(n_classes))
    ax.set_yticks(range(n_classes))
    ax.set_xticklabels(class_names)
    ax.set_yticklabels(class_names)
    
    # Números en las celdas
    for i in range(n_classes):
        for j in range(n_classes):
            color = 'white' if matrix[i, j] > matrix.max() / 2 else 'black'
            ax.text(j, i, str(matrix[i, j]), ha='center', va='center', color=color)
    
    ax.set_xlabel('Predicción')
    ax.set_ylabel('Real')
    ax.set_title('Matriz de Confusión')
    
    plt.tight_layout()
    return fig


def plot_decision_regions(X, y, model, resolution=0.02, figsize=(10, 8)):
    """
    Visualiza las regiones de decisión de un modelo 2D.
    
    Solo funciona con datos de 2 dimensiones.
    Útil para entender cómo el modelo separa las clases.
    """
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    
    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, resolution),
        np.arange(y_min, y_max, resolution)
    )
    
    # Predecir para cada punto del grid
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Regiones
    ax.contourf(xx, yy, Z, alpha=0.3, cmap='viridis')
    
    # Puntos reales
    scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', edgecolor='black')
    plt.colorbar(scatter)
    
    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')
    ax.set_title('Regiones de Decisión')
    
    return fig


def plot_som_map(som, X, y=None, figsize=(10, 10)):
    """
    Visualiza un Self-Organizing Map entrenado.
    
    Muestra:
    - La distribución de neuronas
    - Qué datos activan cada neurona
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Esto se completará cuando implementemos SOM
    ax.text(0.5, 0.5, 'SOM Visualization\n(Coming soon)', 
            ha='center', va='center', transform=ax.transAxes, fontsize=14)
    
    return fig


def plot_autoencoder_reconstruction(original, reconstructed, n_samples=10, figsize=(15, 3)):
    """
    Compara imágenes originales vs reconstruidas por autoencoder.
    
    ¿POR QUÉ ESTA VISUALIZACIÓN?
    Para ver qué tan bien el autoencoder captura la información esencial.
    Una buena reconstrucción significa que el código latente es informativo.
    """
    fig, axes = plt.subplots(2, n_samples, figsize=figsize)
    
    for i in range(n_samples):
        # Original
        img_orig = original[i]
        if img_orig.ndim == 1:
            img_orig = img_orig.reshape(28, 28)
        axes[0, i].imshow(img_orig, cmap='gray')
        axes[0, i].axis('off')
        if i == 0:
            axes[0, i].set_ylabel('Original', fontsize=12)
        
        # Reconstruido
        img_recon = reconstructed[i]
        if img_recon.ndim == 1:
            img_recon = img_recon.reshape(28, 28)
        axes[1, i].imshow(img_recon, cmap='gray')
        axes[1, i].axis('off')
        if i == 0:
            axes[1, i].set_ylabel('Reconstruido', fontsize=12)
    
    plt.suptitle('Original vs Reconstruido (Autoencoder)', fontsize=14)
    plt.tight_layout()
    return fig


# ============================================================
# PRUEBAS
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("PRUEBA DE VISUALIZACIÓN")
    print("=" * 50)
    
    # Datos sintéticos para prueba
    np.random.seed(42)
    
    # Simular historial de entrenamiento
    epochs = 20
    history = {
        'loss': np.exp(-np.linspace(0, 2, epochs)) + 0.1 * np.random.randn(epochs),
        'accuracy': 1 - np.exp(-np.linspace(0, 2, epochs)) + 0.05 * np.random.randn(epochs),
        'val_loss': np.exp(-np.linspace(0, 1.5, epochs)) + 0.15 * np.random.randn(epochs),
        'val_accuracy': 0.9 - np.exp(-np.linspace(0, 1.5, epochs)) + 0.05 * np.random.randn(epochs),
    }
    
    fig = plot_training_history(history)
    plt.savefig('results/training_history_example.png', dpi=100, bbox_inches='tight')
    print("✓ Gráfico de ejemplo guardado en results/training_history_example.png")
    plt.close()
