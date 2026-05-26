# loader.py - Carga correos desde JSON, EML y CSV, y orquesta el analisis

import json
import csv
import os
import sys
from models import Email
from classifier import PhishingClassifier
from analyzers import TextAnalyzer


def load_email_recursive(data):
    """
    Crea un objeto Email desde un JSON.
    Si el correo tiene respuestas, las carga usando recursividad.
    Complejidad: O(n), porque recorre todos los correos del hilo.
    """
    correo = Email(                                        #O(1)
        data["email_id"],
        data["headers"],
        data["subject"],
        data["body"],
        data["attachments"]
    )

    replies = data.get("replies", [])                    #O(1)

    for reply_data in replies:                            #O(n)
        reply = load_email_recursive(reply_data)          #O(1)
        correo.add_reply(reply)                           #O(1)

    return correo                                        #O(1)

# T(n) = c * n
# O(n) = O(n)
# Θ(n) = Θ(n)
# Promedio = O(n)


def analyze_thread_recursive(correo, analyzers, classifier, results):
    """
    Analiza un correo y sus respuestas.
    Aqui tambien se ve el polimorfismo: todos los analizadores usan analyze(),
    pero cada clase lo hace de una forma distinta.
    Complejidad: O(n), porque puede recorrer todos los correos del hilo.
    """
    analyzer_texts = {}                                                            #O(1)

    for analyzer in analyzers:                                                    #O(n)
        analyzer_name = analyzer.get_name()                                       #O(1)
        analyzer_result = analyzer.analyze(correo)                                #O(1)
        analyzer_texts[analyzer_name] = analyzer_result                           #O(1)

    text_parts = []                                                               #O(1)

    for text in analyzer_texts.values():                                         #O(n)
        if text.strip():                                                         #O(1)
            text_parts.append(text)                                              #O(1)

    combined_text = " ".join(text_parts)                                         #O(1)

    prediction, explanation, confidence = classifier.predict(combined_text)      #O(1)

    result = {                                                                  #O(1)
        "email_id": correo.email_id,
        "subject": correo.subject,
        "sender": correo.headers.get("sender", "desconocido"),
        "prediction": prediction,
        "confidence": confidence,
        "explanation": explanation,
        "analyzer_texts": analyzer_texts,
        "true_label": None
    }

    results.append(result)                                                        #O(1)

    for reply in correo.replies:                                                 #O(n)
        analyze_thread_recursive(reply, analyzers, classifier, results)          #O(1)
# T(n) = c * n * a
# O(n * a) = O(n * a)
# Θ(n * a) = Θ(n * a)
# Promedio = O(n * a)
#
# Si el número de analizadores es fijo:
# O(n)
# Θ(n)
# Promedio = O(n)

def load_from_json(filepath):
    """
    Carga correos desde un archivo JSON.
    Puede cargar un solo correo o una lista de correos.
    Complejidad: O(n), porque recorre todos los correos del JSON.
    """
    with open(filepath, "r", encoding="utf-8") as json_file:                    #O(1)
        data = json.load(json_file)                                            #O(1)

    emails = []                                                                #O(1)

    if isinstance(data, list):                                                 #O(1)
        for email_data in data:                                                #O(n)
            correo = load_email_recursive(email_data)                          #O(1)
            emails.append(correo)                                              #O(1)
    else:                                                                      #O(1)
        correo = load_email_recursive(data)                                    #O(1)
        emails.append(correo)                                                  #O(1)

    return emails                                                              #O(1)
# T(n) = c * n
# O(n)
#Θ(n)
# Promedio = O(n)

def clean_csv_text(text):
    """
    Limpia el texto que viene del CSV.
    Complejidad: O(n), porque recorre el texto para quitar HTML y espacios repetidos.
    """
    text = TextAnalyzer.HTML_TAG_PATTERN.sub(" ", text)
    text = TextAnalyzer.WHITESPACE_PATTERN.sub(" ", text)
    text = text.strip()

    return text
# T(m) = 3 * n
#  O(n)
# Θ(n)
# Promedio = (n)

def get_text_from_row(row):
    """Intenta sacar el texto del correo usando diferentes nombres de columna."""
    possible_columns = [                            #O(1)
        "text_combined",
        "text",
        "body"
    ]

    for column in possible_columns:                #O(n)
        value = row.get(column, "")                #O(1)

        if value:                                  #O(1)
            return value                            #O(1)

    return ""                                      #O(1)
# T(n) = c (Porque solo hay 3 columnas fijas)
# O(1)
# Θ(1)
# Promedio = O(1)

def get_real_label(row):
    """Convierte la etiqueta del CSV en Phishing o Legitimo."""
    label_raw = str(row.get("label", "0"))
    label_raw = label_raw.strip()

    if label_raw == "1":
        return "Phishing"

    return "Legitimo"

# T(n) = c (No hay bucles)
#O(1)
#  Θ(1)
# Promedio = O(1)

def load_and_evaluate_csv(csv_path, classifier, analyzers):
    """
    Lee un CSV etiquetado y clasifica cada correo.
    
    """
    if not os.path.exists(csv_path):                                                #O(1)                                            
        print(f"[PhishGuard] Error: archivo no encontrado -> '{csv_path}'")         #O(1)   
        sys.exit(1)                                                                #O(1)

    results = []                                                                    #O(1)

    csv.field_size_limit(10_000_000)                                                #O(1)

    with open(csv_path, "r", encoding="utf-8", errors="ignore") as csv_file:        #O(n)
        reader = csv.DictReader(csv_file)                                            #O(1)
        rows = list(reader)                                                        #O(1)

    total = len(rows)                                                                #O(1)
    print(f"[PhishGuard] Cargados {total} correos del CSV.")                        #O(1)
    print("[PhishGuard] Clasificando...\n")                                        #O(1)

    for index, row in enumerate(rows, 1):                                            #O(N)
        text = get_text_from_row(row)                                                #O(1)
        true_label = get_real_label(row)                                            #O(1)

        if not text.strip():                                                        #O(1)
            continue                                                                #O(1)

        clean_text = clean_csv_text(text)                                            #O(1)
        prediction, explanation, confidence = classifier.predict(clean_text)        #O(1)

        if len(clean_text) > 60:                                                    #O(1)
            subject = clean_text[:60] + "..."                                        #O(1)
        else:                                                                        #O(1)
            subject = clean_text                                                    #O(1)

        result = {                                                                    #O(1)
            "email_id": str(index).zfill(5),
            "subject": subject,
            "sender": "CSV",
            "prediction": prediction,
            "confidence": confidence,
            "explanation": explanation,
            "analyzer_texts": {},
            "true_label": true_label
        }

        results.append(result)                                                        #O(1)

        if index % 100 == 0:                                                        #O(1)
            print(f"  Progreso: {index}/{total} correos clasificados...")            #O(1)

    return results                                                                    #O(1)

# n = número de correos o filas del CSV
# m = longitud media del texto de cada correo
#
# T(n) = c * n * m
# O(n * m)
#  Θ(n * m)
# Promedio = O(n * m)
#
# Si se considera que el tamaño medio del texto y el clasificador son constantes:
# O(n)
# Θ(n)
# Promedio = O(n)
