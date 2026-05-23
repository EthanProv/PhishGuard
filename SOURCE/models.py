# models.py - Modelo de datos del correo electronico
 
class Email:
    """Representa un mensaje de correo con posibles respuestas anidadas."""
 
    def __init__(self, email_id, headers, subject, body, attachments):
        self.email_id = email_id
        self.headers = headers
        self.subject = subject
        self.body = body
        self.attachments = attachments
        self.replies = []
 
    def add_reply(self, reply):
        """Añade una respuesta al correo actual."""
        self.replies.append(reply)
 
    def print_thread(self, level=0):
        """
        Muestra el hilo de correos usando recursividad.
        Complejidad: O(n), porque recorre todos los correos del hilo.
        """
        spaces = "    " * level
        print(f"{spaces}[{self.email_id}] {self.subject}")
 
        for reply in self.replies:
            reply.print_thread(level + 1)
 
#T(n) = 5 + 6 +2 + (1+2+1n) --> T(n)= 12 + (3+n)
