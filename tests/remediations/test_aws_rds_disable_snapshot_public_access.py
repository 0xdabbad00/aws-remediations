from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_rds_disable_snapshot_public_access import AwsRdsDisableSnapshotPublicAccess


class TestAwsRdsDisableSnapshotPublicAccess(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'SnapshotAttributes': [
                {
                    'Id': 'DBSnapshotIdentifier1'
                }
            ]
        }
        AwsRdsDisableSnapshotPublicAccess()._fix(Session, resource, {})
        mock_session.assert_called_once_with('rds')

        mock_client.modify_db_snapshot_attribute.assert_called_with(
                DBSnapshotIdentifier='DBSnapshotIdentifier1',
                AttributeName='restore',
                ValuesToRemove=['all']
            )
