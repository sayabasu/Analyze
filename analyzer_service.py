import os

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import SpacyNlpEngine
from presidio_analyzer.predefined_recognizers.in_aadhaar_recognizer import (
    InAadhaarRecognizer,
)
from presidio_analyzer.predefined_recognizers.in_pan_recognizer import InPanRecognizer
from presidio_analyzer.predefined_recognizers.in_passport_recognizer import (
    InPassportRecognizer,
)
from presidio_analyzer.predefined_recognizers.in_voter_recognizer import (
    InVoterRecognizer,
)

from custom_recognizers_india import gstin_recognizer

load_dotenv()

API_KEY = os.environ.get("ANALYZER_API_KEY")
API_KEY_HEADER = "X-API-Key"


from werkzeug.datastructures import Headers


def _is_authorized(headers: Headers) -> bool:
    if not API_KEY:
        return True

    return headers.get(API_KEY_HEADER) == API_KEY


_ENTITY_FILTER_CANDIDATES = [
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "URL",
    "CREDIT_CARD",
    "IBAN_CODE",
    "IP_ADDRESS",
    "IN_PAN",
    "IN_AADHAAR",
    "IN_PASSPORT",
    "IN_VOTER",
    "IN_GSTIN",
]


def _is_truthy_env(value: str | None) -> bool:
    if not value:
        return False

    return value.strip().lower() in {"1", "true", "on", "yes"}


def _load_entity_filter() -> list[str]:
    enabled = [
        entity
        for entity in _ENTITY_FILTER_CANDIDATES
        if _is_truthy_env(os.environ.get(entity))
    ]
    return enabled or _ENTITY_FILTER_CANDIDATES


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
if not nlp_engine.is_loaded():
    nlp_engine.load()

# -------------------------------------------------------
# 2) Register built-in + custom recognizers
# -------------------------------------------------------
registry = RecognizerRegistry()
registry.load_predefined_recognizers(nlp_engine=nlp_engine, languages=["en"])
registry.add_recognizer(gstin_recognizer)
registry.add_recognizer(InPanRecognizer())
registry.add_recognizer(InAadhaarRecognizer())
registry.add_recognizer(InPassportRecognizer())
registry.add_recognizer(InVoterRecognizer())

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
DEFAULT_ENTITY_FILTER = _load_entity_filter()


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not _is_authorized(request.headers):
        return jsonify({"error": "Unauthorized"}), 401

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
    port = int(os.environ.get("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
