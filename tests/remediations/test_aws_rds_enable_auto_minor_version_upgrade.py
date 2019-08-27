from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_rds_enable_auto_minor_version_upgrade import AwsRdsEnableAutoMinorVersionUpgrade


class TestAwsRdsEnableAutoMinorVersionUpgrade(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Id': 'TestDBInstanceIdentifier'
        }
        parameters = {
            'ApplyImmediately': 'true'
        }
        AwsRdsEnableAutoMinorVersionUpgrade()._fix(Session, resource, parameters)
        mock_session.assert_called_once_with('rds')

        mock_client.modify_db_instance.assert_called_with(
            DBInstanceIdentifier='TestDBInstanceIdentifier',
            AutoMinorVersionUpgrade=True,
            ApplyImmediately=True
        )
