from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsRdsDisableInstancePublicAccess(RemediationBase):
    """Remediation that disables public access for an RDS instance"""

    @classmethod
    def _id(cls) -> str:
        return 'RDS.DisableInstancePublicAccess'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client('rds').modify_db_instance(
            DBInstanceIdentifier=resource['Id'], PubliclyAccessible=False
        )
