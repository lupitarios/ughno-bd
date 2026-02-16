# Technical Error Constants for UGH-NO Endpoint
from enum import Enum

from errors.error_definition import ErrorDefinition


class ErrorConstants(str, Enum):
    TEC_0001_RATE_LIMIT_ERROR = "Rate limit exceeded. Please try again later."
    TEC_0002_AUTHENTICATION_ERROR = "Authentication failed. Please check your API key."
    TEC_0003_CONNECTION_ERROR = "Failed to connect to the OpenAI API. Please check your network connection."
    TEC_0004_GENERAL_API_ERROR = "An error occurred while processing your request. Please try again."
    TEC_0005_TIMEOUT_ERROR = "The request to OpenAI timed out. Please try again."

TEC_0001_RATE_LIMIT_ERROR = ErrorDefinition("TEC-0001", ErrorConstants.TEC_0001_RATE_LIMIT_ERROR.value)
TEC_0002_AUTHENTICATION_ERROR = ErrorDefinition("TEC-0002", ErrorConstants.TEC_0002_AUTHENTICATION_ERROR.value)
TEC_0003_CONNECTION_ERROR = ErrorDefinition("TEC-0003", ErrorConstants.TEC_0003_CONNECTION_ERROR.value)
TEC_0004_GENERAL_API_ERROR = ErrorDefinition("TEC-0004", ErrorConstants.TEC_0004_GENERAL_API_ERROR.value)
TEC_0005_TIMEOUT_ERROR = ErrorDefinition("TEC-0005", ErrorConstants.TEC_0005_TIMEOUT_ERROR.value)