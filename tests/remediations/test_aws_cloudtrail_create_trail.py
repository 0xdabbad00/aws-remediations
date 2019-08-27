from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_cloudtrail_create_trail import AwsCloudTrailCreateTrail


class TestAwsCloudTrailCreateTrail(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        parameters = {
            'Name': 'TestTrailName',
            'TargetBucketName': 'TestTargetBucketName',
            'TargetPrefix': 'TestTargetPrefix',
            'SnsTopicName': 'TestSnsTopicName',
            'IncludeGlobalServiceEvents': 'True',
            'IsMultiRegionTrail': 'True',
            'KmsKeyId': 'TestKmsKeyId',
            'IsOrganizationTrail': 'True'
        }

        AwsCloudTrailCreateTrail()._fix(Session, {}, parameters)
        mock_session.assert_called_once_with('cloudtrail')
        mock_client.create_trail.assert_called_once_with(
            Name='TestTrailName',
            S3BucketName='TestTargetBucketName',
            S3KeyPrefix='TestTargetPrefix',
            SnsTopicName='TestSnsTopicName',
            IncludeGlobalServiceEvents=True,
            IsMultiRegionTrail=True,
            EnableLogFileValidation=True,
            KmsKeyId='TestKmsKeyId',
            IsOrganizationTrail=True
        )
        mock_client.start_logging.assert_called_once_with(Name='TestTrailName')
