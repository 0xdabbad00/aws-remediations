from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_ec2_enable_vpc_flow_logs_to_s3 import AwsEc2EnableVpcFlowLogsToS3


class TestAwsEc2EnableVpcFlowLogsToS3(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Id': 'TestVpcId'
        }
        parameters = {
            'TargetBucketName': 'TestTargetBucketName',
            'TargetPrefix': 'TestTargetPrefix',
            'TrafficType': 'TestTrafficType'
        }
        mock_client.create_flow_logs.return_value = {}

        AwsEc2EnableVpcFlowLogsToS3()._fix(Session, resource, parameters)
        mock_session.assert_called_once_with('ec2')
        mock_client.create_flow_logs.assert_called_once_with(
            ResourceIds=['TestVpcId'],
            ResourceType='VPC',
            TrafficType='TestTrafficType',
            LogDestinationType='s3',
            LogDestination='arn:aws:s3:::TestTargetBucketName/TestTargetPrefix'
        )
