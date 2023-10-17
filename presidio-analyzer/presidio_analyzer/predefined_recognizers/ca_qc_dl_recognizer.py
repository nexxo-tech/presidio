import ipaddress
from typing import Optional, List

from presidio_analyzer import Pattern, PatternRecognizer


class CaQcDlRecognizer(PatternRecognizer):
    """
    Recognize Quebec Driving license using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "Quebec Driving License (Medium)",
            r"\b([a-zA-Z]{1}[0-9]{4}[ -]?[0-9]{6}[ -]?[0-9]{2})\b",  # noqa: E501
            0.5,
        ),
    ]

    CONTEXT = [
        "permis",
        "conduire",
        "permis de conduire",
        "conducteur"
        "driving",
        "driver",
        "license",
        "licence",
        "driving license",
        "driver license",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "CA_QC_DL",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )
