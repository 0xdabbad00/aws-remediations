from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsIamDeleteInactiveAccessKeys(RemediationBase):
    """Remediation that deletes inactive user access keys"""

    @classmethod
    def _id(cls) -> str:
        return 'IAM.DeleteInactiveAccessKeys'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        client = session.client('iam')
        if 'AccessKey1Active' in resource['CredentialReport'
                                         ] and not resource['CredentialReport']['AccessKey1Active']:
            client.delete_access_key(
                UserName=resource['UserName'],
                AccessKeyId=resource['CredentialReport']['AccessKey1Id']
            )
        if 'AccessKey2Active' in resource['CredentialReport'
                                         ] and not resource['CredentialReport']['AccessKey2Active']:
            client.delete_access_key(
                UserName=resource['UserName'],
                AccessKeyId=resource['CredentialReport']['AccessKey2Id']
            )
