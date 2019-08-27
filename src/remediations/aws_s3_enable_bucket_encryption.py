from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsS3EnableBucketEncryption(RemediationBase):
    """Remediation that enables encryption for an S3 bucket"""

    @classmethod
    def _id(cls) -> str:
        return 'S3.EnableBucketEncryption'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {'SSEAlgorithm': 'AES256', 'KMSMasterKeyID': ''}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client('s3').put_bucket_encryption(
            Bucket=resource['Name'],
            ServerSideEncryptionConfiguration={
                'Rules':
                    [
                        {
                            'ApplyServerSideEncryptionByDefault':
                                {
                                    'SSEAlgorithm': parameters['SSEAlgorithm'],
                                    'KMSMasterKeyID': parameters['KMSMasterKeyID']
                                },
                        },
                    ],
            },
        )
