from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_ec2_stop_instance import AwsEc2StopInstance


class TestAwsEc2StopInstance(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Id': 'TestInstanceId'
        }
        AwsEc2StopInstance()._fix(Session, resource, {})
        mock_session.assert_called_once_with('ec2')
        mock_client.stop_instances.assert_called_once_with(InstanceIds=['TestInstanceId'])
