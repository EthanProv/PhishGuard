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
    if not raw_value:                                                                                        #O(1)    
        return ""                                                                                            #O(1)

    decoded_parts = []                                                                                        #O(1)

    for part, charset in decode_header(raw_value):                                                            #O(N)
        if isinstance(part, bytes):                                                                           #O(1)
            try:                                                                                              #O(1)
                decoded_text = part.decode(charset or "utf-8", errors="replace")                              #O(1)
            except (LookupError, UnicodeDecodeError):                                                        #O(1)
                decoded_text = part.decode("utf-8", errors="replace")                                        #O(1)
        else:                                                                                                    #O(1)
            decoded_text = str(part)                                                                            #O(1)

        decoded_parts.append(decoded_text)                                                                    #O(1)

    final_text = " ".join(decoded_parts)                                                                    #O(1)
    final_text = final_text.strip()                                                                            #O(1)

    return final_text                                                                                        #O(1)
    #T(n) = 2 + 1 + n( max(1+1+2)1) +1 = T(n)= 3 + 4n +1 = 4 + 4n


def extract_body(message):
    """
    Extrae el cuerpo del correo.
    Complejidad: O(n), porque puede recorrer todas las partes del mensaje.
    """
    body_parts = []                                                                                        #O(1)

    if message.is_multipart():                                                                            #O(1)
        for part in message.walk():                                                                        #O(N)
            content_type = part.get_content_type()                                                        #O(1)
            disposition = str(part.get("Content-Disposition", ""))                                        #O(1)

            is_text = content_type == "text/plain"                                                        #O(1)
            is_attachment = "attachment" in disposition                                                    #O(1)

            if is_text and not is_attachment:                                                            #O(1)
                try:                                                                                      #O(1)
                    charset = part.get_content_charset() or "utf-8"                                        #O(1)
                    payload = part.get_payload(decode=True)                                            #O(1)
                    text = payload.decode(charset, errors="replace")                                        #O(1)
                except Exception:                                                                          #O(1)
                    text = part.get_payload(decode=False) or ""                                            #O(1)

                body_parts.append(text)                                                                    #O(1)
    else:                                                                                                    #O(1)
        try:                                                                                               #O(1)
            charset = message.get_content_charset() or "utf-8"
            payload = message.get_payload(decode=True)                                                    #O(1)

            if payload:                                                                                    #O(1)
                text = payload.decode(charset, errors="replace")                                            #O(1)
                body_parts.append(text)                                                                    #O(1)
        except Exception:                                                                                  #O(1)
            text = str(message.get_payload() or "")                                                        #O(1)
            body_parts.append(text)                                                                        #O(1)

    body = "\n".join(body_parts)                                                                            #O(1)

    return body                                                                                            #O(1)
#T(n)= 1 + max(1+n*(1+1+max(4)),4)) = T(n)= 1 + 1+7n


def extract_attachments(message):
    """
    Extrae los nombres de los adjuntos.
    Complejidad: O(n), porque revisa las partes del mensaje.
    """
    attachments = []    #O(1)

    for part in message.walk():    #O(N)
        disposition = str(part.get("Content-Disposition", ""))    #O(1)
        filename_raw = part.get_filename()    #O(1)

        if filename_raw and "attachment" in disposition:        #O(2)
            filename = decode_header_value(filename_raw)        #O(1)
            attachments.append({"filename": filename})    #O(1)

    return attachments                    #O(1)

#T(n)= 1 + n*1+1+max(1+1+1+1)= T(n)= 1 +6n


def extract_sender_info(message):
    """Extrae el remitente y la fecha del correo."""
    from_raw = message.get("From", "unknown@unknown.com")    #O(1)
    from_text = decode_header_value(from_raw)        #O(1)

    date = message.get("Date", "")        #O(1)

    match = re.search(r"[\w.\-+]+@[\w.\-]+", from_text)    #O(1)

    if match:    #O(1)
        sender = match.group(0)    #O(1)
    else:        #O(1)
        sender = from_text        #O(1)

    headers = {                    #O(1)
        "sender": sender,
        "date": date
    }

    return headers            #O(1)
#T(n)= 1+1+1+1+2 = T(n)=6


def parse_eml_file(filepath, email_id=None):
    """Lee un archivo .eml y devuelve un objeto Email."""
    if not os.path.exists(filepath):                                    #O(1)
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")    #O(1)

    with open(filepath, "r", encoding="utf-8", errors="replace") as eml_file:    #O(1)
        message = message_from_file(eml_file, policy=email.policy.compat32)    #O(1)

    if email_id:    #O(1)
        final_email_id = email_id    #O(1)
    else:    #O(1)
        basename = os.path.basename(filepath)    #O(1)
        final_email_id = os.path.splitext(basename)[0]    #O(1)

    subject_raw = message.get("Subject", "(sin asunto)")    #O(1)
    subject = decode_header_value(subject_raw)    #O(1)

    headers = extract_sender_info(message)    #O(1)
    body = extract_body(message)                #O(1)
    attachments = extract_attachments(message)    #O(1)

    correo = Email(            #O(1)
        final_email_id,
        headers,
        subject,
        body,
        attachments
    )

    return correo        #O(1)
#T(n)= 1 + 4 +1 +1 +1 +1 +1 +1 +5 --> T(n)=16


def parse_eml_folder(folder_path):
    """
    Lee una carpeta con correos .eml.
    Complejidad: O(n), porque recorre los archivos de la carpeta.
    """
    if not os.path.isdir(folder_path):                                                #O(1)
        raise NotADirectoryError(f"Carpeta no encontrada: {folder_path}")            #O(1)

    emails = []        #O(1)
    eml_files = []    #O(1)

    for filename in os.listdir(folder_path):                                                    #O(N)
        is_eml = filename.lower().endswith(".eml")                                            #O(1)
        looks_like_spamassassin_file = filename.count(".") == 1                            #O(1)
        is_windows_extra_file = filename.endswith(":Zone.Identifier")                        #O(1)

        if is_eml or (looks_like_spamassassin_file and not is_windows_extra_file):            #O(1)
            eml_files.append(filename)                                                        #O(1)

    eml_files.sort()                                                        #O(1)

    if not eml_files:                                                                                    #O(1)
        print(f"[Parser] No se encontraron correos en '{folder_path}'")                    #O(1)
        return emails                                                            #O(1)

    total = len(eml_files)                                                            #O(1)
    print(f"[Parser] Encontrados {total} correo(s) en '{folder_path}'")                            #O(1)

    for filename in eml_files:                                #O(N)
        filepath = os.path.join(folder_path, filename)    #O(1)

        try:                                            #O(1)
            correo = parse_eml_file(filepath)            #O(1)
            emails.append(correo)                                        #O(1)
            print(f"[Parser] Parseado: {filename}")            #O(1)
        except Exception as error:                                    #O(1)
            print(f"[Parser] Error al parsear {filename}: {error}")            #O(1)

    return emails                                            #O(1)

#T(n)= 2 + 1 +1 + n* 1+ 3 + 1 + n*1+4 --> T(n)= 4 +5n +5n --> T(n)= 4+ 10n
