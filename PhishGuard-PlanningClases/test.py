from src.cargador import CargadorCorreos


def main():
    cargador = CargadorCorreos()
    correos = cargador.cargar_desde_json("data/correos.json")

    print(f"Correos cargados: {len(correos)}")

    for correo in correos[:5]:
        print("-------------------------")
        print("Asunto:", correo.asunto)
        print("Remitente:", correo.remitente)
        print("Etiqueta:", correo.etiqueta)


if __name__ == "__main__":
    main()