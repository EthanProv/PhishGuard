# reporter.py - Generacion de informes y exportacion de resultados

import os


def print_report(results):
    """
    Muestra un resumen general.
    Complejidad: O(n), porque cuenta los correos phishing.
    """
    total = len(results)
    phishing = 0

    for result in results:
        if result["prediction"] == "Phishing":
            phishing = phishing + 1

    legitimos = total - phishing

    print("\n" + "=" * 65)
    print("              PHISHGUARD -- INFORME DE ANALISIS")
    print("=" * 65)
    print(f"  Correos analizados : {total}")
    print(f"  Phishing           : {phishing}")
    print(f"  Legitimos          : {legitimos}")
    print("=" * 65 + "\n")

    #T(n)= 1 +1 +1 +1 +n*1 +1 +1 +1 +1 --> T(n)= 4 + n +4 --> T(n) = 8 + n


def print_metrics(results):
    """
    Calcula metricas si hay etiqueta real.
    Complejidad: O(n), porque recorre los resultados.
    """
    labeled_results = []

    for result in results:
        if result["true_label"] is not None:
            labeled_results.append(result)

    if not labeled_results:
        return

    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for result in labeled_results:
        prediction = result["prediction"]
        real_label = result["true_label"]

        if prediction == "Phishing" and real_label == "Phishing":
            true_positive = true_positive + 1
        elif prediction == "Phishing" and real_label == "Legitimo":
            false_positive = false_positive + 1
        elif prediction == "Legitimo" and real_label == "Legitimo":
            true_negative = true_negative + 1
        elif prediction == "Legitimo" and real_label == "Phishing":
            false_negative = false_negative + 1

    total = len(labeled_results)

    if total > 0:
        accuracy = (true_positive + true_negative) / total * 100
    else:
        accuracy = 0.0

    if true_positive + false_positive > 0:
        precision = true_positive / (true_positive + false_positive) * 100
    else:
        precision = 0.0

    if true_positive + false_negative > 0:
        recall = true_positive / (true_positive + false_negative) * 100
    else:
        recall = 0.0

    if precision + recall > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0.0

    accuracy = round(accuracy, 2)
    precision = round(precision, 2)
    recall = round(recall, 2)
    f1 = round(f1, 2)

    print("\n" + "=" * 65)
    print("              PHISHGUARD -- METRICAS")
    print("=" * 65)
    print(f"  Correos con etiqueta : {total}")
    print(f"  Accuracy             : {accuracy}%")
    print(f"  Precision            : {precision}%")
    print(f"  Recall               : {recall}%")
    print(f"  F1-score             : {f1}%")
    print("-" * 65)
    print(f"  Verdaderos positivos : {true_positive}")
    print(f"  Falsos positivos     : {false_positive}")
    print(f"  Verdaderos negativos : {true_negative}")
    print(f"  Falsos negativos     : {false_negative}")
    print("=" * 65 + "\n")
    #T(n)= 1 + 1 + n*3 + n*3 + n*3 + n*3 + 1 +2 +2 +2 +2 +1 +1 +1 +1 +1 +1 +1 +1 +1 +1 +1 +1 +1  +1 --> T(n) = 2 + 3n +3n +3n +3n +23 --> T(n)= 25 +9n


def format_entry(result):
    """
    Prepara un resultado para guardarlo en un fichero.
    Complejidad: O(n), porque puede recorrer los textos de los analizadores.
    """
    confidence = round(result["confidence"] * 100, 1)
    true_label = result.get("true_label")

    lines = []
    lines.append(f"[{result['email_id']}]")
    lines.append(f"  Asunto    : {result['subject']}")
    lines.append(f"  Remitente : {result['sender']}")
    lines.append(f"  Confianza : {confidence}%")

    analyzer_texts = result.get("analyzer_texts", {})

    if analyzer_texts:
        lines.append("  Texto analizado:")

        for name, text in analyzer_texts.items():
            preview = text[:120]
            preview = preview.replace("\n", " ")
            preview = preview.strip()

            if preview:
                lines.append(f"    - {name}: {preview}")

    if true_label:
        if true_label == result["prediction"]:
            status = "correcto"
        else:
            status = "incorrecto"

        lines.append(f"  Etiqueta real: {true_label} ({status})")

    explanation = result["explanation"]

    if explanation:
        lines.append("  Explicacion:")

        for line in explanation:
            lines.append(f"    - {line}")

    lines.append("")

    final_text = "\n".join(lines)

    return final_text

#T(n)= 1 +1 +4 +1 max(1+n*4) +3 +3n + 1 +1 --> T(n)= 7 + 4n + 3 +3n +2 --> T(n) = 12 + 4n +3n --> T(n)= 7n + 12

def export_results(results, output_dir="output"):
    """
    Guarda los resultados en dos ficheros.
    Complejidad: O(n), porque reparte los resultados en dos grupos.
    """
    os.makedirs(output_dir, exist_ok=True)

    phishing_results = []
    legit_results = []

    for result in results:
        if result["prediction"] == "Phishing":
            phishing_results.append(result)
        else:
            legit_results.append(result)

    files_to_create = [
        ("phishing.txt", "CORREOS DE PHISHING", phishing_results),
        ("legitimos.txt", "CORREOS LEGITIMOS", legit_results)
    ]

    for filename, title, selected_results in files_to_create:
        path = os.path.join(output_dir, filename)

        with open(path, "w", encoding="utf-8") as file:
            file.write(f"PHISHGUARD -- {title}\n")
            file.write("=" * 65 + "\n\n")

            for result in selected_results:
                entry = format_entry(result)
                file.write(entry + "\n")

            file.write(f"Total: {len(selected_results)} correos\n")

        print(f"  - {filename}: {len(selected_results)} correos")

    print(f"[PhishGuard] Resultados exportados en '{output_dir}/'")
#T(n)= 1 +2 +1 + n *(n*1+1+1++1+1*(n+1)+1) -> T(n)= 4 + n(5n*n) --> T(n)= 4 + 5n³