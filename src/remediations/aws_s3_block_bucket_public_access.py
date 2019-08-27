from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsS3BlockBucketPublicAccess(RemediationBase):
    """Remediation that puts an S3 bucket block public access configuration"""

    @classmethod
    def _id(cls) -> str:
        return 'S3.BlockBucketPublicAccess'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {
            'BlockPublicAcls': 'true',
            'IgnorePublicAcls': 'true',
            'BlockPublicPolicy': 'true',
            'RestrictPublicBuckets': 'true'
        }

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client('s3').put_public_access_block(
            Bucket=resource['Name'],
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': parameters['BlockPublicAcls'].lower() == 'true',
                'IgnorePublicAcls': parameters['IgnorePublicAcls'].lower() == 'true',
                'BlockPublicPolicy': parameters['BlockPublicPolicy'].lower() == 'true',
                'RestrictPublicBuckets': parameters['RestrictPublicBuckets'].lower() == 'true',
            },
        )
