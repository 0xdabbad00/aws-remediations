from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_guardduty_create_detector import AwsGuardDutyCreateDetector


class TestAwsGuardDutyCreateDetector(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        parameters = {
            'FindingPublishingFrequency': 'TestFindingPublishingFrequency'
        }
        mock_client.create_flow_logs.return_value = {}

        AwsGuardDutyCreateDetector()._fix(Session, {}, parameters)
        mock_session.assert_called_once_with('guardduty')
        mock_client.create_detector.assert_called_once_with(
            Enable=True,
            FindingPublishingFrequency='TestFindingPublishingFrequency'
        )
