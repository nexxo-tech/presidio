from hashlib import sha256
from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer

class PasswordRecognizer(PatternRecognizer):
    """Recognize common passwords using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern("Password (weak)", r"[^\>]{8,59}", 0.2),
    ]

    CONTEXT = ["password", "pwd", "mot de passe", "mpd", "pass"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "PASSWORD",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )

