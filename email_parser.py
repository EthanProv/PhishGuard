# email_parser.py - Parsea archivos .eml y los convierte en objetos Email

import os
import re
import email
import email.policy
from email import message_from_file
from email.header import decode_header
from models import Email


def decode_header_value(raw_value):
    """
    Convierte una cabecera del correo a texto normal.
    Complejidad: O(n), porque recorre las partes decodificadas.
    """
    if not raw_value:
        return ""

    decoded_parts = []

    for part, charset in decode_header(raw_value):
        if isinstance(part, bytes):
            try:
                decoded_text = part.decode(charset or "utf-8", errors="replace")
            except (LookupError, UnicodeDecodeError):
                decoded_text = part.decode("utf-8", errors="replace")
        else:
            decoded_text = str(part)

        decoded_parts.append(decoded_text)

    final_text = " ".join(decoded_parts)
    final_text = final_text.strip()

    return final_text
    #T(n) = 2 + 1 + n( max(1+1+2)1) +1 = T(n)= 3 + 4n +1 = 4 + 4n


def extract_body(message):
    """
    Extrae el cuerpo del correo.
    Complejidad: O(n), porque puede recorrer todas las partes del mensaje.
    """
    body_parts = []

    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))

            is_text = content_type == "text/plain"
            is_attachment = "attachment" in disposition

            if is_text and not is_attachment:
                try:
                    charset = part.get_content_charset() or "utf-8"
                    payload = part.get_payload(decode=True)
                    text = payload.decode(charset, errors="replace")
                except Exception:
                    text = part.get_payload(decode=False) or ""

                body_parts.append(text)
    else:
        try:
            charset = message.get_content_charset() or "utf-8"
            payload = message.get_payload(decode=True)

            if payload:
                text = payload.decode(charset, errors="replace")
                body_parts.append(text)
        except Exception:
            text = str(message.get_payload() or "")
            body_parts.append(text)

    body = "\n".join(body_parts)

    return body
#T(n)= 1 + max(1+n*(1+1+max(4)),4)) = T(n)= 1 + 1+7n


def extract_attachments(message):
    """
    Extrae los nombres de los adjuntos.
    Complejidad: O(n), porque revisa las partes del mensaje.
    """
    attachments = []

    for part in message.walk():
        disposition = str(part.get("Content-Disposition", ""))
        filename_raw = part.get_filename()

        if filename_raw and "attachment" in disposition:
            filename = decode_header_value(filename_raw)
            attachments.append({"filename": filename})

    return attachments

#T(n)= 1 + n*1+1+max(1+1+1+1)= T(n)= 1 +6n


def extract_sender_info(message):
    """Extrae el remitente y la fecha del correo."""
    from_raw = message.get("From", "unknown@unknown.com")
    from_text = decode_header_value(from_raw)

    date = message.get("Date", "")

    match = re.search(r"[\w.\-+]+@[\w.\-]+", from_text)

    if match:
        sender = match.group(0)
    else:
        sender = from_text

    headers = {
        "sender": sender,
        "date": date
    }

    return headers
#T(n)= 1+1+1+1+2 = T(n)=6


def parse_eml_file(filepath, email_id=None):
    """Lee un archivo .eml y devuelve un objeto Email."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8", errors="replace") as eml_file:
        message = message_from_file(eml_file, policy=email.policy.compat32)

    if email_id:
        final_email_id = email_id
    else:
        basename = os.path.basename(filepath)
        final_email_id = os.path.splitext(basename)[0]

    subject_raw = message.get("Subject", "(sin asunto)")
    subject = decode_header_value(subject_raw)

    headers = extract_sender_info(message)
    body = extract_body(message)
    attachments = extract_attachments(message)

    correo = Email(
        final_email_id,
        headers,
        subject,
        body,
        attachments
    )

    return correo
#T(n)= 1 + 4 +1 +1 +1 +1 +1 +1 +5 --> T(n)=16


def parse_eml_folder(folder_path):
    """
    Lee una carpeta con correos .eml.
    Complejidad: O(n), porque recorre los archivos de la carpeta.
    """
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"Carpeta no encontrada: {folder_path}")

    emails = []
    eml_files = []

    for filename in os.listdir(folder_path):
        is_eml = filename.lower().endswith(".eml")
        looks_like_spamassassin_file = filename.count(".") == 1
        is_windows_extra_file = filename.endswith(":Zone.Identifier")

        if is_eml or (looks_like_spamassassin_file and not is_windows_extra_file):
            eml_files.append(filename)

    eml_files.sort()

    if not eml_files:
        print(f"[Parser] No se encontraron correos en '{folder_path}'")
        return emails

    total = len(eml_files)
    print(f"[Parser] Encontrados {total} correo(s) en '{folder_path}'")

    for filename in eml_files:
        filepath = os.path.join(folder_path, filename)

        try:
            correo = parse_eml_file(filepath)
            emails.append(correo)
            print(f"[Parser] Parseado: {filename}")
        except Exception as error:
            print(f"[Parser] Error al parsear {filename}: {error}")

    return emails

#T(n)= 2 + 1 +1 + n* 1+ 3 + 1 + n*1+4 --> T(n)= 4 +5n +5n --> T(n)= 4+ 10n
