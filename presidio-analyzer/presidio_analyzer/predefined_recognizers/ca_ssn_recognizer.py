import ipaddres
from collections import defaultdict
from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CaSsnRecognizer(PatternRecognizer):
    """Recognize CA Social Security Number (SSN) using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern("SSN1 (weak)", r"\b[0-9]{9}\b", 0.2),
        Pattern("SSN2 (medium)", r"\b([0-9]{3})[- .]([0-9]{3})[- .]([0-9]{3})\b", 0.5),
    ]

    CONTEXT = [
        "nas",
        "assurance",
        "sociale",
        "#nas",
        "ssn",
        "sin",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "CA_SSN",
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
        Check if the pattern text cannot be validated as a CA_SSN entity.

        :param pattern_text: Text detected as pattern by regex
        :return: True if invalidated
        """
        # if there are delimiters, make sure both delimiters are the same
        delimiter_counts = defaultdict(int)
        for c in pattern_text:
            if c in (".", "-", " "):
                delimiter_counts[c] += 1
        if len(delimiter_counts.keys()) > 1:
            # mismatched delimiters
            return True

        only_digits = "".join(c for c in pattern_text if c.isdigit())
        if all(only_digits[0] == c for c in only_digits):
            # cannot be all same digit
            return True

        if only_digits[3:5] == "00" or only_digits[5:] == "0000":
            # groups cannot be all zeros
            return True

        for sample_ssn in ("000", "666", "123456789", "98765432", "078051120"):
            if only_digits.startswith(sample_ssn):
                return True

        try:
            ipaddress.ip_address(pattern_text)
            return True
        except ValueError:
            return False

        return False
