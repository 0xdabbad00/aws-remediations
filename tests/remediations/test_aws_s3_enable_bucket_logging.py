from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_s3_enable_bucket_versioning import AwsS3EnableBucketVersioning


class TestAwsS3EnableBucketVersioning(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Name': 'TestName'
        }
        AwsS3EnableBucketVersioning()._fix(Session, resource, {})
        mock_session.assert_called_once_with('s3')

        mock_client.put_bucket_versioning.assert_called_with(
            Bucket='TestName',
            VersioningConfiguration={'Status': 'Enabled'}
        )
