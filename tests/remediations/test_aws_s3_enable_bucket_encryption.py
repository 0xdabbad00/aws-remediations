from unittest import mock, TestCase
from boto3 import Session

from app.exceptions import InvalidParameterException
from remediations.aws_s3_enable_bucket_encryption import AwsS3EnableBucketEncryption


class TestAwsS3EnableBucketEncryption(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix_aes256(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Name': 'TestName'
        }
        parameters = {
            'SSEAlgorithm': 'AES256',
            'KMSMasterKeyID': ''
        }
        AwsS3EnableBucketEncryption()._fix(Session, resource, parameters)
        mock_session.assert_called_once_with('s3')

        mock_client.put_bucket_encryption.assert_called_with(
            Bucket='TestName',
            ServerSideEncryptionConfiguration={
                'Rules':
                    [
                        {
                            'ApplyServerSideEncryptionByDefault':
                                {
                                    'SSEAlgorithm': 'AES256'
                                },
                        },
                    ],
            },
        )

    @mock.patch.object(Session, 'client')
    def test_fix_kms(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Name': 'TestName'
        }
        parameters = {
            'SSEAlgorithm': 'aws:kms',
            'KMSMasterKeyID': '313e6a3d-57c7-4544-ba59-0fecaabaf7b2'
        }
        AwsS3EnableBucketEncryption()._fix(Session, resource, parameters)
        mock_session.assert_called_once_with('s3')

        mock_client.put_bucket_encryption.assert_called_with(
            Bucket='TestName',
            ServerSideEncryptionConfiguration={
                'Rules':
                    [
                        {
                            'ApplyServerSideEncryptionByDefault':
                                {
                                    'SSEAlgorithm': 'aws:kms',
                                    'KMSMasterKeyID': '313e6a3d-57c7-4544-ba59-0fecaabaf7b2'
                                },
                        },
                    ],
            },
        )

    @mock.patch.object(Session, 'client')
    def test_fix_unknown_algorithm(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Name': 'TestName'
        }
        parameters = {
            'SSEAlgorithm': 'unknown'
        }

        self.assertRaises(InvalidParameterException, AwsS3EnableBucketEncryption()._fix, Session, resource, parameters)
        mock_session.assert_not_called()
