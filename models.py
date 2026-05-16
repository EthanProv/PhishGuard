# models.py - Modelo de datos del correo electronico

class Email:
    """Representa un mensaje de correo con posibles respuestas anidadas."""

    def __init__(
        self,
        email_id:    str,
        headers:     dict,
        subject:     str,
        body:        str,
        attachments: list
    ):
        self.email_id = email_id
        self.headers = headers
        self.subject = subject
        self.body = body
        self.attachments = attachments
        self.replies = []  # respuestas anidadas

    def print_thread(self, level: int = 0) -> None:
        indent = "" * level
        print(f"{indent}[{self.email_id}] {self.subject}")
        for reply in self.replies:
            reply.print_thread(level + 1)

#AQUI HAY RECURSIVIDAD porque se llama asi mismo es O(n)
