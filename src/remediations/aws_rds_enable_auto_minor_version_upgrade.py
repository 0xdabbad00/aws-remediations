from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsRdsEnableAutoMinorVersionUpgrade(RemediationBase):
    """Remediation that enables Auto Minor Version upgrade for RDS instances"""

    @classmethod
    def _id(cls) -> str:
        return 'RDS.EnableAutoMinorVersionUpgrade'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {'ApplyImmediately': 'true'}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client('rds').modify_db_instance(
            DBInstanceIdentifier=resource['Id'],
            AutoMinorVersionUpgrade=True,
            ApplyImmediately=parameters['ApplyImmediately'].lower() == 'true'
        )
