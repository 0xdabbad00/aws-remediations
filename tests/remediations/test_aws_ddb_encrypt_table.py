from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_ddb_encrypt_table import AwsDdbEncryptTable


class TestAwsDdbEncryptTable(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Name': 'TestName'
        }
        AwsDdbEncryptTable()._fix(Session, resource, {})
        mock_session.assert_called_once_with('dynamodb')
        mock_client.update_table.assert_called_once_with(
            TableName='TestName',
            SSESpecification={
                'Enabled': True,
                'SSEType': 'KMS'
            }
        )
