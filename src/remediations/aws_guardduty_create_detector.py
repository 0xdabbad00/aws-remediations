from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsGuardDutyCreateDetector(RemediationBase):
    """Remediation that creates a GuardDuty detector if one doesn't exist"""

    @classmethod
    def _id(cls) -> str:
        return 'GuardDuty.CreateDetector'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {'FindingPublishingFrequency': 'FIFTEEN_MINUTES'}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client("guardduty").create_detector(
            Enable=True, FindingPublishingFrequency=parameters['FindingPublishingFrequency']
        )
