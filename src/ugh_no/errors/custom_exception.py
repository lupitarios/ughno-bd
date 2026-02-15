from ugh_no.errors.constants.functional_errors import ErrorDefinition


class UserException(Exception):
    """Custom exception class for user-related errors."""
    def __init__(self, error: ErrorDefinition):
        self.error = error
        super().__init__(self.error)

    def __str__(self):
        return f"UserException: {self.error}"

class TechnicalException(Exception):
    """Custom exception class for technical errors."""
    def __init__(self, error: ErrorDefinition):
        self.error = error
        super().__init__(self.error)

    def __str__(self):
        return f"TechnicalException: {self.error}"