from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsDdbEncryptTable(RemediationBase):
    """Remediation that creates a KMS key and uses it to encrypt DDB table"""

    @classmethod
    def _id(cls) -> str:
        return 'DDB.EncryptTable'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client('dynamodb').update_table(
            TableName=resource['Name'], SSESpecification={
                'Enabled': True,
                'SSEType': 'KMS'
            }
        )
