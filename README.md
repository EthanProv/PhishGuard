# PHISHGUARD

Sistema de detección de correos electrónicos de phishing mediante inteligencia artificial. Analiza correos en formato .eml, JSON y CSV, clasificándolos como Phishing o Legítimo usando el modelo DistilBERT de HuggingFace. Los resultados se exportan automáticamente a ficheros de texto con el detalle de cada correo analizado.

---

## Integrantes del grupo

- Ethan Provencio
- Josep Maria Poblet
- Jhoan Lope

---

## Contexto y problemática

El phishing es una de las amenazas de ciberseguridad más extendidas en la actualidad. Consiste en el envío de correos fraudulentos que suplantan la identidad de entidades de confianza con el objetivo de robar credenciales o instalar malware. Según el informe Verizon DBIR, más del 36% de las brechas de seguridad corporativas tienen su origen en correos de phishing.

Los sistemas de detección clásicos basados en listas negras o palabras clave prohibidas presentan dos limitaciones críticas: quedan obsoletos en horas porque los atacantes cambian constantemente sus dominios y vocabulario, y son costosos de mantener manualmente. Phishguard nace para resolver esta problemática usando un modelo de lenguaje capaz de entender el contexto semántico del correo, detectando patrones de phishing aunque el atacante cambie las palabras o el dominio.

---

## Funcionalidades principales

- Clasificación de correos como Phishing o Legítimo con el modelo DistilBERT v2.4.1 (99.58% de precisión oficial).
- Análisis de hilos de correo con respuestas anidadas de forma recursiva.
- Tres modos de entrada: archivos .eml, hilos JSON y datasets CSV etiquetados.
- Limpieza automática de etiquetas HTML del cuerpo antes de clasificar.
- Extracción de URLs y nombres de adjuntos como evidencia adicional.
- Cálculo de métricas de precisión (accuracy, precision, recall, F1-score) en modo CSV.
- Exportación automática de resultados a `output/phishing.txt` y `output/legitimos.txt`.
- Soporte automático de GPU (CUDA) y CPU.
- Motor de IA intercambiable: cambiar una línea actualiza todo el clasificador.

---

## Dependencias y cómo instalar

Requisitos: Python 3.10 o superior.

### Sin GPU (CPU únicamente, ~200MB)

```bash
pip install -r requirements.txt
```

### Con GPU NVIDIA (CUDA, ~2GB)

```bash
pip install -r requirements-gpu.txt
```

> La primera ejecución descarga el modelo automáticamente (~270MB desde HuggingFace).
> Las ejecuciones siguientes lo cargan desde la caché local.

---

## Uso de POO

El proyecto aplica los siguientes principios de Programación Orientada a Objetos:

**Encapsulación:** Cada módulo oculta su lógica interna y expone solo los métodos necesarios. `PhishingClassifier` encapsula completamente el funcionamiento de DistilBERT; el resto del sistema solo llama a `predict(texto)`.

**Herencia y polimorfismo:** `analyzers.py` implementa una jerarquía de clases con `BaseAnalyzer` como clase base abstracta y tres subclases concretas: `TextAnalyzer`, `AttachmentAnalyzer` y `URLAnalyzer`. En `loader.py` se itera sobre una lista de analizadores llamando a `analyze()` en cada uno sin distinguir el tipo concreto, delegando la lógica específica a cada subclase.

**Recursividad con objetos:** La clase `Email` contiene una lista de objetos `Email` en su atributo `replies`, formando un árbol recursivo que representa los hilos de conversación. Las funciones `load_email_recursive()` y `analyze_thread_recursive()` recorren este árbol llamándose a sí mismas.

**Separación de responsabilidades:** Cada módulo tiene una única responsabilidad bien definida: `models.py` (datos), `email_parser.py` (lectura .eml), `analyzers.py` (extracción de texto), `classifier.py` (IA), `loader.py` (carga y análisis), `reporter.py` (informes), `main.py` (coordinación).

---

## Instrucciones de ejecución

```bash
# Modo JSON (por defecto, usa data/emails.json)
python main.py

# Modo EML (correos reales de una carpeta)
python main.py --eml data/emails/spam/

# Modo JSON con ruta explícita
python main.py --json data/emails.json

# Modo CSV (dataset etiquetado con métricas de precisión)
python main.py --csv data/CEAS_08.csv
```

Los resultados se guardan automáticamente en:

```
output/
├── phishing.txt    # correos clasificados como phishing
└── legitimos.txt   # correos clasificados como legítimos
```

---

## Vídeo de presentación

[Enlace al vídeo]

---

## Uso de IA en el desarrollo

Hemos utilizado inteligencia artificial como apoyo durante el desarrollo del proyecto, especialmente en el módulo `analyzers.py`.

Nosotros desarrollamos el diseño inicial de las clases `BaseAnalyzer`, `TextAnalyzer`, `AttachmentAnalyzer` y `URLAnalyzer` con asistencia de la IA, que nos ayudó a implementar la limpieza de HTML.

El resto de módulos (`classifier.py`, `loader.py`, `reporter.py`, `main.py`, `models.py`, `email_parser.py`) fueron desarrollados principalmente por nosotros. La IA se utilizó únicamente como apoyo puntual para resolver dudas concretas.

---

## Evolución del enfoque de clasificación

Durante el desarrollo fuimos probando distintos enfoques hasta encontrar una solución que funcionara bien con correos reales y que pudiera adaptarse a técnicas modernas de phishing.

### Etapa 1 — Reglas manuales (descartado)

El primer metodo que probamos fue un sistema basado en reglas manuales: listas de palabras sospechosas, dominios maliciosos conocidos y extensiones de archivos peligrosas.

Aunque era sencillo de implementar, pronto vimos sus limitaciones. Para cubrir suficientes casos necesitábamos demasiadas reglas y el sistema era difícil de mantener. Además, aparecían muchos falsos positivos y falsos negativos. Los ataques de phishing cambian constantemente y los atacantes modifican el lenguaje, los dominios y la estructura de los correos, así que cualquier lista de reglas quedaba desactualizada muy rápido.

### Etapa 2 — Machine Learning clásico con GBT (descartado)

Después intentamos utilizar Machine Learning clásico entrenando un modelo de Gradient Boosting Trees (GBT) con scikit-learn. Para ello extraíamos características manualmente de los correos, como el número de URLs sospechosas, palabras clave detectadas o tipos de archivos adjuntos.

Los resultados no fueron los esperados. El principal problema era la calidad y antigüedad de los datasets públicos disponibles para entrenamiento. Muchos de ellos, como CEAS_08 o SpamAssassin, contienen correos de 2008 o incluso anteriores. El phishing actual utiliza técnicas muy diferentes, especialmente en la forma de redactar los mensajes y evitar la detección, por lo que el modelo no conseguía clasificar correctamente muchos correos modernos.

### Etapa 3 — Deep Learning con modelos preentrenados (solución definitiva)

Finalmente decidimos utilizar modelos de deep learning preentrenados para clasificación de phishing. Este enfoque nos permitió aprovechar modelos ya entrenados con grandes cantidades de texto y mucho más capaces de adaptarse a variaciones modernas en los correos.

Probamos cuatro modelos distintos de HuggingFace y comparamos su rendimiento utilizando los mismos datasets y métricas. Los resultados fueron considerablemente mejores que en los enfoques anteriores, especialmente en capacidad de detección y reducción de falsos positivos.

---

| Modelo | Tamaño | Accuracy | F1 |
|---|---|---|---|
| cybersectony/distilbert_v2.1 | 270MB | 84.12% | 84.75% |
| ElSlay/BERT-Phishing-Email-Model | 400MB | 85.81% | 86.59% |
| ealvaradob/bert-finetuned-phishing | 1.3GB | 88.38% | 89.28% |
| **cybersectony/distilbert_v2.4.1** | **270MB** | **93.33%** | **93.33%** |

El modelo elegido fue `cybersectony/phishing-email-detection-distilbert_v2.4.1` por tener la mejor relación entre peso y rendimiento, consigue el mejor F1-score con solo 270MB, siendo además el más rápido de ejecutar.
