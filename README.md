# PhishGuard — Documentacion

## Que es PhishGuard

PhishGuard es un sistema de deteccion de correos de phishing. Analiza el contenido de un correo (asunto, cuerpo, adjuntos y URLs) y usa un modelo de inteligencia artificial (DistilBERT) para clasificarlo como **Phishing** o **Legitimo**, junto con una puntuacion de confianza.

---

## Descripcion de cada fichero

### `models.py`
Define la clase `Email`, que es la estructura de datos central de todo el programa. Cada correo se representa como un objeto con los campos: ID, cabeceras (remitente y fecha), asunto, cuerpo, adjuntos y una lista de respuestas anidadas. Esta lista permite modelar hilos de correo como un arbol recursivo.

### `email_parser.py`
Se encarga de leer archivos `.eml` del disco y convertirlos en objetos `Email`. Soporta correos con varias partes MIME (texto + HTML + adjuntos) y gestiona la decodificacion de cabeceras codificadas. Tiene dos funciones principales:
- `parse_eml_file`: parsea un unico archivo `.eml`
- `parse_eml_folder`: parsea todos los archivos `.eml` de una carpeta

### `analyzers.py`
Contiene tres clases que extraen texto del correo para pasarselo al modelo de DL. Todas heredan de `BaseAnalyzer` (clase abstracta):
- `TextAnalyzer`: extrae el asunto y el cuerpo, eliminando etiquetas HTML
- `AttachmentAnalyzer`: extrae los nombres de los archivos adjuntos
- `URLAnalyzer`: extrae las URLs del cuerpo usando expresiones regulares

### `classifier.py`
Carga el modelo DistilBERT preentrenado de HuggingFace y lo usa para clasificar correos. El metodo `predict` recibe un texto combinado y devuelve la prediccion (`Phishing` o `Legitimo`), una explicacion y una puntuacion de confianza entre 0 y 1.

### `loader.py`
Gestiona la carga de correos desde distintas fuentes y orquesta el analisis:
- `load_email_recursive`: construye un arbol de objetos `Email` desde un JSON
- `analyze_thread_recursive`: recorre el arbol de correos y clasifica cada uno
- `load_from_json`: carga un hilo de correo desde un archivo JSON
- `load_and_evaluate_csv`: carga un dataset CSV etiquetado y calcula metricas de precision

### `reporter.py`
Genera los informes del analisis:
- `print_report`: imprime un resumen por pantalla (total, phishing, legitimos)
- `print_metrics`: calcula e imprime Accuracy, Precision, Recall y F1-score (solo en modo CSV)
- `export_results`: guarda los resultados en `output/phishing.txt` y `output/legitimos.txt`

### `main.py`
Punto de entrada del programa. Lee los argumentos de linea de comandos, inicializa los analizadores y el clasificador, carga los correos segun el modo seleccionado y llama al reporter para mostrar y exportar los resultados.

---

## Modos de uso

El programa se ejecuta desde la terminal con uno de estos modos:

```
python main.py                          # modo JSON (por defecto, usa data/emails.json)
python main.py --eml  data/emails/      # carpeta con archivos .eml reales
python main.py --json data/emails.json  # archivo JSON con hilo de correos
python main.py --csv  data/dataset.csv  # dataset CSV etiquetado (calcula metricas)
```

---

## Flujo de ejecucion

```
main.py
   |
   |-- 1. Crea los analizadores: TextAnalyzer, AttachmentAnalyzer, URLAnalyzer
   |
   |-- 2. Carga el modelo DistilBERT (classifier.py)
   |       Si es la primera vez, descarga ~270MB desde HuggingFace
   |
   |-- 3. Lee los argumentos y carga los correos segun el modo:
   |
   |       --eml   --> email_parser.py  --> lista de objetos Email
   |       --json  --> loader.py        --> arbol de objetos Email (recursivo)
   |       --csv   --> loader.py        --> lista de correos del CSV
   |
   |-- 4. Analiza y clasifica cada correo:
   |
   |       Para cada Email:
   |         TextAnalyzer     --> texto limpio del asunto + cuerpo
   |         AttachmentAnalyzer --> nombres de adjuntos
   |         URLAnalyzer      --> URLs del cuerpo
   |         Los tres textos se combinan en uno solo
   |         classifier.predict(texto) --> "Phishing" o "Legitimo" + confianza
   |
   |-- 5. Genera el informe:
   |
   |       reporter.print_report()   --> resumen por pantalla
   |       reporter.print_metrics()  --> metricas (solo modo CSV)
   |       reporter.export_results() --> output/phishing.txt y output/legitimos.txt
```

    └── legitimos.txt    # correos clasificados como legitimos
```
