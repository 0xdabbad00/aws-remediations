from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsS3EnableBucketVersioning(RemediationBase):
    """Remediation that enables versioning for an S3 bucket"""

    @classmethod
    def _id(cls) -> str:
        return 'S3.EnableBucketVersioning'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client('s3').put_bucket_versioning(
            Bucket=resource['Name'], VersioningConfiguration={'Status': 'Enabled'}
        )
