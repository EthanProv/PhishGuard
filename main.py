# main.py - Punto de entrada de PhishGuard
#
# Uso:
#   python main.py                          -> modo JSON (por defecto)
#   python main.py --eml  data/emails/      -> archivos .eml reales
#   python main.py --json data/emails.json  -> ruta JSON explicita
#   python main.py --csv  data/dataset.csv  -> dataset etiquetado con metricas

import argparse
import sys
from analyzers import TextAnalyzer, AttachmentAnalyzer, URLAnalyzer
from classifier import PhishingClassifier
from email_parser import parse_eml_folder
from loader    import load_from_json, load_and_evaluate_csv, analyze_thread_recursive
from reporter  import print_report, print_metrics, export_results


if __name__ == "__main__":

    # Inicializar los tres analizadores de texto
    analyzers = [
        TextAnalyzer(),
        AttachmentAnalyzer(),
        URLAnalyzer()
    ]

    # Cargar el clasificador DistilBERT
    classifier = PhishingClassifier()

    # Parsear argumentos de linea de comandos
    parser = argparse.ArgumentParser(prog="PhishGuard")
    group  = parser.add_mutually_exclusive_group()
    group.add_argument("--eml",  metavar="FOLDER", help="Carpeta con archivos .eml")
    group.add_argument("--csv",  metavar="FILE",   help="Dataset CSV etiquetado")
    group.add_argument("--json", metavar="FILE",   help="Archivo JSON con hilo de correos")
    args = parser.parse_args()

    results = []

    if args.csv:
        print(f"\n[PhishGuard] Modo: CSV etiquetado -> '{args.csv}'")
        results = load_and_evaluate_csv(args.csv, classifier, analyzers)
    else:
        if args.eml:
            print(f"\n[PhishGuard] Modo: carpeta EML -> '{args.eml}'")
            emails_to_analyze = parse_eml_folder(args.eml)
        elif args.json:
            print(f"\n[PhishGuard] Modo: JSON -> '{args.json}'")
            emails_to_analyze = load_from_json(args.json)
        else:
            print("\n[PhishGuard] Modo: JSON (por defecto) -> 'data/emails.json'")
            print("  Consejo: usa --eml <carpeta>, --csv <archivo> o --json <archivo>")
            emails_to_analyze = load_from_json("data/emails.json")

        if not emails_to_analyze:
            print("[PhishGuard] No hay correos para analizar. Saliendo.")
            sys.exit(0)

        for email_obj in emails_to_analyze:
            analyze_thread_recursive(email_obj, analyzers, classifier, results)

    if not results:
        print("[PhishGuard] No hay correos para analizar. Saliendo.")
        sys.exit(0)

    # Mostrar resumen y metricas
    print_report(results)
    print_metrics(results)

    # Exportar resultados a ficheros
    export_results(results)

#T(n)= 1 + 3 +1 +1 +1 +1 +1 +1 +1 +1 max(2,max(2,3,3)+ max(2) + 4n) + 2 +1 +1 +1 --> T(n)= 12 + 10 +4n +5 --> T(n)= 27 + 4n