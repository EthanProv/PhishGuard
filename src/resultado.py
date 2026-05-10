



"""


Este archivo contiene la clase ResultadoAnalisis.

Sirve para guardar:
- la puntuación de riesgo del correo
- los motivos por los que se considera sospechoso
- las características detectadas durante el análisis

Esta clase NO decide si el correo es phishing, spam o legítimo.
Solo guarda los resultados del análisis.

La clasificación final se hará después en clasificador.py.
"""

from dataclasses import dataclass, field


@dataclass
class ResultadoAnalisis:
    """
    Representa el resultado del análisis de un correo.

    Atributos:
        puntuacion: puntuación total de riesgo.
        motivos: lista de motivos detectados durante el análisis.
        caracteristicas: diccionario con características extraídas del correo.
    """

    puntuacion: int = 0
    motivos: list[str] = field(default_factory=list) #field sirve para definir valores por defecto en una clase @dataclass, sobre todo cuando el valor es una lista o un diccionario.
    caracteristicas: dict = field(default_factory=dict)

    def agregar_riesgo(self, puntos: int, motivo: str):
        """
        Añade puntos de riesgo al correo y guarda el motivo.

        Ejemplo:
            resultado.agregar_riesgo(3, "URL sospechosa detectada")
        """

        self.puntuacion += puntos
        self.motivos.append(motivo)

    def agregar_motivo(self, motivo: str):
        """
        Añade un motivo informativo sin sumar puntos de riesgo.

        Esto sirve para guardar información útil aunque no aumente
        directamente la puntuación.
        """

        self.motivos.append(motivo)

    def guardar_caracteristica(self, nombre: str, valor):
        """
        Guarda una característica detectada durante el análisis.

        Ejemplo:
            resultado.guardar_caracteristica("numero_urls", 3)
        """

        self.caracteristicas[nombre] = valor

    def combinar(self, otro_resultado: "ResultadoAnalisis"):
        """
        Combina otro ResultadoAnalisis con este.

        Esto será útil cuando analicemos respuestas anidadas de forma
        recursiva en motor.py.
        """

        self.puntuacion += otro_resultado.puntuacion
        self.motivos.extend(otro_resultado.motivos)
        self.caracteristicas.update(otro_resultado.caracteristicas)

    def tiene_riesgo(self) -> bool:
        """
        Devuelve True si el correo tiene riesgo detectado.
        """

        return self.puntuacion > 0

    def obtener_resumen(self) -> dict:
        """
        Devuelve el resultado en forma de diccionario.

        Esto servirá después para generar informes.
        """

        return {
            "puntuacion": self.puntuacion,
            "motivos": self.motivos,
            "caracteristicas": self.caracteristicas
        }