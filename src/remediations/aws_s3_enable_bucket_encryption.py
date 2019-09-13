from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase
from app.exceptions import InvalidParameterException


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
        if parameters['SSEAlgorithm'] == 'AES256':
            session.client('s3').put_bucket_encryption(
                Bucket=resource['Name'],
                ServerSideEncryptionConfiguration={
                    'Rules': [{
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        },
                    },],
                },
            )
        elif parameters['SSEAlgorithm'] == 'aws:kms':
            session.client('s3').put_bucket_encryption(
                Bucket=resource['Name'],
                ServerSideEncryptionConfiguration={
                    'Rules':
                        [
                            {
                                'ApplyServerSideEncryptionByDefault':
                                    {
                                        'SSEAlgorithm': "aws:kms",
                                        'KMSMasterKeyID': parameters['KMSMasterKeyID']
                                    },
                            },
                        ],
                },
            )
        else:
            raise InvalidParameterException(
                "Invalid value {} for parameter {}".format(
                    parameters['SSEAlgorithm'], 'SSEAlgorithm'
                )
            )
