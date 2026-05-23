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
    analyzers = [                                                                                                            #O(1)
        TextAnalyzer(),
        AttachmentAnalyzer(),
        URLAnalyzer()
    ]

    # Cargar el clasificador DistilBERT
    classifier = PhishingClassifier()                                                                                        #O(1)

    # Parsear argumentos de linea de comandos
    parser = argparse.ArgumentParser(prog="PhishGuard")                                                                      #O(1)
    group  = parser.add_mutually_exclusive_group()                                                                           #O(1)
    group.add_argument("--eml",  metavar="FOLDER", help="Carpeta con archivos .eml")                                         #O(1)
    group.add_argument("--csv",  metavar="FILE",   help="Dataset CSV etiquetado")                                            #O(1)
    group.add_argument("--json", metavar="FILE",   help="Archivo JSON con hilo de correos")                                  #O(1)
    args = parser.parse_args()                                                                                               #O(1)

    results = []                                                                                                            #O(1)

    if args.csv:                                                                                                            #O(1)
        print(f"\n[PhishGuard] Modo: CSV etiquetado -> '{args.csv}'")                                                       #O(1)
        results = load_and_evaluate_csv(args.csv, classifier, analyzers)                                                    #O(1)
    else:                                                                                                                   #O(1)
        if args.eml:                                                                                                        #O(1)
            print(f"\n[PhishGuard] Modo: carpeta EML -> '{args.eml}'")                                                      #O(1)
            emails_to_analyze = parse_eml_folder(args.eml)                                                                  #O(1)
        elif args.json:                                                                                                     #O(1)
            print(f"\n[PhishGuard] Modo: JSON -> '{args.json}'")                                                            #O(1)
            emails_to_analyze = load_from_json(args.json)                                                                   #O(1)
        else:                                                                                                               #O(1)
            print("\n[PhishGuard] Modo: JSON (por defecto) -> 'data/emails.json'")                                          #O(1)
            print("  Consejo: usa --eml <carpeta>, --csv <archivo> o --json <archivo>")                                     #O(1)
            emails_to_analyze = load_from_json("data/emails.json")                                                          #O(1)

        if not emails_to_analyze:                                                                                           #O(1)
            print("[PhishGuard] No hay correos para analizar. Saliendo.")                                                   #O(1)
            sys.exit(0)                                                                                                     #O(1)

        for email_obj in emails_to_analyze:                                                                                 #O(n)
            analyze_thread_recursive(email_obj, analyzers, classifier, results)                                             #O(1)

    if not results:                                                                                                         #O(1)
        print("[PhishGuard] No hay correos para analizar. Saliendo.")                                                       #O(1)
        sys.exit(0)                                                                                                         #O(1)

    # Mostrar resumen y metricas
    print_report(results)                                                                                                    #O(1)
    print_metrics(results)                                                                                                   #O(1)

    # Exportar resultados a ficheros
    export_results(results)                                                                                                #O(1)

#T(n)= 1 + 3 +1 +1 +1 +1 +1 +1 +1 +1 max(2,max(2,3,3)+ max(2) + 4n) + 2 +1 +1 +1 --> T(n)= 12 + 10 +4n +5 --> T(n)= 27 + 4n
