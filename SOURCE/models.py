# models.py - Modelo de datos del correo electronico
 
class Email:
    """Representa un mensaje de correo con posibles respuestas anidadas."""
 
    def __init__(self, email_id, headers, subject, body, attachments):
        self.email_id = email_id                                             #O(1)
        self.headers = headers                                               #O(1)
        self.subject = subject                                               #O(1)
        self.body = body                                                     #O(1)
        self.attachments = attachments                                       #O(1)
        self.replies = []                                                    #O(1)
 
    def add_reply(self, reply):
        """Añade una respuesta al correo actual."""
        self.replies.append(reply)                                           #O(1)
 
    def print_thread(self, level=0):
        """
        Muestra el hilo de correos usando recursividad.
        Complejidad: O(n), porque recorre todos los correos del hilo.
        """
        spaces = "    " * level                                              #O(1)
        print(f"{spaces}[{self.email_id}] {self.subject}")                   #O(1)
 
        for reply in self.replies:                                           #O(N)
            reply.print_thread(level + 1)                                    #O(1)
 
#T(n) = 5 + 6 +2 + (1+2+1n) --> T(n)= 12 + (3+n)
