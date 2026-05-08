'''
Representa un correo electrónico.

Debe guardar:

asunto,
cuerpo,
remitente,
URLs,
adjuntos,
cabeceras,
respuestas anidadas.
'''


# src/correo.py

from dataclasses import dataclass, field


@dataclass
class Correo:
    asunto: str
    cuerpo: str
    remitente: str
    urls: list[str] = field(default_factory=list)
    adjuntos: list[str] = field(default_factory=list)
    cabeceras: dict = field(default_factory=dict)
    respuestas: list["Correo"] = field(default_factory=list)

    # Estos campos son útiles para entrenamiento
    etiqueta: str | None = None
    tipo_dataset: str | None = None
    subtipo: str | None = None