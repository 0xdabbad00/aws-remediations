class RemediationException(Exception):
    """Base exception class for remediations"""


class RemediationDoesNotExist(RemediationException):
    """Exception thrown when defined remediation couldn't be found"""


class RemediationAlreadyExists(RemediationException):
    """Exception thrown when a remediation with the same id already exists"""


class RemediationNotAuthorized(RemediationException):
    """Exception thrown when remediation was not authorized to perform operation on AWS resource"""


class InvalidInput(Exception):
    """Exception thrown when input to Lambda is invalid"""
