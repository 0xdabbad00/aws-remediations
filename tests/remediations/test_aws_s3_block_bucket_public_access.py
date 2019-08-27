from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_s3_block_bucket_public_access import AwsS3BlockBucketPublicAccess


class TestAwsS3BlockBucketPublicAccessConfigurable(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Name': 'TestName'
        }
        parameters = {
            'BlockPublicAcls': 'true',
            'IgnorePublicAcls': 'true',
            'BlockPublicPolicy': 'true',
            'RestrictPublicBuckets': 'true'
        }
        AwsS3BlockBucketPublicAccess()._fix(Session, resource, parameters)
        mock_session.assert_called_once_with('s3')

        mock_client.put_public_access_block.assert_called_with(
            Bucket='TestName',
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True,
            },
        )
