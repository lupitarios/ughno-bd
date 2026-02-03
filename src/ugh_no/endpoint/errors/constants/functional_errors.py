# Functional Error Constants for UGH-NO Endpoint
from enum import Enum

from src.ugh_no.endpoint.errors.error_definition import ErrorDefinition


class ErrorConstants(str, Enum):
    TF_0001_RATE_LIMIT_ERROR = "Rate limit exceeded. Please wait 24hrs or change the tier."
    TF_0002_GENERAL_API_ERROR = "An error occurred while processing your request. Please try again."

C_TF_0001_RATE_LIMIT_ERROR = ErrorDefinition("TF-0001", ErrorConstants.TF_0001_RATE_LIMIT_ERROR.value)
C_TF_0002_GENERAL_API_ERROR = ErrorDefinition("TF-0002", ErrorConstants.TF_0002_GENERAL_API_ERROR.value)