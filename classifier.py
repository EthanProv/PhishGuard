# classifier.py - Clasificador de phishing usando DistilBERT

import torch
from transformers import pipeline as hf_pipeline


class PhishingClassifier:
    """
    Esta clase carga el modelo de IA y lo usa para decidir
    si un correo parece phishing o legitimo.
    """

    MODEL_NAME = "cybersectony/phishing-email-detection-distilbert_v2.4.1"

    PHISHING_LABELS = {
        "phishing_url",
        "phishing_url_alt",
        "phishing_email",
        "phishing",
        "label_1",
        "1",
        "spam"
    }

    def __init__(self):
        print("[Clasificador] Cargando modelo de IA...")
        print("[Clasificador] La primera vez puede tardar porque descarga el modelo.")

        if torch.cuda.is_available():
            device = 0
            print("[Clasificador] Usando GPU")
        else:
            device = -1
            print("[Clasificador] Usando CPU")

        self.pipeline = hf_pipeline(
            task="text-classification",
            model=self.MODEL_NAME,
            device=device,
            truncation=True,
            max_length=512,
            top_k=None
        )

        print("[Clasificador] Modelo cargado correctamente.")
        #T(n)= 1 +1 +1 +1 +1 + 6 +1 --> T(n)=12

    def predict(self, text):
        """
        Clasifica un texto como Phishing o Legitimo.
        Complejidad: O(n), siendo n el numero de etiquetas que devuelve el modelo.
        """
        scores = self.pipeline(text)[0]

        phishing_score = 0.0
        legit_score = 0.0

        for item in scores:
            label = item["label"].lower()
            score = item["score"]

            is_phishing_label = label in self.PHISHING_LABELS or "phishing" in label

            if is_phishing_label:
                if score > phishing_score:
                    phishing_score = score
            else:
                if score > legit_score:
                    legit_score = score

        if phishing_score > legit_score:
            prediction = "Phishing"
            confidence = phishing_score
        else:
            prediction = "Legitimo"
            confidence = legit_score

        explanation = []

        if prediction == "Phishing":
            percentage = round(confidence * 100, 1)
            explanation.append(f"El modelo ha dado {percentage}% de confianza en phishing")

        confidence = round(confidence, 4)

        return prediction, explanation, confidence
    #T(n) = 1 +1 +1 + n(1 +1 max(1+1),1) + 1 +1 +1 +1 max(3) --> T(n)= 3 + 4n + 7 --> T(n)= 10 + 4n
