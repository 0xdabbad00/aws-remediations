from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsEc2StopInstance(RemediationBase):
    """Remediation that stops an EC2 instance"""

    @classmethod
    def _id(cls) -> str:
        return 'EC2.StopInstance'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client('ec2').stop_instances(InstanceIds=[
            resource['Id'],
        ])
