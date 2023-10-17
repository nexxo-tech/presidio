import ipaddress
from typing import Optional, List

from presidio_analyzer import Pattern, PatternRecognizer


class CaCpRecognizer(PatternRecognizer):
    """
    Recognize Canadian Postal Code using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Postal Code (Medium)",
            r"\b([a-zA-Z]\d[a-zA-Z][ -]?\d[a-zA-Z]\d)\b",  # noqa: E501
            0.5,
        ),
    ]

    CONTEXT = [
        "postal code",
        "zip code",
        "code postal",
        "code zip",
        "cp",
        "zip",
        "postal",
        "code",
        "adresse",
        "addresse",
        "address",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "CA_POSTAL_CODE",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )