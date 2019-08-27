from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsIamUpdateAccountPasswordPolicy(RemediationBase):
    """Remediation that updates the Account password policy to provided values"""

    @classmethod
    def _id(cls) -> str:
        return 'IAM.UpdateAccountPasswordPolicy'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {
            'MinimumPasswordLength': '14',
            'RequireSymbols': 'true',
            'RequireNumbers': 'true',
            'RequireUppercaseCharacters': 'true',
            'RequireLowercaseCharacters': 'true',
            'AllowUsersToChangePassword': 'true',
            'MaxPasswordAge': '90',
            'PasswordReusePrevention': '24'
        }

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        session.client('iam').update_account_password_policy(
            MinimumPasswordLength=int(parameters['MinimumPasswordLength']),
            RequireSymbols=parameters['RequireSymbols'].lower() == 'true',
            RequireNumbers=parameters['RequireNumbers'].lower() == 'true',
            RequireUppercaseCharacters=parameters['RequireUppercaseCharacters'].lower() == 'true',
            RequireLowercaseCharacters=parameters['RequireLowercaseCharacters'].lower() == 'true',
            AllowUsersToChangePassword=parameters['AllowUsersToChangePassword'].lower() == 'true',
            MaxPasswordAge=int(parameters['MaxPasswordAge']),
            PasswordReusePrevention=int(parameters['PasswordReusePrevention'])
        )
