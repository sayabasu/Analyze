from presidio_analyzer import Pattern, PatternRecognizer


# -------------------------
# PAN (Permanent Account Number)
# Format: 5 letters + 4 digits + 1 letter
# Example: ABCDE1234F
# -------------------------
pan_pattern = Pattern(
    name="pan_pattern",
    regex=r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    score=0.85,  # confidence score, tune as needed
)

pan_recognizer = PatternRecognizer(
    supported_entity="IN_PAN",
    patterns=[pan_pattern],
    # optional context words to boost confidence
    context=["pan", "permanent account", "income tax"]
)


# -------------------------
# Aadhaar (12-digit ID)
# Typical written forms:
#   123412341234
#   1234 1234 1234
# First digit: 2–9
# -------------------------
aadhaar_patterns = [
    # 12 digits, no spaces
    Pattern(
        name="aadhaar_12digits",
        regex=r"\b[2-9][0-9]{11}\b",
        score=0.80,
    ),
    # grouped with spaces: 1234 5678 9012
    Pattern(
        name="aadhaar_grouped",
        regex=r"\b[2-9][0-9]{3}\s[0-9]{4}\s[0-9]{4}\b",
        score=0.80,
    ),
]

aadhaar_recognizer = PatternRecognizer(
    supported_entity="IN_AADHAAR",
    patterns=aadhaar_patterns,
    context=["aadhaar", "uidai", "aadhar"]  # include common spelling too
)
