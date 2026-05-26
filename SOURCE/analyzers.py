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
T(n) = 2+2
# O(1) = O(1)
# Θ(1) = Θ(1)
# Promedio = O(1)

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

# T(n) = 3 * n
# O(n) = O(n)
# Θ(n) = Θ(n)
# Promedio = O(n)

class AttachmentAnalyzer(BaseAnalyzer):
    """Analiza los nombres de los archivos adjuntos"""

    def get_name(self):
        return "Adjuntos"    #O(1)

    def analyze(self, email):
        """
        Devuelve los nombres de los adjuntos
        Complejidad: O(n), porque recorre la lista de adjuntos una vez
        """
        filenames = []        #O(1)

        for attachment in email.attachments:            #O(N)
            filename = attachment.get("filename", "")        #O(1)

            if filename:                    #O(1)
                filenames.append(filename)    #O(1)

        final_text = " ".join(filenames)    #O(1)

        return final_text            #O(1)
    #T(n)= 1 + (1 +n*1) --> T(n) = 2+3n
# O(n) = O(n)
# Θ(n) = Θ(n)
# Promedio = O(n)


class URLAnalyzer(BaseAnalyzer):
    """Busca enlaces dentro del cuerpo del correo"""

    URL_PATTERN = re.compile(r"https?://[^\s<>\"']+|www\.[^\s<>\"']+")            #O(1)

    def get_name(self):
        return "Enlaces"    #O(1)

    def analyze(self, email):
        """
        Devuelve las URLs encontradas
        Complejidad: O(n), porque busca dentro del texto del correo
        """
        urls_found = self.URL_PATTERN.findall(email.body)    #O(n)
        final_text = " ".join(urls_found)    #O(1)

        return final_text    #O(1)
    # T(n) = 2n
# O(n) = O(n)
# Θ(n) = Θ(n)
# Promedio = O(n)
