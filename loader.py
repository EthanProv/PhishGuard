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
    correo = Email(
        data["email_id"],
        data["headers"],
        data["subject"],
        data["body"],
        data["attachments"]
    )

    replies = data.get("replies", [])

    for reply_data in replies:
        reply = load_email_recursive(reply_data)
        correo.add_reply(reply)

    return correo

#T(n) = 5 +n*1 +1 --> T(n)= 6+n


def analyze_thread_recursive(correo, analyzers, classifier, results):
    """
    Analiza un correo y sus respuestas.
    Aqui tambien se ve el polimorfismo: todos los analizadores usan analyze(),
    pero cada clase lo hace de una forma distinta.
    Complejidad: O(n), porque puede recorrer todos los correos del hilo.
    """
    analyzer_texts = {}

    for analyzer in analyzers:
        analyzer_name = analyzer.get_name()
        analyzer_result = analyzer.analyze(correo)
        analyzer_texts[analyzer_name] = analyzer_result

    text_parts = []

    for text in analyzer_texts.values():
        if text.strip():
            text_parts.append(text)

    combined_text = " ".join(text_parts)

    prediction, explanation, confidence = classifier.predict(combined_text)

    result = {
        "email_id": correo.email_id,
        "subject": correo.subject,
        "sender": correo.headers.get("sender", "desconocido"),
        "prediction": prediction,
        "confidence": confidence,
        "explanation": explanation,
        "analyzer_texts": analyzer_texts,
        "true_label": None
    }

    results.append(result)

    for reply in correo.replies:
        analyze_thread_recursive(reply, analyzers, classifier, results)
    #T(n)= n + n + 3 + 8 + n*4 --> T(n)= 2n + 4n +11 --> T(n)= 6n + 11


def load_from_json(filepath):
    """
    Carga correos desde un archivo JSON.
    Puede cargar un solo correo o una lista de correos.
    Complejidad: O(n), porque recorre todos los correos del JSON.
    """
    with open(filepath, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    emails = []

    if isinstance(data, list):
        for email_data in data:
            correo = load_email_recursive(email_data)
            emails.append(correo)
    else:
        correo = load_email_recursive(data)
        emails.append(correo)

    return emails
#T(n)= 1 + 1 +1 --> T(n)= 3

def clean_csv_text(text):
    """
    Limpia el texto que viene del CSV.
    Complejidad: O(n), porque recorre el texto para quitar HTML y espacios repetidos.
    """
    text = TextAnalyzer.HTML_TAG_PATTERN.sub(" ", text)
    text = TextAnalyzer.WHITESPACE_PATTERN.sub(" ", text)
    text = text.strip()

    return text


def get_text_from_row(row):
    """Intenta sacar el texto del correo usando diferentes nombres de columna."""
    possible_columns = [
        "text_combined",
        "text",
        "body"
    ]

    for column in possible_columns:
        value = row.get(column, "")

        if value:
            return value

    return ""


def get_real_label(row):
    """Convierte la etiqueta del CSV en Phishing o Legitimo."""
    label_raw = str(row.get("label", "0"))
    label_raw = label_raw.strip()

    if label_raw == "1":
        return "Phishing"

    return "Legitimo"



def load_and_evaluate_csv(csv_path, classifier, analyzers):
    """
    Lee un CSV etiquetado y clasifica cada correo.
    Complejidad: O(n), porque procesa las filas del CSV una vez.
    """
    if not os.path.exists(csv_path):
        print(f"[PhishGuard] Error: archivo no encontrado -> '{csv_path}'")
        sys.exit(1)

    results = []

    csv.field_size_limit(10_000_000)

    with open(csv_path, "r", encoding="utf-8", errors="ignore") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    total = len(rows)
    print(f"[PhishGuard] Cargados {total} correos del CSV.")
    print("[PhishGuard] Clasificando...\n")

    for index, row in enumerate(rows, 1):
        text = get_text_from_row(row)
        true_label = get_real_label(row)

        if not text.strip():
            continue

        clean_text = clean_csv_text(text)
        prediction, explanation, confidence = classifier.predict(clean_text)

        if len(clean_text) > 60:
            subject = clean_text[:60] + "..."
        else:
            subject = clean_text

        result = {
            "email_id": str(index).zfill(5),
            "subject": subject,
            "sender": "CSV",
            "prediction": prediction,
            "confidence": confidence,
            "explanation": explanation,
            "analyzer_texts": {},
            "true_label": true_label
        }

        results.append(result)

        if index % 100 == 0:
            print(f"  Progreso: {index}/{total} correos clasificados...")

    return results


#T(n)=3+1+1+1+2+1+1+1 + n(1+1+1+1+1+1+3+8+2) --> T(n)= 11 + 19n