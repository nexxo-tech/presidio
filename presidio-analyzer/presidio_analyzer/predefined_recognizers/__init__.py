"""Predefined recognizers package. Holds all the default recognizers."""

from presidio_analyzer.predefined_recognizers.transformers_recognizer import (
    TransformersRecognizer,
)
from .aba_routing_recognizer import AbaRoutingRecognizer
from .credit_card_recognizer import CreditCardRecognizer
from .crypto_recognizer import CryptoRecognizer
from .date_recognizer import DateRecognizer
from .email_recognizer import EmailRecognizer
from .es_nif_recognizer import EsNifRecognizer
from .iban_recognizer import IbanRecognizer
from .ip_recognizer import IpRecognizer
from .it_driver_license_recognizer import ItDriverLicenseRecognizer
from .it_fiscal_code_recognizer import ItFiscalCodeRecognizer
from .it_identity_card_recognizer import ItIdentityCardRecognizer
from .it_passport_recognizer import ItPassportRecognizer
from .it_vat_code import ItVatCodeRecognizer
from .medical_license_recognizer import MedicalLicenseRecognizer
from .phone_recognizer import PhoneRecognizer
from .sg_fin_recognizer import SgFinRecognizer
from .spacy_recognizer import SpacyRecognizer
from .stanza_recognizer import StanzaRecognizer
from .uk_nhs_recognizer import NhsRecognizer
from .url_recognizer import UrlRecognizer
from .us_bank_recognizer import UsBankRecognizer
from .us_driver_license_recognizer import UsLicenseRecognizer
from .us_itin_recognizer import UsItinRecognizer
from .us_passport_recognizer import UsPassportRecognizer
from .us_ssn_recognizer import UsSsnRecognizer
from .au_abn_recognizer import AuAbnRecognizer
from .au_acn_recognizer import AuAcnRecognizer
from .au_tfn_recognizer import AuTfnRecognizer
from .au_medicare_recognizer import AuMedicareRecognizer
from .in_pan_recognizer import InPanRecognizer
from .pl_pesel_recognizer import PlPeselRecognizer
from .azure_ai_language import AzureAILanguageRecognizer
from .in_aadhaar_recognizer import InAadhaarRecognizer
from .in_vehicle_registration_recognizer import InVehicleRegistrationRecognizer

from .ca_qc_nam_recognizer import CaQcNamRecognizer
from .ca_qc_dl_recognizer import CaQcDlRecognizer
from .ca_pc_recognizer import CaPcRecognizer
from .ca_sin_recognizer import CaSinRecognizer
from .ca_passport_recognizer import CaPassportRecognizer
from .ca_bank_recognizer import CaBankRecognizer

NLP_RECOGNIZERS = {
    "spacy": SpacyRecognizer,
    "stanza": StanzaRecognizer,
    "transformers": TransformersRecognizer,
}

__all__ = [
    "AbaRoutingRecognizer",
    "CreditCardRecognizer",
    "CryptoRecognizer",
    "DateRecognizer",
    "EmailRecognizer",
    "IbanRecognizer",
    "IpRecognizer",
    "NhsRecognizer",
    "MedicalLicenseRecognizer",
    "PhoneRecognizer",
    "SgFinRecognizer",
    "UrlRecognizer",
    "UsBankRecognizer",
    "UsItinRecognizer",
    "UsLicenseRecognizer",
    "UsPassportRecognizer",
    "UsSsnRecognizer",
    "EsNifRecognizer",
    "SpacyRecognizer",
    "StanzaRecognizer",
    "NLP_RECOGNIZERS",
    "AuAbnRecognizer",
    "AuAcnRecognizer",
    "AuTfnRecognizer",
    "AuMedicareRecognizer",
    "TransformersRecognizer",
    "ItDriverLicenseRecognizer",
    "ItFiscalCodeRecognizer",
    "ItVatCodeRecognizer",
    "ItIdentityCardRecognizer",
    "ItPassportRecognizer",
    "InPanRecognizer",
    "PlPeselRecognizer",
    "AzureAILanguageRecognizer",
    "InAadhaarRecognizer",
    "InVehicleRegistrationRecognizer",

    # Sortify
    "CaQcNamRecognizer",
    "CaQcDlRecognizer",
    "CaSinRecognizer",
    "CaPcRecognizer",
    "CaCpRecognizer",
    "CaPassportRecognizer",
    "CaBankRecognizer",
]
