import ipaddress
from typing import Optional, List

from presidio_analyzer import Pattern, PatternRecognizer


class CaQcNamRecognizer(PatternRecognizer):
    """
    Recognize Quebec NAM using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Quebec NAM (Medium)",
            r"\b([a-zA-Z]{4}[ -]?[0-9]{4}[ -]?[0-9]{4})\b",  # noqa: E501
            0.5,
        ),
    ]

    CONTEXT = [
        "nam",
        "numéro d'assurance maladie",
        "assurance maladie",
        "ramq",
        "assurance",
        "carte soleil",
        "medical insurance",
        "health insurance",
        "health card",
        "healthcare",
        "health care",
        "health",
        "healthcard",
        "health card",
        "health insurance card",
        "healthcare card",
        "health care card",
        "healthcare number",
        "health care number",
        "health number",
        "healthcard number",
        "health card number",
        "health insurance card number",
        "healthcare card number",
        "health care card number",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "CA_QC_NAM",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )

    def invalidate_result(self, pattern_text: str) -> bool:
        """
        Check if the pattern text cannot be validated as a CA_QC_NAM entity.

        :param pattern_text: Text detected as pattern by regex
        :return: True if invalidated
        """
        # if there are delimiters, make sure both delimiters are the same
        clean_string = pattern_text.replace(" ", "").replace("-", "")
        if len(clean_string) != 12:
            return True

        # Months are augmented of 50 for women
        if not int(clean_string[6:8]) in range(1, 13) and not int(clean_string[6:8]) in range(51, 63):
            return True

        if not int(clean_string[8:10]) in range(1, 32):
            return True

        return False