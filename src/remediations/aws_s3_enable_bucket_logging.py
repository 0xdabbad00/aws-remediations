from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsS3EnableBucketLogging(RemediationBase):
    """Remediation that enables S3 bucket access logging"""

    @classmethod
    def _id(cls) -> str:
        return 'S3.EnableBucketLogging'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {'TargetBucket': '', 'TargetPrefix': ''}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client('s3').put_bucket_logging(
            Bucket=resource['Name'],
            BucketLoggingStatus={
                'LoggingEnabled':
                    {
                        'TargetBucket': parameters['TargetBucket'],
                        'TargetPrefix': parameters['TargetPrefix']
                    }
            }
        )
