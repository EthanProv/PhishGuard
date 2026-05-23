# analyzers.py - Extrae texto del correo para alimentar el clasificador

import re
from abc import ABC, abstractmethod
from models import Email



class BaseAnalyzer(ABC):
    """
    Clase base para los analizadores
    Usa POO y polimorfismo

    Cada analizador tiene su propia forma de analizar el correo,
    pero todos usan los mismos metodos: get_name() y analyze()
    """

    @abstractmethod
    def get_name(self): #O(1)
        pass #O(1)

    @abstractmethod
    def analyze(self, email): #O(1
        pass #O(1)

'''
T(n) = 1+1

'''


class TextAnalyzer(BaseAnalyzer):
    """Extrae el asunto y el cuerpo del correo como texto limpio"""

    # Patron para eliminar etiquetas HTML
    HTML_TAG_PATTERN = re.compile(r'<[^>]+>')   #O(1)

    # Patron para normalizar espacios multiples
    WHITESPACE_PATTERN = re.compile(r'\s+')    #O(1)

    def get_name(self) -> str:
        return "TextAnalyzer"
        #T(n) = 1

    def _strip_html(self, text: str) -> str:
        """Elimina etiquetas HTML y normaliza espacios"""
        clean = self.HTML_TAG_PATTERN.sub(' ', text)
        clean = self.WHITESPACE_PATTERN.sub(' ', clean).strip()
        return clean
        #T(n) = 3
        
    def analyze(self, email: Email) -> str:
        """Devuelve el asunto y el cuerpo limpios de HTML"""
        subject_clean = self._strip_html(email.subject)
        body_clean = self._strip_html(email.body)
        return f"{subject_clean} {body_clean}" 
        #T(n)= 3

#T(n) = 1 +1 + ( 1+ 3 + 3)

class AttachmentAnalyzer(BaseAnalyzer):
    """Analiza los nombres de los archivos adjuntos"""

    def get_name(self):
        return "Adjuntos"

    def analyze(self, email):
        """
        Devuelve los nombres de los adjuntos
        Complejidad: O(n), porque recorre la lista de adjuntos una vez
        """
        filenames = []

        for attachment in email.attachments:
            filename = attachment.get("filename", "")

            if filename:
                filenames.append(filename)

        final_text = " ".join(filenames)

        return final_text
    #T(n)= 1 + (1 +n*1) --> T(n) = 2+n


class URLAnalyzer(BaseAnalyzer):
    """Busca enlaces dentro del cuerpo del correo"""

    URL_PATTERN = re.compile(r"https?://[^\s<>\"']+|www\.[^\s<>\"']+")

    def get_name(self):
        return "Enlaces"

    def analyze(self, email):
        """
        Devuelve las URLs encontradas
        Complejidad: O(n), porque busca dentro del texto del correo
        """
        urls_found = self.URL_PATTERN.findall(email.body)
        final_text = " ".join(urls_found)

        return final_text
    #T(n)= 1 +1
