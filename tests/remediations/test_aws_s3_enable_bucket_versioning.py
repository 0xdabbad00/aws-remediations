from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_s3_enable_bucket_logging import AwsS3EnableBucketLogging


class TestAwsS3EnableBucketLogging(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Name': 'TestName'
        }
        parameters = {
            'TargetBucket': 'TestTargetBucket',
            'TargetPrefix': 'TestTargetPrefix'
        }
        AwsS3EnableBucketLogging()._fix(Session, resource,parameters)
        mock_session.assert_called_once_with('s3')

        mock_client.put_bucket_logging.assert_called_with(
            Bucket='TestName',
            BucketLoggingStatus={
                'LoggingEnabled':
                    {
                        'TargetBucket': 'TestTargetBucket',
                        'TargetPrefix': 'TestTargetPrefix'
                    }
            }
        )
