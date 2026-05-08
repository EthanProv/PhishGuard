'''
Carga los correos simulados desde correos.json.
'''

# src/cargador.py
# src/cargador.py

import json
from pathlib import Path
from .correo import Correo


class CargadorCorreos:
    """
    Clase encargada de cargar correos desde un archivo JSON.

    Esta clase lee correos desde un archivo como:
        data/correos.json
        data/correos_entrenamiento.json
        data/correos_prueba.json

    Y convierte cada correo del JSON en un objeto de la clase Correo.
    """

    def cargar_desde_json(self, ruta_archivo: str) -> list[Correo]:
        """
        Carga una lista de correos desde un archivo JSON.

        Parámetros:
            ruta_archivo: ruta del archivo JSON.

        Devuelve:
            Una lista de objetos Correo.
        """

        ruta = Path(ruta_archivo)

        if not ruta.exists():
            raise FileNotFoundError(f"No se ha encontrado el archivo: {ruta_archivo}")

        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError("El archivo JSON debe contener una lista de correos.")

        correos = []

        for correo_json in datos:
            correo = self._crear_correo_recursivo(correo_json)
            correos.append(correo)

        return correos

    def _crear_correo_recursivo(self, datos: dict) -> Correo:
        """
        Convierte un diccionario del JSON en un objeto Correo.

        Esta función es recursiva porque un correo puede tener respuestas,
        y cada respuesta también puede tener más respuestas dentro.
        """

        respuestas = []

        for respuesta_json in datos.get("respuestas", []):
            respuesta = self._crear_correo_recursivo(respuesta_json)
            respuestas.append(respuesta)

        correo = Correo(
            asunto=datos.get("asunto", ""),
            cuerpo=datos.get("cuerpo", ""),
            remitente=datos.get("remitente", ""),
            urls=datos.get("urls", []),
            adjuntos=datos.get("adjuntos", []),
            cabeceras=datos.get("cabeceras", {}),
            respuestas=respuestas,
            etiqueta=datos.get("etiqueta"),
            tipo_dataset=datos.get("tipo_dataset"),
            subtipo=datos.get("subtipo")
        )

        return correo