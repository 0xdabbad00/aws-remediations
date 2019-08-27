from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsS3BlockBucketPublicACL(RemediationBase):
    """Remediation that blocks public permissions for an S3 bucket"""

    @classmethod
    def _id(cls) -> str:
        return 'S3.BlockBucketPublicACL'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client('s3').put_bucket_acl(
            Bucket=resource['Name'],
            ACL='private',
        )
