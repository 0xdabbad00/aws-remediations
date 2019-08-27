from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_kms_enable_key_rotation import AwsKmsEnableKeyRotation


class TestAwsIamUpdateAccountPasswordPolicy(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        resource = {
            'Id': 'TestKeyId'
        }
        AwsKmsEnableKeyRotation()._fix(Session, resource, {})
        mock_session.assert_called_once_with('kms')
        mock_client.enable_key_rotation.assert_called_once_with(
            KeyId='TestKeyId'
        )

