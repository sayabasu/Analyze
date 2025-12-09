from flask import Flask, request, jsonify

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import SpacyNlpEngine
from presidio_analyzer.predefined_recognizers.generic import (
    CreditCardRecognizer,
    EmailRecognizer,
    PhoneRecognizer,
    UrlRecognizer,
)

from custom_recognizers_india import pan_recognizer, aadhaar_recognizer


# -------------------------------------------------------
# 1) Proper spaCy NLP Engine Configuration (REQUIRED)
# -------------------------------------------------------
nlp_models = [
    {
        "lang_code": "en",
        "model_name": "en_core_web_lg",
    }
]

nlp_engine = SpacyNlpEngine(models=nlp_models)

# -------------------------------------------------------
# 2) Register built-in + custom recognizers
# -------------------------------------------------------
registry = RecognizerRegistry()
registry.add_recognizer(EmailRecognizer())
registry.add_recognizer(PhoneRecognizer())
registry.add_recognizer(UrlRecognizer())
registry.add_recognizer(CreditCardRecognizer())
registry.add_recognizer(pan_recognizer)
registry.add_recognizer(aadhaar_recognizer)

# -------------------------------------------------------
# 3) Create AnalyzerEngine
# -------------------------------------------------------
analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine,
    registry=registry,
    supported_languages=["en"],
)

# -------------------------------------------------------
# 4) Flask REST API
# -------------------------------------------------------
app = Flask(__name__)

# Only return the PII categories we care about instead of every spaCy entity.
DEFAULT_ENTITY_FILTER = [
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "URL",
    "CREDIT_CARD",
    "IN_PAN",
    "IN_AADHAAR",
]


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")
    language = data.get("language", "en")
    entities = data.get("entities")  # optional: filter only some entity types

    if not entities:
        entities = DEFAULT_ENTITY_FILTER

    results = analyzer.analyze(
        text=text,
        language=language,
        entities=entities,
    )

    return jsonify([r.to_dict() for r in results])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
