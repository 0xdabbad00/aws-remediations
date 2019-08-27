from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_rds_disable_instance_public_access import AwsRdsDisableInstancePublicAccess


class TestAwsRdsDisableInstancePublicAccess(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Id': 'TestDBInstanceIdentifier'
        }
        AwsRdsDisableInstancePublicAccess()._fix(Session, resource, {})
        mock_session.assert_called_once_with('rds')
        mock_client.modify_db_instance.assert_called_once_with(
            DBInstanceIdentifier='TestDBInstanceIdentifier',
            PubliclyAccessible=False
        )


