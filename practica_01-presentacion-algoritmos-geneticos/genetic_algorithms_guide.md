# Algoritmos Genéticos: Cuando la IA Copia los Deberes de la Evolución

## 🧬 Parte 1: Primero, entendamos la biología

### El Dogma Central de la Biología Molecular

```
ADN → ARN → Proteína → Forma 3D → Fenotipo (lo que ves)
```

**¿Qué significa cada cosa?**

- **ADN**: El libro de instrucciones. Como el código fuente de un programa.
- **ARN**: La copia de trabajo. Como cuando copias código a otro archivo para ejecutarlo.
- **Proteína**: Las máquinas moleculares que hacen el trabajo.
- **Forma 3D**: Cómo se pliega esa proteína (determina su función).
- **Fenotipo**: El resultado visible: color de ojos, altura, resistencia a enfermedades, etc.

**Ejemplo concreto:**
- Gen del ADN que codifica melanina → ARN mensajero → Proteína melanina → Se deposita en células → Ojos marrones (fenotipo)

### ¿Por qué la evolución funciona?

La evolución necesita **3 ingredientes**:

#### 1. **Variabilidad** (No todos somos iguales)
- Las mutaciones crean diferencias en el ADN
- La reproducción sexual mezcla genes de dos padres
- Resultado: cada individuo es único

#### 2. **Selección** (Los mejores sobreviven más)
- Los individuos con mejores características tienen más probabilidades de sobrevivir
- Los que sobreviven tienen más hijos
- Pasan sus genes "buenos" a la siguiente generación

#### 3. **Herencia** (Los hijos se parecen a los padres)
- Los genes se copian de padres a hijos
- Las características útiles se mantienen en la población
- Con el tiempo, toda la especie mejora

**Ejemplo simple:**
Imagina jirafas con cuellos de diferentes tamaños. Las de cuello largo alcanzan más hojas → comen más → sobreviven más → tienen más crías con cuello largo → después de muchas generaciones, todas las jirafas tienen cuello largo.

### 🔄 El giro inesperado: Transcripción Inversa

El flujo normal es: ADN → ARN → Proteína

**Pero algunos virus hacen trampa:**

```
ARN → ADN (Transcripción Inversa)
```

- Los retrovirus (como el VIH) tienen su información en ARN
- Usan una enzima llamada **transcriptasa inversa**
- Convierten su ARN en ADN
- Insertan ese ADN en nuestras células
- Ahora nuestras células producen más virus

**¿Por qué es importante?**
- Rompe el "dogma central" (la información puede fluir en reversa)
- Muestra que la naturaleza es más flexible de lo que pensábamos
- Esta idea de "reescribir hacia atrás" inspiró algoritmos modernos (lo veremos después)

---

## 🤖 Parte 2: ¿Qué son los Algoritmos Genéticos?

### Definición simple

**Algoritmos de optimización que imitan la evolución biológica para encontrar buenas soluciones a problemas complejos.**

En lugar de:
- ❌ Probar todas las posibilidades (imposible si hay millones)
- ❌ Usar matemáticas complicadas (a veces no hay fórmula)

Hacemos:
- ✅ Crear una población de soluciones
- ✅ Dejar que las mejores "se reproduzcan"
- ✅ Esperar a que "evolucione" una buena solución

### El mapeo Biología ↔ Computación

| Biología | Algoritmo Genético | Ejemplo (Horarios Universidad) |
|----------|-------------------|-------------------------------|
| Individuo | Una solución candidata | Un horario completo específico |
| Población | Conjunto de soluciones | 100 horarios diferentes |
| Cromosoma/ADN | Representación codificada | Lista de todas las asignaciones |
| Gen | Una parte de la solución | "Matemáticas: Lunes 9am Aula 3" |
| Alelo | Valor concreto de un gen | "Lunes 9am" (podría ser "Martes 11am") |
| Fenotipo | La solución real evaluada | El horario funcionando en la universidad |
| Fitness | Qué tan buena es la solución | Puntuación: ¿funciona bien? |
| Selección Natural | Elegir mejores soluciones | Horarios sin conflictos se quedan |
| Reproducción Sexual | Cruce (crossover) | Mezclar dos horarios buenos |
| Mutación | Cambio aleatorio pequeño | Cambiar una clase de hora |

---

## 🔄 Parte 3: El Ciclo Completo (Paso a Paso)

Vamos a usar un ejemplo simple: **encontrar la combinación óptima de parámetros para un modelo**.

### Paso 1: Población Inicial

**¿Qué hacemos?**
Creamos muchas soluciones aleatorias (por ejemplo, 100).

**Representación como "cromosoma":**

Cada individuo es una cadena de números que representa una solución:

```
Individuo 1: [0.3, 0.7, 0.2, 0.9, 0.1]
Individuo 2: [0.8, 0.2, 0.5, 0.4, 0.6]
Individuo 3: [0.1, 0.9, 0.8, 0.3, 0.7]
...
Individuo 100: [0.6, 0.4, 0.3, 0.8, 0.2]
```

Cada posición en la lista es un "gen" (un parámetro del problema).

**Clave:** Al principio, la mayoría serán soluciones malas. ¡Es completamente normal!

---

### Paso 2: Evaluación (Función de Fitness)

**¿Qué hacemos?**
Evaluamos cada solución para saber qué tan buena es.

**La función de fitness depende completamente de tu problema:**

```
Fitness = función que mide qué tan buena es la solución
```

**Ejemplo:**
Si estás optimizando parámetros de un modelo de predicción:
```
Fitness = Precisión del modelo con esos parámetros
```

**Resultados:**
```
Individuo 1: Fitness = 0.45 (45% de precisión) - MALO
Individuo 2: Fitness = 0.78 (78% de precisión) - BUENO
Individuo 3: Fitness = 0.62 (62% de precisión) - REGULAR
...
```

**Analogía biológica:**
Es como medir "qué tan bien sobrevive" cada individuo en su ambiente. Los que sobreviven mejor tienen mejor fitness.

---

### Paso 3: Selección

**¿Qué hacemos?**
Elegimos qué individuos se van a "reproducir".

**IMPORTANTE:** NO eliminamos todos los malos. ¿Por qué?

Porque un individuo "malo" globalmente puede tener partes muy buenas que queremos conservar.

**Métodos de selección:**

1. **Ruleta:** Probabilidad proporcional al fitness
   - Fitness 0.78 → 78% probabilidad relativa
   - Fitness 0.45 → 45% probabilidad relativa

2. **Torneo:** Elegir 5 al azar, el mejor de esos 5 se reproduce

3. **Élite:** Los top 10 mejores pasan automáticamente a la siguiente generación

**Analogía biológica:**
Los individuos más aptos tienen más probabilidad de reproducirse, pero no es garantizado. Incluso los menos aptos pueden tener descendencia (y sus genes pueden ser útiles).

### Paso 4: Cruce (Crossover) - LA MAGIA

**¿Qué hacemos?**
Mezclamos dos soluciones buenas para crear nuevas soluciones que heredan lo mejor de ambas.

**Ejemplo visual:**

```
PADRE 1: [0.3, 0.7, 0.2, 0.9, 0.1]
PADRE 2: [0.8, 0.2, 0.5, 0.4, 0.6]
                    ↑ PUNTO DE CORTE

HIJO 1:  [0.3, 0.7, 0.2 | 0.4, 0.6]  ← Primera parte del Padre 1, segunda del Padre 2
HIJO 2:  [0.8, 0.2, 0.5 | 0.9, 0.1]  ← Primera parte del Padre 2, segunda del Padre 1
```

**¿Por qué funciona?**
Si el Padre 1 tiene buenos valores en las primeras posiciones y el Padre 2 tiene buenos valores en las últimas, el hijo puede heredar ambas características buenas.

**Analogía biológica:**
Es como tú heredando:
- La buena visión de tu madre
- La altura de tu padre
- Potencialmente tienes ventajas de ambos

### Paso 5: Mutación

**¿Qué hacemos?**
Con una pequeña probabilidad (ej: 2%), cambiamos aleatoriamente un valor.

**Ejemplo:**

```
ANTES de mutación:
[0.3, 0.7, 0.2, 0.4, 0.6]

Tiro dado: ¿Muto? → SÍ (2% de probabilidad)
Elijo posición aleatoria: 3
Cambio el valor: 0.2 → 0.9

DESPUÉS de mutación:
[0.3, 0.7, 0.9, 0.4, 0.6]
          ↑ MUTÓ
```

**¿Por qué es CRUCIAL?**

Sin mutación, estás limitado a recombinar valores que ya existen en la población inicial.

**Ejemplo:**
```
Población inicial:
- Nadie tiene valores superiores a 0.8 en ninguna posición
- Todos los individuos tienen valores entre 0.1 y 0.8

Por mucho que cruces, NUNCA aparecerá un 0.9 o un 1.0
La mutación puede crear estos valores nuevos de la nada.
```

**Analogía biológica:**
- Sin mutación: solo recombinamos genes existentes
- Con mutación: aparecen características completamente nuevas

**Problema de "óptimos locales":**
```
Imagina que estás buscando el punto más alto de una ciudad.
Te encuentras en el tejado de un edificio de 50 metros.
Sin mutación: nunca bajarías a explorar si hay un rascacielos de 200m al lado.
Con mutación: ocasionalmente "saltas" a explorar otras zonas.
```

### Paso 6: Nueva Generación y Repetir

**¿Qué hacemos?**
1. Los hijos (creados por cruce y mutación) forman la nueva población
2. A veces conservamos los mejores padres (elitismo): los top 5 pasan automáticamente
3. Volvemos al Paso 2 (evaluamos fitness de la nueva generación)

**Criterios de parada:**

¿Cuándo paramos de evolucionar?

1. **Por generaciones:** Llegamos a generación 1000
2. **Por fitness:** Encontramos una solución con fitness > 0.95
3. **Por estancamiento:** No mejora en 50 generaciones consecutivas

**Evolución típica:**

```
Generación 1:   Mejor fitness = 0.52 (solución mala pero la menos mala)
Generación 10:  Mejor fitness = 0.67 (mejora notable)
Generación 50:  Mejor fitness = 0.84 (bastante buena)
Generación 200: Mejor fitness = 0.93 (casi óptima)
Generación 350: Mejor fitness = 0.94 (mejora muy lenta)
→ PARAMOS (no mejora significativamente)
```

## 🧬 Parte 4: El Toque Personal - Transcripción Inversa Computacional

### Recordatorio: Transcripción Inversa en Biología

```
Normal:  ADN → ARN → Proteína
Retrovirus: ARN → ADN (escribir hacia atrás)
```

### El Equivalente en Algoritmos Modernos

**Problema tradicional de algoritmos genéticos:**
- El genotipo (código) evoluciona
- El fenotipo (solución evaluada) NO afecta de vuelta al genotipo
- Es como la evolución normal: no importa cuánto entrenes, tus hijos no nacen con músculos

**Pero en computación podemos hacer "trampa":**

#### 🔄 Algoritmos Meméticos (IA + Evolución + "Transcripción Inversa")

```
1. Evoluciona una solución (Algoritmo Genético)
   Genotipo: [Solución codificada]
   
2. MEJORA esa solución localmente (Búsqueda local, IA)
   Fenotipo: [Solución optimizada con técnicas adicionales]
   "El individuo aprende durante su vida"
   
3. REESCRIBE el genotipo con las mejoras
   Nuevo Genotipo: [Solución optimizada RE-CODIFICADA]
   ← ¡TRANSCRIPCIÓN INVERSA!
   
4. Este genotipo mejorado se reproduce
   "Las características adquiridas SÍ se heredan"
```

**Ejemplo concreto:**

```
Gen 1: Creas solución aleatoria
       Genotipo: [0.3, 0.5, 0.7]
       Fitness: 0.40

Gen 6: La solución ha evolucionado
       Genotipo: [0.4, 0.6, 0.8]
       Fitness: 0.65
       
       ↓ APLICAS IA (optimización local, gradient descent)
       
       Fenotipo mejorado: [0.42, 0.68, 0.85]
       Fitness: 0.82 (¡mucho mejor!)
       
       ↓ TRANSCRIPCIÓN INVERSA: recodificas esto al genotipo
       
       Nuevo Genotipo: [0.42, 0.68, 0.85]
       
       ↓ Este genotipo mejorado se reproduce
       
       Sus "hijos" heredan la optimización inteligente
```

**¿Por qué es poderoso?**
- Combina exploración global (AG) con optimización local (IA)
- Las mejoras "inteligentes" se heredan (imposible en biología real)
- Converge mucho más rápido a buenas soluciones

### Otras "Transcripciones Inversas" en IA

**Transfer Learning:**
```
Modelo entrenado (fenotipo expresado)
     ↓ Extraer conocimiento
Nuevo modelo con ese conocimiento (reescribir genotipo)
```

**Neural Architecture Search:**
```
Red neuronal entrenada rinde bien (fenotipo fitness alto)
     ↓ Analizar qué arquitectura funcionó
Modificar el código genético para más redes así
```

---

## 🎯 Parte 5: ¿Por qué es importante la IA en Biología?

### Problemas biológicos que necesitan Algoritmos Genéticos

#### 1. **Diseño de Proteínas**
- Problema: Una proteína puede plegarse en 10^300 formas
- Imposible probar todas
- AG + IA: Evolucionan estructuras proteicas estables
- **Aplicación:** Diseñar enzimas para degradar plásticos

#### 2. **Predicción de Estructura 3D (AlphaFold)**
- Relación: ADN → Proteína → ¿Forma 3D?
- AlphaFold usa IA + inspiración evolutiva
- Compara con proteínas conocidas (información "heredada")
- Optimiza predicciones

#### 3. **Descubrimiento de Fármacos**
- Problema: Probar millones de moléculas vs una proteína objetivo
- AG evoluciona moléculas candidatas
- **Tu ejemplo:** Terapias con transcripción inversa para cáncer
  - Diseñar inhibidores de transcriptasa inversa
  - Evolucionar vectores virales para terapia génica

#### 4. **Optimización de CRISPR**
- Problema: Diseñar secuencias guía que no corten donde no deben
- AG evalúan millones de secuencias candidatas
- Minimizan efectos off-target

#### 5. **Filogenética (Árboles Evolutivos)**
- Problema: Construir el árbol de relaciones entre especies
- Espacio de búsqueda: (2n-3)!! posibles árboles (n=especies)
- Para 10 especies: 34 millones de árboles posibles
- AG encuentran los árboles más probables

### La Conexión Profunda

```
BIOLOGÍA inspira IA → IA resuelve problemas de BIOLOGÍA
                ↑                                    ↓
         (Algoritmos Genéticos)          (Diseño proteínas, fármacos)
```

**La IA en biología es importante porque:**

1. **Escala:** La biología genera datos masivos (genomas, proteomas)
2. **Complejidad:** Sistemas no-lineales, miles de variables interactuando
3. **Optimización:** Encontrar la mejor terapia, proteína, o diagnóstico entre infinitas posibilidades
4. **Inspiración mutua:** La evolución nos enseña algoritmos, los algoritmos descubren biología nueva

---

## 📊 Parte 6: Casos de Uso Reales

### 1. Diseño de Antenas Satelitales - NASA (2006)
- **Problema:** Diseñar antena para satélite ST5 con múltiples restricciones técnicas
- **Solución:** Algoritmo genético evolucionó 10,000 generaciones de diseños
- **Resultado:** Forma no-intuitiva (asimétrica, ramificada)
- **Impacto:** 
  - Mejor rendimiento que diseños humanos tradicionales
  - Más ligera y eficiente
  - Los ingenieros no entienden completamente por qué funciona tan bien
- **Referencia:** Evolutionary Antenna Design at NASA

### 2. Optimización de Plegamiento de Proteínas
- **Problema:** Una proteína puede plegarse en 10^300 formas posibles
- **Aplicación:** 
  - Predecir estructura 3D de proteínas
  - Diseñar enzimas artificiales para degradar plásticos
  - Optimizar anticuerpos terapéuticos
- **Herramientas:** Rosetta@home, FoldIt
- **Impacto real:** Diseño de enzimas que descomponen PET en horas (vs siglos naturalmente)

### 3. Diseño de Fármacos - Insilico Medicine
- **Problema:** Explorar millones de moléculas candidatas para un target específico
- **Aplicación:** 
  - Descubrimiento de moléculas para fibrosis pulmonar idiopática
  - Optimización de propiedades ADME (absorción, distribución, metabolismo, excreción)
- **Resultado:** 
  - Molécula llegó a ensayos clínicos Fase I en 18 meses
  - Proceso tradicional: 4-5 años
- **Técnica:** AG combinados con deep learning

### 4. Optimización de Rutas de Logística - UPS
- **Problema:** Optimizar rutas de entrega de millones de paquetes diariamente
- **Aplicación:** Sistema ORION (On-Road Integrated Optimization and Navigation)
- **Impacto:** 
  - Ahorro de 100 millones de dólares/año en combustible
  - Reducción de 100,000 toneladas de CO2/año
  - Optimiza rutas de 55,000 conductores simultáneamente
- **Complejidad:** Problema NP-hard con millones de variables

### 5. Scheduling de Producción Industrial
- **Problema:** Asignar tareas a máquinas minimizando tiempo y coste
- **Ejemplos:**
  - **Airbus:** Programación de ensamblaje de componentes de aviones
  - **Siemens:** Optimización de líneas de producción de turbinas
- **Variables:** Orden de tareas, asignación de recursos, tiempos de setup
- **Impacto:** Reducción de 15-30% en tiempos de producción

### 6. Optimización de Carteras de Inversión
- **Problema:** Seleccionar activos maximizando retorno y minimizando riesgo
- **Aplicación:** Multi-objetivo (retorno vs riesgo vs liquidez vs diversificación)
- **Ventaja de AG:** Manejan restricciones reales (no vender en corto ciertos activos, límites regulatorios)
- **Instituciones:** Varios hedge funds usan variantes de AG

### 7. Calibración de Modelos Climáticos
- **Problema:** Ajustar ~100 parámetros en modelos de circulación general atmosférica
- **Desafío:** 
  - Cada simulación tarda horas/días
  - Espacio de parámetros gigantesco
  - No hay gradiente disponible
- **Aplicación:** NCAR, Met Office UK
- **Resultado:** Modelos calibrados predicen mejor temperaturas, precipitaciones

### 8. Diseño de Circuitos Analógicos
- **Problema:** Diseñar circuitos electrónicos con componentes discretos
- **Variables:** Valores de resistencias, capacitores, topología del circuito
- **Resultado:** AG han diseñado:
  - Amplificadores de bajo ruido
  - Filtros con respuestas no-estándar
  - Osciladores de alta precisión
- **Ventaja:** Descubren topologías que humanos no considerarían

### 9. Optimización de Hiperparámetros en ML
- **Problema:** Encontrar mejores hiperparámetros para redes neuronales
- **Variables:** Learning rate, batch size, número de capas, dropout, etc.
- **Herramientas:** 
  - TPOT (AutoML con AG)
  - NEAT (evoluciona arquitecturas de redes neuronales)
- **Aplicación real:** Google AutoML usa técnicas inspiradas en AG

### 10. Diseño de Moléculas Farmacéuticas - Generación de Novo
- **Problema:** Crear moléculas completamente nuevas con propiedades deseadas
- **Proceso:**
  1. Codificar moléculas como "genes" (SMILES strings)
  2. Evaluar: afinidad al target, toxicidad, solubilidad
  3. Evolucionar hacia moléculas óptimas
- **Éxito:** 
  - Descubrimiento de inhibidores de quinasas
  - Antibióticos con nuevos mecanismos de acción
- **Empresas:** Atomwise, BenevolentAI, Recursion Pharmaceuticals

## ✅ Parte 7: ¿Cuándo usar Algoritmos Genéticos?

### ✅ Buenos para:

1. **Espacios de búsqueda gigantescos**
   - Millones o billones de combinaciones posibles
   - Imposible probar todas

2. **Problemas combinatorios**
   - Traveling Salesman Problem (ruta más corta)
   - Bin packing (empaquetar cajas eficientemente)
   - Scheduling (horarios, turnos, rutas)

3. **No hay gradiente (no puedes derivar)**
   - La función no es matemáticamente diferenciable
   - Ejemplo: "¿Es este diseño bonito?" (subjetivo)

4. **Optimización multi-objetivo**
   - Maximizar calidad Y minimizar coste Y minimizar tiempo
   - No hay una "mejor" solución única

5. **Problemas "rugosos" (muchos óptimos locales)**
   - El paisaje de soluciones tiene muchas colinas y valles
   - Fácil quedarse atascado

### ❌ NO tan buenos para:

1. **Hay fórmula matemática exacta**
   - Ejemplo: resolver 2x + 3 = 7
   - Usa álgebra simple

2. **Necesitas LA solución óptima garantizada**
   - AG encuentran soluciones "muy buenas", no perfectas
   - Si necesitas perfección matemática, usa programación lineal

3. **Espacios continuos y suaves**
   - Si puedes calcular gradientes, usa gradient descent
   - Mucho más rápido y directo

4. **Problemas simples con pocas variables**
   - Para 3-4 variables, prueba fuerza bruta
   - AG tienen overhead (gestionar población, etc.)

---

## 🎤 Cierre: De Retrovirus a Algoritmos

**El viaje completo:**

1. La naturaleza evoluciona durante 3.800 millones de años
2. Descubrimos cómo funciona: variación, selección, herencia
3. Descubrimos que algunos virus "escriben hacia atrás" (transcripción inversa)
4. Copiamos la evolución en algoritmos (AG)
5. Mejoramos esos algoritmos haciéndolos "escribir hacia atrás" también (meméticos)
6. Usamos esos algoritmos para resolver... problemas biológicos

**El círculo se cierra.**

La evolución tardó milenios en optimizar. Nosotros optimizamos en horas.

No porque seamos más listos que la naturaleza.

Sino porque **le copiamos bien los deberes**.

Y de vez en cuando, mejoramos el examen.