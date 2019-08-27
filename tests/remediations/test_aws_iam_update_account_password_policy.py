from unittest import mock, TestCase
from boto3 import Session
from src.remediations.aws_iam_update_account_password_policy import AwsIamUpdateAccountPasswordPolicy


class TestAwsIamUpdateAccountPasswordPolicy(TestCase):

    @mock.patch.object(Session, 'client')
    def test_fix(self, mock_session):
        mock_client = mock.Mock()
        mock_session.return_value = mock_client
        parameters = {
            'MinimumPasswordLength': '10',
            'RequireSymbols': 'True',
            'RequireNumbers': 'True',
            'RequireUppercaseCharacters': 'True',
            'RequireLowercaseCharacters': 'True',
            'AllowUsersToChangePassword': 'True',
            'MaxPasswordAge': '100',
            'PasswordReusePrevention': '1000'
        }
        AwsIamUpdateAccountPasswordPolicy()._fix(Session, {}, parameters)
        mock_session.assert_called_once_with('iam')
        mock_client.update_account_password_policy.assert_called_once_with(
            MinimumPasswordLength=10,
            RequireSymbols=True,
            RequireNumbers=True,
            RequireUppercaseCharacters=True,
            RequireLowercaseCharacters=True,
            AllowUsersToChangePassword=True,
            MaxPasswordAge=100,
            PasswordReusePrevention=1000
        )

