from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsCloudTrailEnableLogValidation(RemediationBase):
    """Remediation that enables log validation for existing CloudTrail trail"""

    @classmethod
    def _id(cls) -> str:
        return 'CloudTrail.EnableLogValidation'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client('cloudtrail'
                      ).update_trail(Name=resource['Name'], EnableLogFileValidation=True)
