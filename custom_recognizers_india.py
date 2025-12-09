from presidio_analyzer import Pattern, PatternRecognizer


class GstinRecognizer(PatternRecognizer):
    """Simple GSTIN recognizer for Indian tax identifiers."""

    PATTERNS = [
        Pattern(
            "GSTIN",
            r"\b\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]\b",
            0.6,
        ),
    ]

    CONTEXT = ["gstin", "goods and services tax", "gst number"]

    def __init__(self, patterns=None, context=None, supported_language="en", supported_entity="IN_GSTIN"):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )


gstin_recognizer = GstinRecognizer()
