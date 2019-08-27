from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_cloudtrail_enable_log_validation import AwsCloudTrailEnableLogValidation


class TestAwsCloudTrailEnableLogValidation(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Name': 'TestName'
        }
        AwsCloudTrailEnableLogValidation()._fix(Session, resource, {})
        mock_session.assert_called_once_with('cloudtrail')
        mock_client.update_trail.assert_called_once_with(
            Name='TestName',
            EnableLogFileValidation=True
        )
