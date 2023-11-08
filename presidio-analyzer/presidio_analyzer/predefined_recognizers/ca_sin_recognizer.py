import ipaddress

from collections import defaultdict
from typing import Optional, List, Tuple

from presidio_analyzer import Pattern, PatternRecognizer


class CaSinRecognizer(PatternRecognizer):
    """Recognize CA Social Insurance Number (SIN) using regex. Inspired from https://learn.microsoft.com/en-us/purview/sit-defn-canada-social-insurance-number

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    :param replacement_pairs: List of tuples with potential replacement values
    """

    PATTERNS = [
        Pattern("SIN1 (weak)", r"\b[0-9]{9}\b", 0.2),
        Pattern("SIN2 (medium)", r"\b([0-9]{3})[- .]([0-9]{3})[- .]([0-9]{3})[- .]?([0-9]{0,3})$\b", 0.5),
    ]

    CONTEXT = [
        "nas",
        "NAS",
        "assurance",
        "numero d'assurance sociale",
        "carte d’assurance sociale",
        "assurance social",
        "assurance sociale",
        "numéro d’assurance social",
        "numéro d’assurance sociale",
        "sociale",
        "#nas",
        "ssn",
        "sin",
        "ssns",
        "#sin",
        "#",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "fr",
        supported_entity: str = "CA_SIN",
        replacement_pairs: Optional[List[Tuple[str, str]]] = None,
    ):
        self.replacement_pairs = (
            replacement_pairs if replacement_pairs else [("-", ""), (" ", ""), (".", "")]
        )
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )
    
    def validate_result(self, pattern_text: str) -> bool:  # noqa D102
        sanitized_value = self.__sanitize_value(pattern_text, self.replacement_pairs)
        checksum = self.__luhn_checksum(sanitized_value)

        return checksum

    def invalidate_result(self, pattern_text: str) -> bool:
        """
        Check if the pattern text cannot be validated as a CA_SIN entity.

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
        if only_digits[0] == "8":
            # cannot start with 8 : https://www.canada.ca/en/employment-social-development/services/sin.html
            return True

        if only_digits[0:3] == "000" or only_digits[3:6] == "000" or only_digits[6:] == "000":
            # groups cannot be all zeros
            return True
        
        if len(only_digits) != 9:
            return True

        try:
            ipaddress.ip_address(pattern_text)
            return True
        except ValueError:
            return False

        return False

    @staticmethod
    def __luhn_checksum(sanitized_value: str) -> bool:
        def digits_of(n: str) -> List[int]:
            return [int(dig) for dig in str(n)]

        digits = digits_of(sanitized_value)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(str(d * 2)))
        return checksum % 10 == 0

    @staticmethod
    def __sanitize_value(text: str, replacement_pairs: List[Tuple[str, str]]) -> str:
        for search_string, replacement_string in replacement_pairs:
            text = text.replace(search_string, replacement_string)
        return text