# classifier.py - Clasificador de phishing usando DistilBERT

import torch
from transformers import pipeline as hf_pipeline


class PhishingClassifier:
    """
    Esta clase carga el modelo de IA y lo usa para decidir
    si un correo parece phishing o legitimo.
    """

    MODEL_NAME = "cybersectony/phishing-email-detection-distilbert_v2.4.1"            #O(1)

    PHISHING_LABELS = {                                    #O(1)
        "phishing_url",
        "phishing_url_alt",
        "phishing_email",
        "phishing",
        "label_1",
        "1",
        "spam"
    }

    def __init__(self):
        print("[Clasificador] Cargando modelo de IA...")                #O(1)
        print("[Clasificador] La primera vez puede tardar porque descarga el modelo.") #Depende de la primera vez o no va ir mas lento            #O(1)

        if torch.cuda.is_available():            #O(1)
            device = 0                        #O(1)
            print("[Clasificador] Usando GPU")            #O(1)
        else:                                #O(1)
            device = -1                            #O(1)
            print("[Clasificador] Usando CPU")                #O(1)

        self.pipeline = hf_pipeline(                        #O(1)
            task="text-classification",
            model=self.MODEL_NAME,
            device=device,
            truncation=True,
            max_length=512,
            top_k=None
        )

        print("[Clasificador] Modelo cargado correctamente.")            #O(1)
        #T(n)= 1 +1 +1 +1 +1 + 6 +1 --> T(n)=12

    def predict(self, text):
        """
        Clasifica un texto como Phishing o Legitimo.
        Complejidad: O(n), siendo n el numero de etiquetas que devuelve el modelo.
        """
        scores = self.pipeline(text)[0] #Esta cosa nos digo la IA para que funcionara -_> Hace que  da el primer resultado que devuelve.    #O(1)

        phishing_score = 0.0    #O(1)
        legit_score = 0.0    #O(1)

        for item in scores:    #O(N)
            label = item["label"].lower()    #O(1)
            score = item["score"]    #O(1)

            is_phishing_label = label in self.PHISHING_LABELS or "phishing" in label        #O(1)

            if is_phishing_label:                #O(1)
                if score > phishing_score:        #O(1)
                    phishing_score = score    #O(1)
            else:    #O(1)
                if score > legit_score:    #O(1)
                    legit_score = score    #O(1)

        if phishing_score > legit_score:        #O(1)
            prediction = "Phishing"            #O(1)
            confidence = phishing_score        #O(1)
        else:                                    #O(1)
            prediction = "Legitimo"            #O(1)
            confidence = legit_score            #O(1)

        explanation = []        #O(1)

        if prediction == "Phishing":                #O(1)
            percentage = round(confidence * 100, 1)            #O(1)
            explanation.append(f"El modelo ha dado {percentage}% de confianza en phishing")            #O(1)

        confidence = round(confidence, 4)            #O(1)

        return prediction, explanation, confidence            #O(1)
#T(n) = 1 +1 +1 + n(1 +1 max(1+1),1) + 1 +1 +1 +1 max(3) --> T(n)= 3 + 4n + 7 --> T(n)= 10 + 4n
# (n)
# Θ(n)
# Promedio = O(n)
