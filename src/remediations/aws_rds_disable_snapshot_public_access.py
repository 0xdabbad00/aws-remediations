from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsRdsDisableSnapshotPublicAccess(RemediationBase):
    """Remediation that disables public access for RDS instance snapshot"""

    @classmethod
    def _id(cls) -> str:
        return 'RDS.DisableSnapshotPublicAccess'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        client = session.client('rds')
        for snapshot_attrs in resource['SnapshotAttributes']:
            client.modify_db_snapshot_attribute(
                DBSnapshotIdentifier=snapshot_attrs['Id'],
                AttributeName='restore',
                ValuesToRemove=['all']
            )
