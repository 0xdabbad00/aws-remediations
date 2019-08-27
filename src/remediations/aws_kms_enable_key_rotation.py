from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsKmsEnableKeyRotation(RemediationBase):
    """Remediation that enables rotation for a KMS key"""

    @classmethod
    def _id(cls) -> str:
        return 'KMS.EnableKeyRotation'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client('kms').enable_key_rotation(KeyId=resource['Id'])
