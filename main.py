"""
Aqui es donde se ejecutara todo
"""


#ORYEABA POR AHORA
"""
main.py

Archivo principal temporal para probar PHISHGUARD.

Este main sirve para comprobar:
- que se cargan los correos desde JSON
- que los analizadores funcionan
- que se genera una puntuación de riesgo
- que se muestran los motivos detectados

Más adelante, este main se podrá cambiar para usar:
- MotorAnalisis
- ClasificadorCorreo
- InformeRiesgo
"""


from src.cargador import CargadorCorreos
from src.resultado import ResultadoAnalisis
from src.analizadores import obtener_analizadores_por_defecto


def elegir_archivo_correos() -> str:
    """
    Devuelve la ruta del archivo de correos que se usará para probar.

    Primero intenta usar correosreales.json porque es el archivo de prueba.
    Si no existe, usa correos.json.
    """

    import os

    if os.path.exists("data/correosreales.json"):
        return "data/correosreales.json"

    if os.path.exists("data/correos_prueba.json"):
        return "data/correos_prueba.json"

    if os.path.exists("data/correos.json"):
        return "data/correos.json"

    raise FileNotFoundError(
        "No se ha encontrado ningún archivo de correos en data/"
    )


def clasificar_temporal(puntuacion: int) -> str:
    """
    Clasificación temporal por puntuación.

    Esto es provisional.
    Más adelante lo pondremos bien en clasificador.py.
    """

    if puntuacion >= 15:
        return "PHISHING"
    elif puntuacion >= 8:
        return "SPAM / SOSPECHOSO"
    elif puntuacion >= 3:
        return "SOSPECHOSO LEVE"
    else:
        return "LEGÍTIMO"


def analizar_correo(correo, analizadores):
    """
    Analiza un único correo usando todos los analizadores.

    Parámetros:
        correo: objeto Correo.
        analizadores: lista de analizadores.

    Devuelve:
        ResultadoAnalisis con puntuación, motivos y características.
    """

    resultado = ResultadoAnalisis()

    for analizador in analizadores:
        analizador.analizar(correo, resultado)

    return resultado


def main():
    """
    Función principal del programa.
    """

    print("=" * 70)
    print("PHISHGUARD - PRUEBA TEMPORAL DEL SISTEMA")
    print("=" * 70)

    ruta_correos = elegir_archivo_correos()

    print(f"Archivo usado: {ruta_correos}")

    cargador = CargadorCorreos()
    correos = cargador.cargar_desde_json(ruta_correos)

    print(f"Correos cargados: {len(correos)}")
    print()

    analizadores = obtener_analizadores_por_defecto()

    print("Analizadores cargados:")
    for analizador in analizadores:
        print(f"- {analizador.__class__.__name__}")

    print()
    print("=" * 70)

    for indice, correo in enumerate(correos, start=1):
        resultado = analizar_correo(correo, analizadores)
        clasificacion = clasificar_temporal(resultado.puntuacion)

        print(f"CORREO {indice}")
        print("-" * 70)
        print(f"Asunto: {correo.asunto}")
        print(f"Remitente: {correo.remitente}")

        if correo.etiqueta is not None:
            print(f"Etiqueta real del dataset: {correo.etiqueta}")

        print(f"Puntuación de riesgo: {resultado.puntuacion}")
        print(f"Clasificación temporal: {clasificacion}")

        print("Motivos detectados:")

        if resultado.motivos:
            for motivo in resultado.motivos:
                print(f"  - {motivo}")
        else:
            print("  - No se han detectado señales sospechosas.")

        print("Características extraídas:")

        if resultado.caracteristicas:
            for nombre, valor in resultado.caracteristicas.items():
                print(f"  - {nombre}: {valor}")
        else:
            print("  - No hay características registradas.")

        print("=" * 70)


if __name__ == "__main__":
    main()