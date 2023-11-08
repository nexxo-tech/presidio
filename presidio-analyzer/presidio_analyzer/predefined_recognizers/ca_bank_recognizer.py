from typing import Optional, List

from presidio_analyzer import Pattern, PatternRecognizer


class CaBankRecognizer(PatternRecognizer):
    """
    Recognizes CA bank number using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern("Bank Account (Weak)", r"\b[0-9]{7}\b", 0.1),
        Pattern("Bank Account (Medium)", r"\b([0-9]{5})[- .]([0-9]{3})[- .]([0-9]{7})$\b", 0.5),
    ]

    CONTEXT = [
        "compte",
        "bancaire",
        "desjardins",
        "banque",
        "banque nationale",
        "banque royale",
        "banque td",
        "banque scotia",
        "banque de montréal",
        "banque de montreal",
        "banque laurentienne",
        "cibc",
        "folio",
        "bank",
        "account",
        "account#",
        "acct",
        "debit",
        "institution",
        "institution financière",
        "financial institution",
        "financial",
        "transit",
        "checquing"
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "CA_BANK_ACCOUNT",
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
        Check if the pattern text cannot be validated as a CA_BANK_ACCOUNT entity.

        :param pattern_text: Text detected as pattern by regex
        :return: True if invalidated
        """
        only_digits = "".join(c for c in pattern_text if c.isdigit())
        if all(only_digits[0] == c for c in only_digits):
            # cannot be all same digit
            return True

        return False