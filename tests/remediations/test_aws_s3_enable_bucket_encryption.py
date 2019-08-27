from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_s3_enable_bucket_encryption import AwsS3EnableBucketEncryption


class TestAwsS3EnableBucketEncryption(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Name': 'TestName'
        }
        parameters = {
            'SSEAlgorithm': 'TestSSEAlgorithm',
            'KMSMasterKeyID': 'TestKMSMasterKeyID'
        }
        AwsS3EnableBucketEncryption()._fix(Session, resource,parameters)
        mock_session.assert_called_once_with('s3')

        mock_client.put_bucket_encryption.assert_called_with(
            Bucket='TestName',
            ServerSideEncryptionConfiguration={
                'Rules':
                    [
                        {
                            'ApplyServerSideEncryptionByDefault':
                                {
                                    'SSEAlgorithm': 'TestSSEAlgorithm',
                                    'KMSMasterKeyID': 'TestKMSMasterKeyID'
                                },
                        },
                    ],
            },
        )
