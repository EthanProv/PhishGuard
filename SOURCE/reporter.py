# reporter.py - Generacion de informes y exportacion de resultados

import os


def print_report(results):
    """
    Muestra un resumen general.
    Complejidad: O(n), porque cuenta los correos phishing.
    """
    total = len(results)                                #0(1)
    phishing = 0                                        #0(1)

    for result in results:                              #O(n)
        if result["prediction"] == "Phishing":          #0(1)
            phishing = phishing + 1                     #0(1)
    
    legitimos = total - phishing                        #0(1)

    print("\n")                                         #0(1)
    print("PHISHGUARD -- INFORME DE ANALISIS")          #0(1)
    print(f"Correos analizados: {total}")               #0(1)
    print(f"Phishing: {phishing}")                      #0(1)
    print(f"Legitimos: {legitimos}")                    #0(1)

    #T(n)= 1+1+(n*2)+1+1+1+1+1+1 --> T(n)= 2+2n+6 --> T(n) = 8 + 2n
    #Big O(n)
    #Teta O(n)
    #Mejor caso O(n)

def print_metrics(results):
    """
    Calcula metricas si hay etiqueta real.
    Complejidad: O(n), porque recorre los resultados.
    """
    labeled_results = []                                #0(1)

    for result in results:                              #0(n)
        if result["true_label"] is not None:            #0(1)
            labeled_results.append(result)              #0(1)

    if not labeled_results:                             #0(1)
        return                                          #0(1)

    true_positive = 0                                   #0(1)
    false_positive = 0                                  #0(1)
    true_negative = 0                                   #0(1)
    false_negative = 0                                  #0(1)

    for result in labeled_results:                      #0(n)
        prediction = result["prediction"]               #0(1)
        real_label = result["true_label"]               #0(1)

        if prediction == "Phishing" and real_label == "Phishing":    #0(2)
            true_positive = true_positive + 1                        #0(1)
        elif prediction == "Phishing" and real_label == "Legitimo":  #0(2)
            false_positive = false_positive + 1                      #0(1)
        elif prediction == "Legitimo" and real_label == "Legitimo":  #0(2)
            true_negative = true_negative + 1                        #0(1)
        elif prediction == "Legitimo" and real_label == "Phishing":  #0(2)
            false_negative = false_negative + 1                      #0(1)

    total = len(labeled_results)                                     #0(1)

    if total > 0:                                                    #0(1)
        accuracy = (true_positive + true_negative) / total * 100     #0(1)
    else:                                                            #0(1)
        accuracy = 0.0                                               #0(1)

    if true_positive + false_positive > 0:                                    #0(1)
        precision = true_positive / (true_positive + false_positive) * 100    #0(1)
    else:                                                                     #0(1)
        precision = 0.0                                                       #0(1)

    if true_positive + false_negative > 0:                                    #0(1)
        recall = true_positive / (true_positive + false_negative) * 100       #0(1)
    else:                                                                     #0(1)
        recall = 0.0                                                          #0(1)

    if precision + recall > 0:                                                #0(1)
        f1 = 2 * precision * recall / (precision + recall)                    #0(1)
    else:                                                                     #0(1)
        f1 = 0.0                                                              #0(1)

    accuracy = round(accuracy, 2)                                             #0(1)
    precision = round(precision, 2)                                           #0(1)
    recall = round(recall, 2)                                                 #0(1)
    f1 = round(f1, 2)                                                         #0(1)

    print("\n")                                                                #0(1)
    print("PHISHGUARD -- METRICAS")                                            #0(1)
    print("=" * 65)                                                            #0(1)
    print(f"Correos con etiqueta: {total}")                                    #0(1)
    print(f"Accuracy: {accuracy}%")                                            #0(1)
    print(f"Precision: {precision}%")                                          #0(1)
    print(f"Recall: {recall}%")                                                #0(1)
    print(f"F1-score: {f1}%")                                                  #0(1)
    print(f"Verdaderos positivos: {true_positive}")                            #0(1)
    print(f"Falsos positivos: {false_positive}")                               #0(1)
    print(f"Verdaderos negativos: {true_negative}")                            #0(1)
    print(f"Falsos negativos: {false_negative}")                               #0(1)
    print("\n")                                                                #0(1)
    #T(n)= 1+(n*2)+6+(n*5)+26 --> T(n) = 2n+5n+33 --> T(n)= 33 + 7n
    #Big O(n)
    #Teta O(n)
    #Mejor caso O(n)

def format_entry(result):
    """
    Prepara un resultado para guardarlo en un fichero.
    Complejidad: O(n), porque puede recorrer los textos de los analizadores.
    """
    confidence = round(result["confidence"] * 100, 1)                        #0(1)
    true_label = result.get("true_label")                                    #0(1)

    lines = []                                                                #0(1)
    lines.append(f"[{result['email_id']}]")                                   #0(1)
    lines.append(f"Asunto: {result['subject']}")                              #0(1)
    lines.append(f"Remitente: {result['sender']}")                            #0(1)
    lines.append(f"Confianza: {confidence}%")                                 #0(1)

    analyzer_texts = result.get("analyzer_texts", {})                         #0(1)

    if analyzer_texts:                                                        #0(1)
        lines.append("  Texto analizado:")                                    #0(1)

        for name, text in analyzer_texts.items():                             #0(n)
            preview = text[:120]                                              #0(1)
            preview = preview.replace("\n", " ")                              #0(1)
            preview = preview.strip()                                         #0(1)

            if preview:                                                       #0(1)
                lines.append(f"    - {name}: {preview}")                      #0(1)

    if true_label:                                                            #0(1)
        if true_label == result["prediction"]:                                #0(1)
            status = "correcto"                                               #0(1)
        else:                                                                 #0(1)
            status = "incorrecto"                                             #0(1)

        lines.append(f"Etiqueta real: {true_label} ({status})")             #0(1)

    explanation = result["explanation"]                                       #0(1)

    if explanation:                                                           #0(1)
        lines.append("Explicacion:")                                        #0(1)

        for line in explanation:                                              #0(n)
            lines.append(f" - {line}")                                     #0(1)

    lines.append("")                                                          #0(1)

    final_text = "\n".join(lines)                                             #0(1)

    return final_text                                                         #0(1)                                               

    #T(n)= 10 + (n*5) + 7 + (n*1) + 3 --> T(n)= 6n + 20
    #Big O(n)
    #Teta O(n)
    #Mejor caso O(n)

def export_results(results, output_dir="output"):
    """
    Guarda los resultados en dos ficheros.
    Complejidad: O(n), porque reparte los resultados en dos grupos.
    """
    os.makedirs(output_dir, exist_ok=True)                                #0(1)

    phishing_results = []                                                 #0(1)
    legit_results = []                                                    #0(1)

    for result in results:                                                #0(n)
        if result["prediction"] == "Phishing":                            #0(1)
            phishing_results.append(result)                               #0(1)
        else:                                                             #0(1)
            legit_results.append(result)                                  #0(1)

    files_to_create = [                                                   #0(1)          
        ("phishing.txt", "CORREOS DE PHISHING", phishing_results),
        ("legitimos.txt", "CORREOS LEGITIMOS", legit_results)
    ]                            

    for filename, title, selected_results in files_to_create:            #0(n)
        path = os.path.join(output_dir, filename)                        #0(1)

        with open(path, "w", encoding="utf-8") as file:                 #0(1)
            file.write(f"PHISHGUARD -- {title}\n")                      #0(1)
            file.write("=" * 65 + "\n\n")                               #0(1)

            for result in selected_results:                              #0(n)
                entry = format_entry(result)                            #0(1)
                file.write(entry + "\n")                                #0(1)

            file.write(f"Total: {len(selected_results)} correos\n")      #0(1)

        print(f"  - {filename}: {len(selected_results)} correos")        #0(1)

    print(f"[PhishGuard] Resultados exportados en '{output_dir}/'")      #0(1)
    
#T(n)= 3 + (n*2) + 1 + (n*5*n*2) + 1 -> T(n)= 4 + 2n + n^2
